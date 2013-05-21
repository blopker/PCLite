from .lib import requests
from . import settings
from .lib.concurrent import futures

executor = futures.ThreadPoolExecutor(max_workers=10)

def command(fn):
    def wrap(*args, **kwargs):
        callback = args[0]
        def cb(fu):
            try:
                callback(fu.result())
            except Exception as e:
                raise e
        future = executor.submit(fn, *args, **kwargs)
        future.add_done_callback(cb)
    return wrap


@command
def get_package_list(callback):
    print("run")
    return ['bo', 'is', 'really, really', 'awesome']

