# Copyright (c) 2018 Gabriele Baldoni, Artem Chirkin.
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0, or the Apache License, Version 2.0
# which is available at https://www.apache.org/licenses/LICENSE-2.0.
#
# SPDX-License-Identifier: Apache-2.0
#
# Contributors: Gabriele Baldoni, Artem Chirkin
'''Haskell-style MVars using threading primitives.'''
import contextlib
import threading
import typing

T = typing.TypeVar('T')


class MVar(typing.Generic[T]):
    '''
    Haskell-style MVars.

    At its core functionality are methods `take()`, `get()`, and `put()`,
    which closely reflect their haskell counterparts.

    This implementation also adds a few more methods which enable a more
    pythonic style of programming.
    In particular, `wait()` and `locked()` by supporting the context manager protocol
    allow you to perform atomic operations on the MVar using `with` syntax.
    Using `with` syntax on MVar itself is equivalent to using `locked()` without arguments.
    It is safe to nest `with` syntax on the same MVar (it uses a recursive lock).

    For most of the functions, the documentation indicates whether they are blocking or not;
    this refers to the underlying recursive lock.
    '''

    __lock: threading.RLock
    __condition: threading.Condition
    __full: bool
    __value: typing.Optional[T]

    def __init__(self):
        self.__lock = threading.RLock()
        self.__condition = threading.Condition(lock=self.__lock)
        self.__full = False
        self.__value = None

    def __enter__(self) -> typing.Tuple[bool, typing.Optional[T]]:
        self.__lock.__enter__()
        return (self.__full, self.__value)

    def __exit__(self, *args):
        return self.__lock.__exit__(*args)

    def is_full(self) -> bool:
        '''Whether the value is there (non-blocking)'''
        return self.__full

    def is_empty(self) -> bool:
        '''Inverse of 'is_full' (non-blocking)'''
        return not self.__full

    def get(self, timeout: typing.Optional[float] = None) -> T:
        '''
        Wait for the value and get it without emptying the MVar (blocking).
        Does not cause other waiting threads to wake up.
        '''
        with self.__lock:
            if not self.__condition.wait_for(self.is_full, timeout=timeout):
                raise TimeoutError('MVar.get: timeout')
            return self.__value

    def take(self, timeout: typing.Optional[float] = None) -> T:
        '''
        Wait for the value and take it (blocking).
        Empties the MVar and wakes up all waiting threads.
        '''
        with self.__lock:
            if not self.__condition.wait_for(self.is_full, timeout=timeout):
                raise TimeoutError('MVar.take: timeout')
            v = self.__value
            self.__value = None
            self.__full = False
            self.__condition.notify_all()
            return v

    def take_nowait(self) -> T:
        '''
        Try to take the value without waiting (blocking).
        Empties the MVar and wakes up all waiting threads if the MVar was full.
        Otherwise, throws the ValueError.
        '''
        with self.__lock:
            if self.is_empty():
                raise ValueError("MVar.take_nowait: empty")
            v = self.__value
            self.__value = None
            self.__full = False
            self.__condition.notify_all()
            return v

    def put(self, value: T, timeout: typing.Optional[float] = None) -> None:
        '''
        Wait for MVar to become empty and put a value in there (blocking).
        Wakes up all waiting threads.
        '''
        with self.__lock:
            if not self.__condition.wait_for(self.is_empty, timeout=timeout):
                raise TimeoutError('MVar.put: timeout')
            self.__value = value
            self.__full = True
            self.__condition.notify_all()

    @contextlib.contextmanager
    def wait(self, timeout: typing.Optional[float] = None) -> bool:
        '''
        Wait for any changes in the state, or for the timeout event (blocking).

        Returns whether it's awaken within the specified time.
        '''
        with self.__lock:
            yield self.__condition.wait(timeout=timeout)

    @contextlib.contextmanager
    def locked(self, timeout: typing.Optional[float] = None) -> typing.Tuple[bool, typing.Optional[T]]:
        '''
        Use the MVar's lock independently of the MVar's state.

        Returns a tuple (is_full, Optional[value]).

        Note, the type of the value `T` may itself be optional,
        that is why this method returns the tuple with the explicit indication of whether it's full.
        '''
        if self.__lock.acquire(True, **({'timeout': timeout} if timeout is not None else {})):
            try:
                yield (self.__full, self.__value)
            finally:
                self.__lock.release()
        else:
            raise TimeoutError('MVar.locked: timeout')

    def notify_all(self) -> None:
        '''Low-level function: wakeup all threads waiting for this MVar (blocking).'''
        with self.__lock:
            self.__condition.notify_all()
