from . import logger
log = logger.get(__name__)
from . import http
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


def run_command(fn, callback, *args, **kwargs):
    ''' Convenience function to run a command without the decorator. '''
    command(fn)(callback, *args, **kwargs)


@command
def get_package_list(callback):
    j = http.getJSON('http://sublime.wbond.net/repositories.json')
    return j["repositories"]
