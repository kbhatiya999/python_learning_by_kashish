import asyncio
import contextvars
from contextlib import contextmanager
from threading import Thread

x = contextvars.ContextVar('x', default='NO_VALUE')
x.set([1, 2, 3])
print(x.get())

@contextmanager
def context_manager_func():
    print('inside cm')
    yield
    print('after yield')

# with context_manager_func() as cm:
#     x.set([4, 5, 6])
#     print(x.get())
#
# print(x.get())

def task(x):
    print('inside task')
    # x.set([7, 8, 9])
    print(x.get())

t = Thread(target=task, args=(x,))
t.start()

t.join()

print(x.get())

async def task(x):
    print('inside atask')
    # x.set([7, 8, 9])
    print(x.get())

asyncio.run(task(x))

