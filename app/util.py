import os
import calendar
import uuid as _uuid

from datetime import datetime, timedelta
from collections import OrderedDict


def now(as_timestamp=False, in_millis=False):
    """Returns a datetime object with
    the current UTC time. The datetime
    does not include timezone information"""

    time = datetime.utcnow()
    if as_timestamp:
        timestamp = calendar.timegm(time.utctimetuple())
        if in_millis:
            return timestamp * 1000
        return timestamp
    return time


def secret(size=16):
    return os.urandom(size).encode('hex')


def uuid():
    return str(_uuid.uuid4()).replace('-', '')


class NamedTuple(tuple):
    """
    Defines a NamedTuple (tuple with names for objects) according to the
    definition in the gist https://gist.github.com/bennoleslie/27aeb9065e81199f8af1

    The main difference in this version is that objects that inherit from NamedTuple here
    can be treated as tuples and mappings, therefore the functions dict() and tuple() can
    be invoked on instances. This makes the object particularly useful to be used as constants
    """

    __slots__ = ()

    _fields = None  # Subclass must provide this

    def __new__(_cls, *args, **kwargs):
        if len(args) > len(_cls._fields):
            raise TypeError("__new__ takes {} positional arguments but {} were given".format(len(_cls._fields) + 1, len(args) + 1))

        missing_args = tuple(fld for fld in _cls._fields[len(args):] if fld not in kwargs)
        if len(missing_args):
            raise TypeError("__new__ missing {} required positional arguments".format(len(missing_args)))
        extra_args = tuple(kwargs.pop(fld) for fld in _cls._fields[len(args):] if fld in kwargs)
        if len(kwargs) > 0:
            raise TypeError("__new__ got an unexpected keyword argument '{}'".format(list(kwargs.keys())[0]))

        return tuple.__new__(_cls, tuple(args + extra_args))

    def _make(self, iterable, new=tuple.__new__, len=len):
        'Make a new Bar object from a sequence or iterable'
        cls = self.__class__
        result = new(cls, iterable)
        if len(result) != len(cls._fields):
            raise TypeError('Expected {} arguments, got {}'.format(len(self._fields), len(result)))
        return result

    def __repr__(self):
        'Return a nicely formatted representation string'
        fmt = '(' + ', '.join('%s=%%r' % x for x in self._fields) + ')'
        return self.__class__.__name__ + fmt % self

    def _asdict(self):
        'Return a new OrderedDict which maps field names to their values'
        return OrderedDict(zip(self._fields, self))

    __dict__ = property(_asdict)

    def _replace(_self, **kwds):
        'Return a new Bar object replacing specified fields with new values'
        result = _self._make(map(kwds.pop, _self._fields, _self))
        if kwds:
            raise ValueError('Got unexpected field names: %r' % list(kwds))
        return result

    def __getnewargs__(self):
        'Return self as a plain tuple.  Used by copy and pickle.'
        return tuple(self)

    def __getstate__(self):
        'Exclude the OrderedDict from pickling'
        return None

    def __getattr__(self, field):
        try:
            idx = self._fields.index(field)
        except ValueError:
            raise AttributeError("'{}' NamedTuple has no attribute '{}'".format(self.__class__.__name__, field))

        for i, v in zip(range(len(self)), self):
            if i == idx:
                return v

    def __getitem__(self, key):
        try:
            idx = self._fields.index(key)
        except ValueError:
            raise AttributeError("'{}' NamedTuple has no attribute '{}'".format(self.__class__.__name__, key))

        for i, v in zip(range(len(self)), self):
            if i == idx:
                return v

    def keys(self):
        return self._fields


def enum(*sequential, **kwargs):
    """Define an iterable enum"""
    class Enum(NamedTuple):
        __slots__ = ()
        _fields = tuple(v for l in [sequential, kwargs.keys()] for v in l)

    return Enum(*[v for l in [range(len(sequential)), kwargs.values()] for v in l])
