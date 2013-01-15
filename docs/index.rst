.. straight.plugin documentation master file, created by
   sphinx-quickstart on Wed Jan 25 22:49:22 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to mannequin's documentation!
===========================================

Contents:

.. toctree::
   :maxdepth: 2

   Writing Models <write-model>
   Writing Fields <write-field>
   Glossary <glossary>


Full Documentation: http://readthedocs.org/docs/mannequin/

Overview
========

**mannequin** is very simple.

It is a small library that helps you create `declarative models` for your own
libraries and applications using Python class definitions. Declarative models
are a nice way to define the `structure of your data or objects`. Using Python
classes for this keeps it natural and familiar.

If you've ever encountered the Python web-framework Django you might be
familiar with it's ``Models`` or ``Forms``. Django uses this declarative technique
to allow you to naturally define tables in your database:

::

    from django.db import models

    class Person(models.Model):
        first_name = models.CharField(max_length=30)
        last_name = models.CharField(max_length=30)


Or the types and ordering of fields of your web-forms:

::

    from django import forms

    class ContactForm(forms.Form):
        subject = forms.CharField(max_length=100)
        message = forms.CharField()
        sender = forms.EmailField()
        cc_myself = forms.BooleanField(required=False)


There are other database libraries that use this technique to represent
database schemas like SQLAlchemy and Axiom.

Let's look at a theoretical example of unpacking binary data from structures.
With the standard ``struct`` module this can be a painful exercise. Given some
imagined packet structure, unpacking a binary stream into the various fields
is cumbersome:

::

    header = struct.unpack('B',data[0])
    length = struct.unpack('B',data[1])
    typeID = struct.unpack('!I',data[2:6])
    param1 = struct.unpack('!H',data[6:8])
    param2 = struct.unpack('!H',data[8:10])
    param3 = struct.unpack('!H',data[10:12])
    param4 = struct.unpack('!H',data[12:14])
    name = struct.unpack('20s',data[14:38])
    checksum = struct.unpack('!I',data[38:42])
    footer = struct.unpack('B',data[42]) 


Yikes! Even if we ask ``struct`` to unpack all of the fields at once, we are
then relegated to numerical indexing. We can use namedtuples but we still have
the feeling that there has to be a better way:

::

    fields = struct.unpack('!BBI4H20sIB', data)

    fields[0] # get the header

    # this might be a more comfortable alternative, perhaps:

    (header, length, typeID, param1, param2,
    param3, param4, name_string, checksum, footer,
    ) = struct.unpack("!2B I 4H 24s I B", data)


One could imagine a library that uses the same sort of `class-based schema
delcaratives` that Django does to solve this problem. Here is a hypothetical
definition of the same packet structure as above:

::

    class TCPPacket(PacketModel):

        endian = BIG

        header = fields.Byte()
        length = fields.Byte()
        type = fields.Integer()
        params = fields.List(4, fields.Short())
        name = fields.String(20)
        checksum = fields.Integer()
        footer = fields.Byte()


The obvious advantage here is `readability`. But there are some other not so
obvious advantages. The fact that this packet declaration is a class means
that it can be `subclassed into more specific implementations`, perhaps adding
`additional fields`. If we were implementing an application specific protocol we
could implement the header of our protocol in a base class and use that in the
actual implementation of our various packet types.

Another advantage is that it keeps the `handling` of each specific packet `close
to the structure definition`. Each class declarative can contain methods
specific to usage inside your application.

Since we are using ``Field`` objects to define the types of our various packet
fields we also gain the ability to do `implicit validation on data`. For
example, if we had an application protocol that featured an authentication
mechanism the Field classes can work harder for us than in the ``TCPPacket``
example:


::

    class UsernameField(fields.String):
        def __init__(self):
            # UsernameField provides an implicit length to String
            super(UsernameField, self).__init__(32) 

        def clean(self, value):
            try:
                # lookup user in database
                # and return it
                return User.objects.get(username=cleaned)
            except User.DoesNotExist, e:
                # ValidationError indicates this field failed
                # to clean
                raise ValidationError(e.message)

        def validate(self, cleaned):
            # recieves actual user instance from self.clean()
            if not user.active:
                msg = "%s is not a currently activated user." % cleaned.username
                raise ValidationError(msg) # indicate failure to validate

    class PasswordField(fields.String):
        def __init__(self):
            # PasswordField provides an implicit length to String
            super(UsernameField, self).__init__(32) 

        def validate(self, cleaned):
            user = self.parent.user
            try:
                # check the password for the user
                user.check_password(cleaned)
                # authenticate user if no exception
                user.authenticate()
            except AuthenticationError, e:
                raise ValidationError(e.message)

    class LoginPacket(MyAppPacket):
        # MyAppPacket provides MyApp's protocol header fields
        user = UsernameField() # verifies user exists in database
        password = PasswordField() # authenticates user on validation


Getting Started
===============

The easiest way to get started is to checkout the examples in the source repository. It may be beneficial to read about ``Models`` and ``Fields``. You may also enjoy the tutorial which describes how to use **mannequin** to create a declarative XML parser.

Read the :doc:`write-model` documentation to get started.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

