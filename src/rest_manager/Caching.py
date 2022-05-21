def memoize(ttl = 100):
    def memoizer(func):
        cache = dict()

        def memoized_func(*args):
            if args in cache:
                memoized_func.cache_info["hits"] += 1
                if memoized_func.cache_info["hits"] == memoized_func.cache_info["ttl"]: memoized_func.cache_clear()
                return cache[args]
            result = func(*args)
            cache[args] = result
            return result

        def clear_cache():
            cache = dict()

        memoized_func.cache_clear = clear_cache
        memoized_func.cache_info = {"hits": 0, "ttl": ttl}

        return memoized_func
    return memoizer