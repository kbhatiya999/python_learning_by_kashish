from functools import partial


def abc (x,y,z):
    print(x,y,z)

p = partial(abc, z=11)

p(9,8)