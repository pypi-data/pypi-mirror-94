# pyhton-mvar

[![PyPI version](https://badge.fury.io/py/mvar.svg)](https://badge.fury.io/py/mvar)
[![Build Status](https://travis-ci.com/gabrik/mvar-python.svg?branch=master)](https://travis-ci.com/gabrik/mvar-python)
[![codecov](https://codecov.io/gh/gabrik/mvar-python/branch/master/graph/badge.svg)](https://codecov.io/gh/gabrik/mvar-python)


A Pyhton port of Haskell's [Control.Concurrent.MVar](https://hackage.haskell.org/package/base/docs/Control-Concurrent-MVar.html).

This implementation blocks on get if the MVar is empty, and on put if the MVar is not empty.

A MVar is a mutable location which can either be empty, or contain a value.
The location can be written to and read from safely from multiple concurrent python threads.


### Installation

    pip3 install mvar

### Example

A brief example with 3 threads and one MVar is available in [example](example/example.py)


Copyright 2018 Gabriele Baldoni
