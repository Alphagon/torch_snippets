# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/misc.ipynb.

# %% auto 0
__all__ = ['Timer', 'track2', 'summarize_input', 'timeit', 'io', 'tryy']

# %% ../nbs/misc.ipynb 2
import time
from .logger import Debug, Excep, debug_mode
from .markup2 import AD
from functools import wraps
from fastcore.basics import ifnone

# %% ../nbs/misc.ipynb 3
class Timer:
    def __init__(self, N, smooth=True, mode=1):
        "print elapsed time every iteration and print out remaining time"
        "assumes this timer is called exactly N times or less"
        self.tok = self.start = time.time()
        self.N = N
        self.ix = 0
        self.smooth = smooth
        self.mode = mode
        # 0 = instant-speed, i.e., time remaining is a funciton of only the last iteration
        # Useful when you know that each loop takes unequal time (increasing/decreasing speeds)
        # 1 = average, i.e., time remaining is a function of average of all iterations
        # Usefule when you know on average each loop or a group of loops take around the same time

    def __call__(self, ix=None, info=None):
        ix = self.ix if ix is None else ix
        info = "" if info is None else f"{info}\t"
        tik = time.time()
        elapsed = tik - self.start

        if self.mode == 0:
            ielapsed = tik - self.tok
            ispeed = ielapsed
            iremaining = (self.N - (ix + 1)) * ispeed

            iunit = "s/iter"
            if ispeed < 1:
                ispeed = 1 / ispeed
                iunit = "iters/s"
            iestimate = iremaining + elapsed
            _info = f"{info}{ix+1}/{self.N} ({elapsed:.2f}s - {iremaining:.2f}s remaining - {ispeed:.2f} {iunit})"

        else:
            speed = elapsed / (ix + 1)
            remaining = (self.N - (ix + 1)) * speed
            unit = "s/iter"
            if speed < 1:
                speed = 1 / speed
                unit = "iters/s"
            estimate = remaining + elapsed
            # print(f'N={self.N} e={elapsed:.2f} _rem={self.N-(ix+1)} r={remaining:.2f} s={speed:.2f}\t\t')
            _info = f"{info}{ix+1}/{self.N} ({elapsed:.2f}s - {remaining:.2f}s remaining - {speed:.2f} {unit})"

        print(
            _info + " " * 10,
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
def summarize_input(args, kwargs, outputs=None):
    o = AD(args, kwargs)
    if outputs is not None:
        o.outputs = outputs
    return o.summary()


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
        info = f"""
{time.time() - s:.2f} seconds to execute `{func.__name__}`
{summarize_input(args=args, kwargs=kwargs, outputs=o)}
        """
        Debug(info, depth=1)
        return o

    return inner

# %% ../nbs/misc.ipynb 12
def tryy(func=None, *, output_to_return_on_fail=None, print_traceback=False):
    def decorator(f):
        def inner(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                if not print_traceback:
                    tb = str(e)
                else:
                    import traceback

                    tb = traceback.format_exc()
                Excep(
                    f"Error for `{f.__name__}` with \n{summarize_input(args, kwargs)}\n{tb}"
                )
                return output_to_return_on_fail

        return inner

    if callable(func):
        return decorator(func)
    return decorator
