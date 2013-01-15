Writing Fields
===============

Descriptors!
------------

The second class in **mannequin** is the ``Field`` and it is only slightly more interesting than the ``Model``. It represents the various `data attributes` of your objects but does so in an interesting way. The ``Field`` class is what is called a **Descriptor** in Python. This is a `special object` that, when assigned to the attribute of a class, takes on some special properties. 

For a full explanation see the `Descriptor How-to Guide <http://docs.python.org/2/howto/descriptor.html>`_

Essentially, a Descriptor is an object that implements a ``__get__`` and a ``__set__`` method. When a Descriptor instance is assigned to an **attribute of a class**, instances of that class will aquire the Descriptor. Because the attribute is a Descriptor, **all access and assignment** to that attribute is `controlled by these methods` on the Descriptor. Here is a trivial example of a Descriptor that returns squares of it's internal value:


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
