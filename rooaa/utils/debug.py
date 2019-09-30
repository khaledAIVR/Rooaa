import time


def performance(func):
    """Simple timing decorator for performance testing"""

    def count_performance(*args, **kwargs):
        t1 = time.perf_counter()
        result = func(*args, **kwargs)
        t2 = time.perf_counter()

        print("------------")
        print(f"{func.__name__}: Time taken {t2-t1:.2}s")
        return result

    return count_performance
