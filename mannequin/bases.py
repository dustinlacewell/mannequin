from __future__ import print_function

import sys
import re
from itertools import chain

class Field(object):
    
    defaults = tuple()

    def __init__(self, **kwargs):
        self.__value = None
        for (defname, defvalue) in self.defaults:
            if defname in kwargs:
                setattr(self, defname, kwargs.pop(defname))
            if not hasattr(self, defname):
                setattr(self, defname, dict(self.defaults)[defname])

        if kwargs:
            raise TypeError("Unexpected field initialization parameters: " +
                ', '.join(kwargs.keys()))

    def clean(self, value):
        return value

    def validate(self, value):
        pass

    def __get__(self, obj, objtype):
        return self.__value

    def __set__(self, obj, value):
        cleaned_value = self.clean(value)
        self.validate(cleaned_value)
        self.__value = cleaned_value

class Model(object):
    version = "unknown"

    def __init__(self):
        self.fields = []
        self.fields.extend(self._getFields(sub=Field))

    def _getFields(self, cls=None, sub=None):
        """Utility to locate class-defined options."""
        assert cls or sub

        for name, value in vars(type(self)).items():
            if cls:
                if isinstance(value, cls):
                    yield (name, value)
            elif sub:
                if issubclass(type(value), sub):
                    yield (name, value)

