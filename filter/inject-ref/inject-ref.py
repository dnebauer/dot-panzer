#!/usr/bin/env python3

from importlib import import_module
from pandocinject import Injector
from pandocfilters import toJSONFilter

if __name__ == "__main__":
    SELECTOR = import_module('selector')
    FORMATTER = import_module('formatter')
    INJECTOR = Injector('inject-ref',
                        selector_module=SELECTOR,
                        formatter_module=FORMATTER)
    toJSONFilter(INJECTOR.get_filter())
