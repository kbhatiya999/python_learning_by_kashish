import multiprocessing
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

import dummy
def abcd(a):
    print(dummy.x)



def mm():
    global dummy
    dummy.x =1000
    abcd(4)
    # with multiprocessing.Pool() as pool:
    with ProcessPoolExecutor() as executor:
        dummy.x=9000
        dummy.x = 90
        res = executor.submit(abcd, (1, 2))
        # pool.map(abcd, (1,2,), )

        print(res.result())


if __name__ == '__main__':
    mm()