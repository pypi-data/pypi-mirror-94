import hashlib
import os
import pickle


cache_root_dir = '.icache-root'


if not os.path.exists(cache_root_dir):
    os.makedirs(cache_root_dir)


def md5(s):
    m = hashlib.md5()
    m.update(s.encode('utf8'))
    return m.hexdigest()


def cache_key(f, *args, **kwargs):
    s = '%s-%s-%s' % (f.__name__, str(args), str(kwargs))
    return os.path.join(cache_root_dir, 'func-%s' % f.__name__, '%s.dump' % md5(s))


# @API
def cache(f):
    def wrap(*args, **kwargs):
        fn = cache_key(f, *args, **kwargs)
        # print('cache key: %s' % fn)
        if os.path.exists(fn):
            # print('loading cache')
            with open(fn, 'rb') as fr:
                cache = pickle.load(fr)
                if cache is not None:
                    return cache

        obj = f(*args, **kwargs)

        cache_dir = os.path.dirname(fn)
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        with open(fn, 'wb') as fw:
            pickle.dump(obj, fw)
        return obj

    return wrap


@cache
def add(a, b):
    return a + b


if __name__ == '__main__':
    print(add(3, 4))
    print(add(3, 4))
    print(add(8, 4))
    print(add(4, 8))
