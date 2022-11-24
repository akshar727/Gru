from functools import wraps


def cache(maxsize=128):
    cache_dict = {}

    def decorator(func):
        @wraps(func)
        def inner(*args, no_cache=False, **kwargs):
            if no_cache:
                return func(*args, **kwargs)

            key_base = "_".join(str(x) for x in args)
            key_end = "_".join(f"{k}:{v}" for k, v in kwargs.items())
            key = f"{key_base}-{key_end}"

            if key in cache_dict:
                return cache_dict[key]

            res = func(*args, **kwargs)

            if len(cache_dict) > maxsize:
                del cache_dict[list(cache_dict.keys())[0]]
                cache_dict[key] = res

            return res
        return inner
    return decorator


def async_cache(maxsize=128):
    cache_dict = {}

    def decorator(func):
        @wraps(func)
        async def inner(*args, no_cache=False, **kwargs):
            if no_cache:
                return await func(*args, **kwargs)

            key_base = "_".join(str(x) for x in args)
            key_end = "_".join(f"{k}:{v}" for k, v in kwargs.items())
            key = f"{key_base}-{key_end}"

            if key in cache_dict:
                return cache_dict[key]

            res = await func(*args, **kwargs)

            if len(cache_dict) > maxsize:
                del cache_dict[list(cache_dict.keys())[0]]
                cache_dict[key] = res

            return res
        return inner
    return decorator
