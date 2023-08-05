''''report time.
see also from linetimer import CodeTimer
'''

import contextlib
from time import perf_counter

from .with_func_attrs import with_func_attrs

@with_func_attrs(time_elapsed=0)
@contextlib.contextmanager
def report_time(test=''):
    ''' report time.

    if test='' (default), just set report_time.time_elapsed, not print

    print only when test is True
    '''
    # then = time()
    then = perf_counter()
    yield
    time_elapsed = float(f'{perf_counter() - then:.6f}')
    if test:
        print("Time needed for `%s': %.4fs" % (test, time_elapsed))
    report_time.time_elapsed = time_elapsed
