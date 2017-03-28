# -*- coding: utf-8 -*-
import atexit
import os
import time
from functools import wraps

PROFILE_TYPE = os.getenv('WEB_PROFILER')

try:
    # If we want to profile the time with line profiler
    if PROFILE_TYPE == 'time':
        from line_profiler import LineProfiler
        profile = LineProfiler()

        def report():
            profile.print_stats(stripzeros=True)

        atexit.register(report)

    elif PROFILE_TYPE == 'basic_time':
        from qualname import qualname

        def profile(f):

            @wraps(f)
            def wrapped(*args, **kwargs):
                before = time.time()
                try:
                    return f(*args, **kwargs)
                finally:
                    stop = time.time()
                    print("{} +{:f} ".format(qualname(f), (stop - before) * 1000))

            return wrapped

    elif PROFILE_TYPE == 'memory':
        from memory_profiler import LineProfiler, show_results
        profile = LineProfiler()

        def report():
            print("Show results!")
            show_results(profile)

        atexit.register(report)


    # Fallback on doing noting
    else:
        def profile(function):
            # NOOP
            return function
except Exception:
    import traceback
    traceback.print_exc()

    def profile(function):
        # NOOP
        return function
