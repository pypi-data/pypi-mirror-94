# PyThreadSwitch
Python microlibrary to run arbitrary tasks in contexts associated with a single thread.

**CAVEAT:** This library is currently not well tested and requires unit tests for many more different scenarios. Any
contribution would be greatly appreciated.

# Installation
Simply install using `pip install threadswitch`.

# Usage
ThreadSwitch currently implements two kinds of thread contexts:

## PersistentContext
A context associated with a background thread which must be manually closed. This context is best suited for system
resources which are restricted to the same thread, such as OpenGL and SQLite3 objects (in a standard CPython installation).
While it provides `start`, `stop`, and `reset` methods to manage thread lifetime, it is recommended to use it with a
context manager (i.e. the `with` keyword).

Example
-------
```python
from threadswitch import PersistentContext
import sqlite3

def init_sqlite_ctx(ctx: PersistentContext):
    ctx.db = sqlite3.connect('my.db')

def clean_sqlite_ctx(ctx: PersistentContext):
    ctx.db.close()

with PersistentContext() as ctx:
    @ctx.task
    def execute(sql, params):
        ctx.db.execute(sql, params)
    
    # Note: As sqlite3.Cursor objects are also thread-bound, operating on one requires a more complex proxy wrapper.
    # This is skipped in this simple example usage.
    
    execute('DROP TABLE foobar').join()
```

## RebootContext
A context which automatically terminates its background thread once it's processed its pending task queue. This is
useful to simply synchronize access to a common system resource, such as the CLI. When closed, dispatching a new task
will automatically restart the background thread.

The thread can be kept alive past the completion of the queue. This is useful to avoid unnecessary thread creation and
termination overhead in a slowly paced environment. It is recommended to use a timeout of a fraction of a second in
general.

Example
-------
```python
from threadswitch import RebootContext
from sys import stdout, stdin

ctx = RebootContext(task_wait_time=.1)
writeline = ctx.task(stdout.writeline)
readline  = ctx.task(stdin.readline)

writeline('foobar')
value = readline().result()
```

## Common
The above sections outline the differences between the two currently implemented context types, but they share various
common behaviors.

### Tasks
As seen in the above examples, one may use `ctx.task` to create a new dispatchable task. Internally, this simply creates
a wrapper function which calls `ctx.dispatch(*args, **kwargs)` upon invocation. They can be used in two different styles:
threaded and asyncio styles.

The `ctx.task` method can also be used as a decorator as follows:

```python
from threadswitch import RebootContext
from sys import stdin

ctx = RebootContext(0.5)
@ctx.task
def read(n: int = -1):
    if n == -1:
        return stdin.readline()
    return stdin.read(n)
read().result()
```

#### Threaded Style
The examples above use "threaded usage style." This style uses `join`, `result`, and `exception` methods on the task
objects returned by dispatched tasks to synchronize threads. `join` simply waits until the task completes either by
returning a result value, or by raising an exception. `result` retrieves the return value of the task, and `exception`
retrieves any occurred exception encountered during the task if applicable. If the task is incomplete, implicitly `join`s.

All of these methods support a `timeout` argument which may be either `None` or a number in seconds.

#### AsyncIO Style
Alternatively, one may simply `await` any dispatched task. This behaves as one would expect from any other `await` call:
If the task was successful, retrieves the result value. If the task encountered an exception, raises the exception in
this thread. As this syntax does not support a timeout, one may alternatively use `await asyncio.wait_for(..., timeout=...)`.


# License
MIT License

Copyright (c) 2021 Kiruse

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
