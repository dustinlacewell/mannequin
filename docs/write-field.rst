Writing Fields
===============

Descriptors!
------------

The second class in **mannequin** is the ``Field`` and it is  slightly more
interesting than the ``Model``. It represents the various `data attributes` of
your objects but does so in an interesting way. The ``Field`` class is what is
called a **Descriptor** in Python. This is a `special object` that, when
assigned to the attribute of a class, takes on some special properties.

For a full explanation see the `Descriptor How-to Guide <http://docs.python.org/2/howto/descriptor.html>`_

Essentially, a Descriptor is an object that implements a ``__get__`` and a
``__set__`` method. When a Descriptor instance is assigned to an **attribute
of a class**, instances of that class will aquire the Descriptor. Because the
attribute is a Descriptor, **all access and assignment** to that attribute is
`controlled by these methods` on the Descriptor. Here is a trivial example of
a Descriptor that returns squares of it's internal value:


::

    class SquaredDescriptor(object):
        def __init__(self):
            self.__value = None

        def __get__(self, obj, obj_type):
            try:
                return self.__value * self.__value
            except TypeError:
                return self.__value

        def __set__(self, obj, value):
            self.__value = value


    class Dummy(object):
        squared = SquaredDescriptor()

We can see this descriptor in action in the interactive session below:

::

    # first create an instance of the Dummy class
    >>> obj = Dummy()

    # our instance has the `squared` attribue
    >>> print obj.squared
    None

    # if we assign a numerical value...
    >>> obj.squared = 5

    # it is squared when accessed
    >>> print obj.squared
    25

    # according to the implementation
    >>> obj.squared = "five"

    # non-numeric values should be returned as-is
    >>> print obj.squared
    five


The nature of Descriptors is what makes the ``Field`` class interesting and
useful. Since assignment can be mediated through the ``Field`` it can provide
*data sanitation* or *parsing* benefits. The base ``Field`` class has a couple
methods already for implementing such behaviors. Here is the base ``Field``
implementation below:


::

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



When you instantiate a ``Field`` class the first thing that the base implementation does, is loop through the ``Field.defaults``. This tuple designates what the **optional** initialization parameters are for the ``Field``. Any keyword arguments passed to the ``Field`` that it doesn't expect will raise a ``TypeError``. Any `missing` keyword arguments will be given the corresponding default from the ``defaults`` attribute.


The second important thing about the ``Field`` class is that it is a `Descriptor`. Once instantiated and assigned to a ``Model`` Class declaration, all access and assignment will be regulated by the ``Field`` instance. We can see that the base ``Field`` implementation provides some basic handling here:

::

        def __set__(self, obj, value):
            cleaned_value = self.clean(value)
            self.validate(cleaned_value)
            setattr(obj, '__field_{0}'.format(id(self)), cleaned_value)

When we assign a value to a Field descriptor a few things happen. The first is that the value is passed to ``Field.clean()``. The default implementation simply returns the value "as is"; however this is a great method in which you can provide your own santiation or other parsing operations. Next, the `cleaned value` is passed to ``Field.validate()``. The default implementation here does nothing, but you can stick in your own validation code by overriding the method.

Lastly, once your Field considers the data value as cleaned and validated, the value is stored in a slightly obsfucated manner. Foremost, the value is stored on the ***Model instance*** that the ``Field`` is bound to. The attribute name given to the value interpolates the `Python object ID` of the current ***Field instance***. The current ``Field`` instance is used so that multiple ``Fields`` of the same type can be bound to the same ``Model``.

::

        def __get__(self, obj, objtype):
            return getattr(obj, "__field_{0}".format(id(self)))

Here we can see that when accessing the ``Field`` value, the same attribute name is generated and the value is returned.


Continuing from here
--------------------

Now that you have a good idea about how both mannequin ``Models`` and ``Fields`` work, head over to the XML Parser Tutorial to see how a real library can be written using mannequin and the declarative technique.