'''
The MIT License

Copyright (c) Bo Lopker, http://blopker.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''
'''
Wrapper of the python logging module for Sublime Text plugins.
by @blopker
'''
import logging
from logging import StreamHandler, Formatter

log = False


def init(name, debug=True):
    ''' Initializes the named logger for the rest of this program's execution.
    All children loggers will assume this loggers's log level if theirs is not
    set. Suggestion: Put logger.init(__name__, debug) in the top __init__.py
    module of your package.'''

    global log

    if log:
        # Logger already initialized.
        return

    log = logging.getLogger(name)
    handler = StreamHandler()

    plugin_name = name.split('.')[0]

    if debug:
        log.setLevel(logging.DEBUG)
        handler.setFormatter(_getDebugFmt(plugin_name))
    else:
        log.setLevel(logging.INFO)
        handler.setFormatter(_getFmt(plugin_name))

    log.addHandler(handler)

    # Not shown if debug=False
    log.debug("Logger for %s initialized.", plugin_name)


def _getDebugFmt(name):
    fmt = '%(levelname)s:' + name + '.%(module)s:%(lineno)d: %(message)s'
    return Formatter(fmt=fmt)


def _getFmt(plugin_name):
    fmt = plugin_name + ': %(message)s'
    return Formatter(fmt=fmt)


def get(name):
    ''' Get a new named logger. Usually called like: logger.get(__name__).Short
    and sweet wrapper for getLogger method so you don't have to import two
    modules.'''
    return logging.getLogger(name)
