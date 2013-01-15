Writing Models
===============

Code Listing
------------

The main class in **mannequin** is the ``Model``. It represents your object and contains all of the data fields provided in its declaration. Other than that, the ``Model`` base-class provides only a few other methods for the book-keeping of said ``Fields``.

Here is the ``Model`` implementation:

::

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


Initialization
--------------

When you instantiate your ``Model`` subclasses, they will already feature the various **Field** descriptors you defined on those subclasses. In fact, nothing about the declarative technique supported by **mannequin** depends on any of the code in this class.

The ``gather_fields`` method here is provided purely as a convenience. It introspects the class and determines each of the instance attributes are subclasses of the **mannequin** ``Field`` type. It stores each of ``Fields`` into a ``.fields`` dictionary on the ``Model`` so that you can use for whatever you'd like.

While gathering the fields, the ``bind_field`` method will be called for each. This is one place you can hook in the case you happen to need to "post-process" each field. The other place is the ``fields_gathered`` method which will be called with the final dictionary of Fields.

As you can see the ``Model`` class is very minimal. However this makes more room for your application specific methods. These models are your data objects after all and your subclasses will likely feature a number of methods relevant to that type, in addition to any Fields you put there.