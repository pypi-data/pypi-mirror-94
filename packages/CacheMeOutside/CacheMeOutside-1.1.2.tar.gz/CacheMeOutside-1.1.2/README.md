# CacheMeOutside - A simple (optionally) persistent caching decorator.
This decorator can be very useful when you have a pure function (always gives the same result when called with no side-effects) which is hard to compute.

It works on functions of just about any signature because it uses python's amazing `*args` and `**kwargs` convention to directly pass through all arguments.

In its simplest form, its usage looks like this:
```python
from cacheMeOutside import cacheMe
import time

@cacheMe()
def someCostlyFunction(a,b):
    time.sleep(1)
    print(f"This only shows up on the first call with these args: {a,b}!")
    return a + b
```

Although initial calls to the above function would take 1 second, repeated calls will return immediately because their results have been cached. It is important to note that **side-effects such as printing will not be repeated!**

You can also pass in a `filename` in order to persistently cache calls to this function across multiple python interpreter invocations. By default this filename refers to a file under the directory `__cmoCache__` beneath where python was called from, but you can change this by passing a `cacheDir` argument. Another optional argument is `maxEntries` (defaults to 1 million) where you can specify an upper-limit on the number of entries that can be simultaneously be stored in the cache. When you run out of entries, the least recently used ones are removed first. You can also pass the argument `invalidationStride` (defaults to 1) in order to invalidate a different number of cache entries when you run out. In the following example, the 5 least recently used entries are removed once you reach 50 entries.
```python
@cacheMe(
    "cache_filename_goes_here", 
    cacheDir="my_custom_cache_directory", 
    maxEntries=50, 
    invalidationStride=5
)
```

We monkey-patch the cache object into the function. This allows you to manually invalidate cache entries like so:
```python
someCostlyFunction.cmoCache.invalidateLRU(5)

# or for an arbitrary call to someCostlyFunction:
someCostlyFunction(1,2)
someCostlyFunction.cmoCache.invalidateCall(1,2)
```

If you have any questions, just look at the code for it. It's all one python file that's about 150 lines of code!