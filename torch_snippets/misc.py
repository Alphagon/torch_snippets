# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/misc.ipynb.

# %% auto 0
__all__ = ['Timer', 'track2', 'timeit', 'io']

# %% ../nbs/misc.ipynb 2
import time
from .logger import Debug
from .inspector import inspect
from fastcore.basics import ifnone

# %% ../nbs/misc.ipynb 3
class Timer:
    def __init__(self, N, smooth=True):
        "print elapsed time every iteration and print out remaining time"
        "assumes this timer is called exactly N times or less"
        self.tok = self.start = time.time()
        self.N = N
        self.ix = 0
        self.smooth = smooth

    def __call__(self, ix=None, info=None):
        ix = self.ix if ix is None else ix
        info = "" if info is None else f"{info}\t"
        tik = time.time()
        elapsed = tik - self.start
        ielapsed = tik - self.tok
        ispeed = ielapsed

        iunit = "s/iter"
        if ispeed < 1:
            ispeed = 1 / ispeed
            iunit = "iters/s"

        iremaining = (self.N - (ix + 1)) * ielapsed
        iestimate = iremaining + elapsed

        print(
            f"{info}{ix+1}/{self.N} ({elapsed:.2f}s - {iremaining:.2f}s remaining - {ispeed:.2f} {iunit})"
            + " " * 10,
            end="\r",
        )
        self.ix += 1
        self.tok = tik


def track2(iterable, *, total=None):
    try:
        total = ifnone(total, len(iterable))
    except:
        ...
    timer = Timer(total)
    for item in iterable:
        info = yield item
        timer(info=info)
        if info is not None:
            yield  # Just to ensure the send operation stops

# %% ../nbs/misc.ipynb 10
def timeit(func):
    def inner(*args, **kwargs):
        s = time.time()
        o = func(*args, **kwargs)
        Debug(f"{time.time() - s:.2f} seconds to execute `{func.__name__}`")
        return o

    return inner


def io(func):
    def inner(*args, **kwargs):
        s = time.time()
        o = func(*args, **kwargs)
        Debug(f"Args: {inspect(args)}\nKWargs: {inspect(kwargs)}\nOutput: {inspect(o)}")
        return o

    return inner
