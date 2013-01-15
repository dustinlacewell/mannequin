from __future__ import print_function

import sys
import re
from itertools import chain

class Field(object):
    
    defaults = tuple()

    def __init__(self, **kwargs):
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
        return getattr(obj, "__field_{0}".format(id(self)))

    def __set__(self, obj, value):
        cleaned_value = self.clean(value)
        self.validate(cleaned_value)
        setattr(obj, '__field_{0}'.format(id(self)), cleaned_value)


class Model(object):
    version = "unknown"

    def gather_fields(self, cls=None, sub=None):
        """Utility to locate class-attributed Fields"""
        assert cls or sub

        self.fields = dict()

        def _gather_fields():
            for name, value in vars(type(self)).items():
                if cls:
                    if isinstance(value, cls):
                        self.bind_field(name, value)
                elif sub:
                    if issubclass(type(value), sub):
                        self.bind_field(name, value)

        _gather_fields()
        self.fields_gathered(self.fields)

    def bind_field(self, name, field):
        field.parent = self
        self.fields[name] = field

    def fields_gathered(self, fields):
        pass
