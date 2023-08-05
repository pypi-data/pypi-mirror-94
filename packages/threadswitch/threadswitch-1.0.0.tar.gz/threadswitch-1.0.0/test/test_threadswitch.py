# ThreadSwitch Unit Test
# Copyright (c) Kiruse 2021. See license in LICENSE.
# TODO: Test thread-bound resources simulating libraries and interfaces like sqlite3
from __future__ import annotations
from threading import Thread
from threadswitch import *
from time import sleep, time
from typing import *
import pytest

class StringBuffer:
    def __init__(self, initial: str = ''):
        self.value = initial
    
    def write(self, msg: str):
        self.value += msg
        return self
    
    def writeline(self, msg: str):
        return self.write(msg + '\n')
    
    def read(self, n: int = -1) -> str:
        if n < 0:
            ret, self.value = self.value, ''
            return ret
        ret, self.value = self.value[:n], self.value[n:]
        return ret
    
    def readline(self) -> str:
        return self.read()
    
    def clear(self) -> StringBuffer:
        self.value = ''
        return self

class WrappedThread:
    def __init__(self, target: Callable):
        def cbwrap():
            self.result = target()
        self.thread = Thread(target=cbwrap)
        self.task: Optional[Task] = None
        self.result = None
    
    def start(self) -> WrappedThread:
        self.thread.start()
        return self
    
    def join(self):
        self.thread.join()
        if self.task:
            self.task.join()
    
    @staticmethod
    def wrap(*cbs: Callable):
        return WrappedThreadCollection([WrappedThread(target=cb) for cb in cbs])

class WrappedThreadCollection:
    def __init__(self, threads: Sequence[WrappedThread]):
        self.threads = threads
    
    def startall(self) -> WrappedThreadCollection:
        for thread in self.threads:
            thread.start()
        return self
    
    def joinall(self) -> WrappedThreadCollection:
        for thread in self.threads:
            thread.join()
        return self
    
    def __getitem__(self, idx: int) -> WrappedThread:
        return self.threads[idx]

class TestPersistentContext:
    def test_threaded(self):
        with PersistentContext() as ctx:
            buff.clear()
            read  = ctx.task(buff.read)
            write = ctx.task(buff.write)
            impl_threaded_textio(read, write)
    
    @pytest.mark.asyncio
    async def test_asyncio(self):
        with PersistentContext() as ctx:
            buff.clear()
            read  = ctx.task(buff.read)
            write = ctx.task(buff.write)
            
            write('420')
            write(' 69')
            await write('\n')
            assert buff.value == '420 69\n'
            
            assert await read(3) == '420'
            assert await read(4) == ' 69\n'

class TestRebootContext:
    def test_threaded(self):
        buff.clear()
        ctx = RebootContext(.5)
        read  = ctx.task(buff.read)
        write = ctx.task(buff.write)
        impl_threaded_textio(read, write)
    
    @pytest.mark.asyncio
    async def test_asyncio(self):
        buff.clear()
        ctx = RebootContext(.5)
        read  = ctx.task(buff.read)
        write = ctx.task(buff.write)
        
        write('420')
        write(' 69')
        await write('\n')
        assert buff.value == '420 69\n'
        
        assert await read(3) == '420'
        assert await read(4) == ' 69\n'
    
    def test_reboot(self):
        buff.clear()
        ctx = RebootContext(.5)
        read  = ctx.task(buff.read)
        write = ctx.task(buff.write)
        
        write('420').join()
        assert ctx.isrunning()
        sleep(.6)
        assert not ctx.isrunning()
        write(' 69\n').join()
        assert ctx.isrunning()
        
        sleep(.1)
        assert ctx.isrunning()
        assert read(3).result() == '420'
        sleep(.6)
        assert not ctx.isrunning()
        assert read(4).result() == ' 69\n'
        assert ctx.isrunning()

def impl_threaded_textio(read: Callable[[int], Task[str]], write: Callable[[str], Task]):
    t0 = time()
            
    def writer1():
        sleep(.1)
        write("420").join()
    def writer2():
        sleep(.2)
        write(" 69").join()
    def writer3():
        sleep(.3)
        write('\n').join()
    
    threads = WrappedThread.wrap(writer1, writer2, writer3).startall()
    dt1 = time()-t0
    assert dt1 < 0.1
    
    threads.joinall()
    dt2 = time()-t0
    assert dt1<dt2-dt1*0.9 # Should take considerably longer
    
    assert buff.value == "420 69\n"
    
    def reader1():
        sleep(.1)
        return read(3).result()
    def reader2():
        sleep(.2)
        return read(4).result()
    
    t0 = time()
    threads = WrappedThread.wrap(reader1, reader2).startall()
    dt1 = time()-t0
    assert dt1 < 0.1
    
    threads.joinall()
    dt2 = time()-t0
    assert dt1<dt2-dt1*0.9 # Should take considerably longer
    
    assert threads[0].result == '420'
    assert threads[1].result == ' 69\n'

buff = StringBuffer()