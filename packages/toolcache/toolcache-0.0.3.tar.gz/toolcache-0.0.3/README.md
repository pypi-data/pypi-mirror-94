
# toolcache

`toolcache` makes it easy to create and configure caches in python

## Features
- save caches to memory or to disk
- memoize functions, instance methods, `@classmethod`s, and `@staticmethod`s
- control cache size with ttl and eviction policies like lru / fifo / lfu
- use thread safety, process safety, or no safety (default = thread safety)
- use custom hash functions
- track cache usage statistics

## Install
`pip install toolcache`

## Contents
- [Example Usage](#example-usage)
- [Reference](#cache-reference)
    - [Cache Types](#cache-types)
    - [Cache Creation](#cache-creation)
    - [Cache Configuration](#cache-configuration)
    - [Cache Decorators](#cache-decorators)
    - [Cache Methods](#cache-methods)
- [Frequently Asked Questions](#frequently-asked-questions)

## Example Usage

### Creating Caches
```python
import toolcache

# memoize function with memory cache
@toolcache.cache('memory')
def f(a, b, c):
    return a * b * c

# memoize function with disk cache, stored in a tempdir
@toolcache.cache('disk')
def f(a, b, c):
    return a * b * c

# memoize function with disk cache, stored in a persistent dir
@toolcache.cache('disk', cache_dir='/path/to/cache/dir')
def f(a, b, c):
    return a * b * c
    
# remove cache entries once they reach a specific age
@toolcache.cache('disk', ttl='24 hours')
def f(a, b, c):
    return a * b * c

# remove cache entries once cache reaches a specific size
@toolcache.cache('disk', max_size=3, max_size_policy='fifo')
def f(a, b, c):
    return a * b * c

# specify which args are used to create unique hash of inputs
@toolcache.cache('disk', hash_args=['a', 'b'])
def f(a, b, c):
    return a * b * c

# create standalone cache
standalone_cache = toolcache.MemoryCache()
```

### Using Caches

```python
# get cache size
print(f.cache.get_cache_size())
> 4

# track cache usage statistics
print(f.cache.stats)
> {'n_checks': 6,
>  'n_deletes': 2,
>  'n_hashes': 8,
>  'n_hits': 2,
>  'n_loads': 1,
>  'n_misses': 4,
>  'n_saves': 3,
>  'n_size_evictions': 0,
>  'n_ttl_evictions': 0}

# clear cache
f.cache.delete_all_entries()
```

### More Examples
- [Cache Eviction Policies](examples/cache_eviction_policies.py)
- [Define Custom Cache](examples/define_custom_cache.py)
- [Disk Cache Options](examples/disk_cache_options.py)
- [Function Hashing Options](examples/function_hashing_options.py)
- [Monitor Cache Usage](examples/monitor_cache_statistics.py)
- [Standalone Caches](examples/standalone_cache.py)

## Cache Reference

### Cache Types

`toolcache` includes 3 cache types that each inherit from abstract cache class `BaseCache`:

| cachetype     | description | use case |
| --            | -- | -- |
| `MemoryCache` | cache that saves each entry as key-value pair in a `dict` | speed |
| `DiskCache`   | cache that saves each entry as a file to disk | persistence, or large data that does not fit in memory |
| `NullCache`   | cache that does not save any entries | programmatically disabling cache |


### Cache Creation

Caches can be created in two ways:
1. decorating a function with `@toolcache.cache(cachetype)` where `cachetype` is `'memory'`, `'disk'`, `'null'`, or a class inheriting from `BaseCache`
2. creating a standalone cache by instantiating a class that inherits from `BaseCache`

### Cache Configuration

The configuration options listed below can be passed to `toolcache.cache()` or passed to a standalone cache during initialization.

#### Base Cache Config
these configuration options are available to every cache
| arg | description | example value | default behavior |
| --           | --          | --           | -- |
| `safety`     | `str` name of concurrency safety level, one of `'thread'`, `'process'`, or `None` | `'thread'`        | `'thread'` |
| `verbose`    | `bool` of whether to print info whenever saving to or loading from cache          | `False`           | `False` |
| `cache_name` | `bool` of whether to print info whenever saving to or loading from cache          | `'important_cache'` | use decorated function name, or uuid for  a standalone cache |

#### Hash Config
| arg | description | example value | default behavior |
| --           | --          | --           | -- |
| `f_hash`    | custom function for computing hash | `lambda x: hash(x)` | `toolcache. compute_hash_json()` |
| `normalize_hash_inputs`    | bool of whether to normalize function calls so that for a function `f` with args `a` and `b`, the calls `f(1, 2)` and `f(a=1, b=2)` are equivalent | `False` | `False` |
| `hash_include_args`    | `list` of `str` names of arguments used to compute hash | `['arg1', 'arg2']`       | include all args |
| `hash_exclude_args`    | `list` of `str` names of arguments excluded from hash | `['arg3', 'arg4']`       | exclude no args |

#### Eviction Config
| arg | description | example value | default behavior |
| --                | --          | --           | -- |
| `ttl`             | [`Timelength`](https://github.com/sslivkoff/tooltime) of time-to-live maximum age for entries in cache | `'1000s'`     | `float('inf')` |
| `max_size`        | `int` of max size of cache size | `1000`     | no max size |
| `max_size_policy` | `str` name of eviction policy to use when `max_size` is exceeded, one of `'lru'`, `'fifo'`, or `'lfu'`  | `'fifo'`    | `'lru'' |

#### Statistic Tracking Config
| arg | description | example value | default behavior |
| --                | --          | --           | -- |
| `track_basic_stats` | `bool` of whether to track basic usage stats | `False` | `False` |
| `track_detailed_stats` | `bool` of whether to track creations and accesses | `False` | `False` |
| `track_creation_times` | `bool` of whether to track creation times | `False` | track only if `ttl` is not `None` or `max_size_policy == 'fifo'` |
| `track_access_times` | `bool` of whether to track access times | `False` | track only if `max_size_policy == 'lru'` |
| `track_access_counts` | `bool` of whether to track access counts | `False` |  track only if `max_size_policy == 'lfu'` |

#### `DiskCache`-specific Config
| arg | description | example value | default behavior |
| --            | --                                                                                                       | --                     | --                |
| `cache_dir`   | `str` of directory path to store cache data                                                              | `'/path/to/cache_dir'` | create a `tmpdir` |
| `file_format` | `str` of file format to use for cache data, either `'pickle'` or `'json'`                                | `'json'`               | `'pickle'`        |
| `f_disk_save` | custom function for saving data to disk, function should take `entry_path` and `entry_data` as arguments | `f_save` | save as pickle  |
| `f_disk_load` | custom function for load data from disk, function should take `entry_path` as an argument                | `f_load` | load as pickle |


### Cache Decorators

When using `toolcache.cache()` to decorate a function, one should consider 1) how function inputs will be hashed, 2) what attributes will be added to the function, and 3) what arguments might be added to the function.

#### Hashing Function Inputs

To save a function input-output pair within a cache, a unique hash must be taken of the inputs.

Under the default hash configuration, each input arg should either be json-serializable or be a hashable object (i.e. it implements a `__hash__()` method). By default `toolcache` uses [`orjson`](https://github.com/ijl/orjson) to create these hashes quickly.

If function inputs do not satisfy these criteria, one or more of the cache config parameters should be used:
| parameter | description | example |
| -- | -- | --      |
| `f_hash` | provide a custom hash function that takes the same args and kwargs as the decorated function | `@toolcache.cache(..., f_hash=f_custom_hash)` |
| `hash_include_args` | specify `list` of arg names that should be used to compute hash | `@toolcache.cache(..., hash_include_args=['arg1', 'arg2'])` |
| `hash_exclude_args` | specify `list` of arg names that should not be used to compute hash | `@toolcache.cache(..., hash_exclude_args=['arg3', 'arg4'])` |

`toolcache.cache()` also works on functions that have `*args` or `**kwargs` for inputs

#### Decorated Function Args
Every time the decorated function is called, it can use the following keyword args to control cache behavior.
| kwarg           | description                                                           | default | example |
| --              | --                                                                    | --      | -- |
| `cache_save`    | `bool` of whether to save output to cache                             | `True`  | `f(..., cache_save=False)` will not save output to cache |
| `cache_load`    | `bool` of whether to attempt to load entry from cache                 | `True`  | `f(..., cache_load=False)` will not attempt to load entry from cache |
| `cache_verbose` | `bool` of whether to print info about loading from or saving to cache | `True`  | `f(..., cache_load=False)` will not attempt to load entry from cache |

You can avoid adding these args to the decorated function by using `@toolcache.cache(..., add_cache_args=False)`.

#### Decorated Function Attributes

The original decorated function can be acessed as `f.__wrapped__`.

The cache instance associated with a decorated function `f()` can be accessed using `f.cache`.

### Cache Methods

These methods are available on every cache instance:

| method | description |
| --     | -- |
| `compute_entry_hash()` | compute hash of entry |
| `save_entry()` | save entry data to cache |
| `exists_in_cache()` | return `bool` of whether entry exists in cache |
| `load_entry()` | load entry data from cache |
| `get_cache_size()` | return `int` number of items in cache |
| `delete_entry()` | remove entry from cache |
| `delete_all_entries()` | delete all entries from cache |


## Frequently Asked Questions

#### How is the performance? What is the overhead for using a cache decorator?

To maximize cache performance, one can disable input name normalization (`normalize_hash_inputs=False`), statistic tracking (`track_basic_stats=False` and `track_detailed_stats=False`), and thread safety (`safety=None`).

On a somewhat modern machine with the above settings, the `toolcache.cache()` decorator adds about 3 μs to each function call, whereas running a simple function with no cache decorator takes about 50 ns per function call. Using a disk cache instead of a memory cache adds about 25 μs per function call. To truly know whether `toolcache` is fast enough for your application you may need to run your own benchmarks.

#### How does `toolcache` relate to other similar projects?

A large motivation for developing `toolcache` was being able to manage memory-based and disk-based caches with a unified interface and feature set. `toolcache` is currently the only python package to offer this functionality.

There exist many other python packages for caching and memoization. [`cacheout`](https://github.com/dgilland/cacheout) and [`python-memoization`](https://github.com/lonelyenvoy/python-memoization) both provide in-memory caches with many features. Compared to `toolcache` these libraries provide a wider variety of cache eviction policies and other interesting features. [`python-diskcache`](https://github.com/grantjenks/python-diskcache/) provides a feature-rich disk-based cache with Django integration and extensive benchmark comparisons to other solutions.
