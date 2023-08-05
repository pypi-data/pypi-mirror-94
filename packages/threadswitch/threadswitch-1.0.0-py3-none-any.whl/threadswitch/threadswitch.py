"""ThreadSwitch main class
Copyright (c) Kiruse 2021. See license in LICENSE."""
from __future__ import annotations
from concurrent.futures import Future as CFuture
from functools import partial
from threading import Thread, Condition
from typing import *
from .errors import *
from .utils import *
import asyncio
import functools
import threading

T = TypeVar('T')

class InvalidStateError(Exception): pass

class ContextBase:
    def __init__(self):
        self._thread: Optional[Thread] = None
        self._queue = TaskQueue()
        self._done_future = CFuture()
        self._terminate: bool = False
        self._lock = threading.RLock()
    
    def dispatch(self, task: Callable[..., T], *args, **kwargs) -> Awaitable[T]:
        if self._terminate:
            raise InvalidStateError("Context terminated")
        ret = Task(task, args, kwargs)
        self._queue.push(ret)
        return ret
    
    def task(self, fn: Callable[..., T]) -> Callable[..., Task[T]]:
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            return self.dispatch(fn, *args, **kwargs)
        return wrapper
    
    def start(self):
        raise NotImplementedError("Must be derived in subclasses")
    
    def stop(self):
        with self._lock:
            self._terminate = True
            self._queue.close()
    
    def join(self):
        event = threading.Event()
        self._done_future.add_done_callback(lambda _: event.set())
        event.wait()
    
    def isrunning(self) -> bool:
        with self._lock:
            return self._thread is not None and self._thread.is_alive()
    
    def __await__(self):
        yield from self.awaitable().__await__()
    
    def awaitable(self) -> Awaitable:
        return asyncio.wrap_future(self._done_future)
    
    
    @property
    def exception(self) -> Optional[BaseException]:
        with self._lock:
            if not self._done_future.done():
                return None
            return self._done_future.exception()

class RebootContext(ContextBase):
    """A Context which terminates whenever whenever its queue is empty and reboots upon dispatching a new task.
    
    ## Fields
    - `initializer`: An initializer callback to run at the creation of the context's background thread"""
    def __init__(self, task_wait_time: float = 0, initializer: Optional[Callable[[RebootContext], None]] = None, cleanup: Optional[Callable[[RebootContext], None]] = None, **kwargs):
        super().__init__(**kwargs)
        self.initializer = initializer
        self.cleanup = cleanup
        self.task_wait_time = task_wait_time
    
    def dispatch(self, task: Callable[..., T], *args, **kwargs) -> Awaitable[T]:
        ret = Task(task, args, kwargs)
        self._queue.push(ret)
        self._launch()
        return ret
    
    def start(self) -> RebootContext:
        return self
    
    def _launch(self):
        with self._lock:
            if not self.isrunning():
                self._terminate = False
                self._done_future = CFuture()
                self._thread = Thread(target=self._loop)
                self._thread.start()
                return self
    
    def _loop(self):
        if self._terminate:
            self._done_future.set_exception(InvalidStateError("Context terminated"))
            return
        
        if self.initializer:
            try:
                self.initializer(self)
            except BaseException as ex:
                self._terminate = True
                self._done_future.set_exception(ex)
                return
        
        while True:
            try:
                task = self._queue.pop(self.task_wait_time)
                if task:
                    task.execute()
                else:
                    break
            except CancellationError:
                break
        self._terminate = True
        
        if self.cleanup:
            try:
                self.cleanup(self)
            except BaseException as ex:
                self._done_future.set_exception(ex)
                return
        self._done_future.set_result(True)
    
    @property
    def exception(self) -> BaseException:
        with self._lock:
            if not self._done_future.done():
                return None
            return self._done_future.exception()

class PersistentContext(ContextBase):
    """A Context which requires explicit termination. This type of context is necessary for IO resources which cannot
    be shared across threads (such as sqlite3 objects in a default CPython installation) and where reopening the
    resource could add too much overhead."""
    def __init__(self, initializer: Optional[Callable[[PersistentContext], None]] = None, cleanup: Optional[Callable[[PersistentContext], None]] = None, **kwargs):
        super().__init__(**kwargs)
        self.initializer = initializer
        self.cleanup = cleanup
    
    def start(self) -> PersistentContext:
        with self._lock:
            if self._thread:
                raise InvalidStateError('PersistentContext already started')
            self._thread = Thread(target=self._loop)
            self._thread.start()
            return self
    
    def reset(self) -> PersistentContext:
        with self._lock:
            if self.isrunning():
                raise InvalidStateError('Background thread still running')
            self._thread = Thread(target=self._loop)
            self._done_future = CFuture()
            self._queue = TaskQueue()
            self._terminate = False
            self._thread.start()
            return self
    
    def _loop(self):
        if self._terminate:
            self._done_future.set_exception(InvalidStateError("Context terminated"))
            return
        
        if self.initializer:
            try:
                self.initializer(self)
            except BaseException as ex:
                self._terminate = True
                self._done_future.set_exception(ex)
                return
        
        while not self._terminate:
            try:
                task = self._queue.pop()
                if task:
                    task.execute()
            except CancellationError:
                break
        
        if self.cleanup:
            try:
                self.cleanup(self)
            except BaseException as ex:
                self._done_future.set_exception(ex)
                return
        self._done_future.set_result(True)
    
    
    def __enter__(self):
        return self.start()
    
    def __exit__(self, ex_t, ex_v, ex_tp):
        self.stop()
    
    
    @property
    def exception(self) -> BaseException:
        with self._lock:
            if not self._done_future.done():
                return None
            return self._done_future.exception()


class TaskQueue:
    def __init__(self):
        self.tasks: List[Task] = []
        self.notif = Condition()
        self._closed = False
    
    def push(self, task: Task):
        with self.notif:
            if self._closed:
                raise InvalidStateError('already closed')
            self.tasks.append(task)
            self.notif.notify_all()
    
    def pop(self, timeout: Optional[float] = None) -> Optional[Task]:
        with self.notif:
            self.notif.wait_for(lambda: not isempty(self.tasks) or self._closed, timeout=timeout)
            if self._closed:
                raise CancellationError()
            if isempty(self.tasks):
                return None
            return shift(self.tasks)
    
    def close(self):
        with self.notif:
            self._closed = True
            self.tasks = []
            self.notif.notify_all()
    
    def __len__(self):
        return len(self.tasks)

class Task(Generic[T]):
    def __init__(self, cb: Callable[..., T], args: Sequence, kwargs: Dict[str, Any]):
        self.future = CFuture()
        self.cb     = cb
        self.args   = args
        self.kwargs = kwargs
    
    def execute(self):
        if not self.future.cancelled():
            try:
                self.future.set_result(self.cb(*self.args, **self.kwargs))
            except BaseException as ex:
                self.future.set_exception(ex)
    
    def cancel(self):
        self.future.cancel()
    
    def __await__(self):
        awaitable = self.awaitable()
        yield from awaitable
        return awaitable.result()
    
    def awaitable(self) -> asyncio.Future:
        return asyncio.wrap_future(self.future)
    
    def join(self, timeout: Union[int, float, None] = None, reraise: bool = False):
        if self.future.done():
            return
        try:
            self.future.result(timeout)
        except:
            if reraise:
                raise
    
    def result(self, timeout: Union[int, float, None] = None):
        return self.future.result(timeout)
    
    def exception(self, timeout: Union[int, float, None] = None):
        return self.future.exception(timeout)


Context = TypeVar('Context', bound=ContextBase)
