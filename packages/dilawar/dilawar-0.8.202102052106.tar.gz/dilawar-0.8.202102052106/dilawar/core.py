__author__ = "Dilawar Singh"
__email__ = "dilawar.s.rajput@gmail.com"

import math
import pickle
from pathlib import Path
import typing as T
import functools

from dilawar.logger import logger


def argmax(ls: list) -> int:
    """argmax: Returns the index i such that max(ls) == ls[i]"""
    _m, _mi = -math.inf, 0
    for i, v in enumerate(ls):
        if v > _m:
            _m = v
            _mi = i
    return _mi


def write_pickle(pklfile: Path, obj: T.Any):
    """Write pickle.

    Parameters
    ----------
    pklfile : Path
        pklfile
    obj : T.Any
        obj
    """
    with pklfile.open("wb") as f:
        pickle.dump(f, obj)

def load_pickle(pklfile: Path):
    """Write pickle.

    Parameters
    ----------
    pklfile : Path
        pklfile
    obj : T.Any
        obj
    """
    with pklfile.open("rb") as f:
        return pickle.load(f)


def run_if_not_pickled(pklfile: T.Union[str, Path]):
    def inner_decorator(func):
        @functools.wraps(func)
        def __inner(*args, **kwargs):
            p = Path(pklfile).resolve()
            if p.exists():
                try:
                    return load_pickle(p)
                except Exception as e:
                    logger.warning(f'Failed to load {p}/{e}')
                    p.unlink()

            x = func(*args, **kwargs)
            with p.open("wb") as f:
                pickle.dump(x, f)
            return x

        return __inner

    return inner_decorator

def flatten(listoflist : T.List[T.List[T.Any]]) -> T.List[T.Any]:
    import operator
    return functools.reduce(operator.iconcat, listoflist, [])

def test_argmax():
    import random

    a = [random.randint(-1000, 1000) for x in range(1000)]
    assert max(a) == a[argmax(a)]


@run_if_not_pickled("a.pickle")
def test_func_pickle():
    import numpy as np

    d = np.random.randint(0, 1000, 1000)
    return d

def test_flatten():
    a = [[1,1,1], [2], [[3], [-1]]]
    x = flatten(a)
    assert x == [1, 1, 1, 2, [3], [-1]]
    a = [[1], [2], [3]]
    x = flatten(a)
    assert x == [1, 2, 3]


def main():
    a = test_func_pickle()
    print(a.shape)
    test_flatten()


if __name__ == "__main__":
    main()
