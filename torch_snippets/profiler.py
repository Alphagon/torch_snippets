import cProfile
import pstats
from io import StringIO


def time_profiler(filename='profiling_results.txt'):
    # The outer function that allows customization of the filename
    def decorator(func):
        # The middle function which receives the function to be wrapped
        def wrapper(*args, **kwargs):
            # The inner function that actually runs the profiling
            profiler = cProfile.Profile()
            profiler.enable() # Start profiling
            result = func(*args, **kwargs)
            profiler.disable() # End profiling
            # Create a StringIO stream to capture profiling results
            s = StringIO()
            ps = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
            ps.print_stats()
            # Write the profiling results to the specified file
            with open(filename, 'w') as f:
                f.write(s.getvalue())
            return result
        return wrapper
    return decorator