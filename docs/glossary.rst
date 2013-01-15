Glossary
-------------

.. glossary::
    :sorted:

    package
        A Python package is a module defined by a directory, containing
        a ``__init__.py`` file, and can contain other modules or other
        packages within it.

        ::
        
            package/
                __init__.py
                subpackage/
                    __init__.py
                submodule.py

        see also, :term:`namespace package`

    declarative
        In computer science, declarative programming is a programming paradigm
        that expresses the logic of a computation without describing its
        control flow. Many languages applying this style attempt to
        minimize or eliminate side effects by describing what the program
        should accomplish, rather than describing how to go about
        accomplishing it (the how is left up to the language's
        implementation). This is in contrast with imperative programming, in
        which algorithms are implemented in terms of explicit steps.

    django
        Django is an open source web application
        framework, written in Python, which follows the model–view–controller
        architectural pattern. It was originally developed to manage several news-
        oriented sites for The World Company of Lawrence, Kansas, and was released
        publicly under a BSD license in July 2005; the framework was named after
        guitarist Django Reinhardt. In June 2008 it was announced that a newly
        formed Django Software Foundation will maintain Django in the future.
        https://djangoproject.com/

    struct
        This module performs conversions between Python values and C structs
        represented as Python strings. This can be used in handling binary data stored
        in files or from network connections, among other sources. It uses Format
        Strings as compact descriptions of the layout of the C structs and the
        intended conversion to/from Python values.
        http://docs.python.org/2/library/struct.html

    namedtuple
        Returns a new tuple subclass named typename. The new subclass is used to
        create tuple-like objects that have fields accessible by attribute lookup as
        well as being indexable and iterable. Instances of the subclass also have a
        helpful docstring (with typename and field_names) and a helpful __repr__()
        method which lists the tuple contents in a name=value format.
        http://docs.python.org/2/library/collections.html#collections.namedtuple


    packet
        In computer networking, a packet is a formatted unit of data carried by a
        packet mode computer network. Computer communications links that do not
        support packets, such as traditional point-to-point telecommunications links,
        simply transmit data as a series of bytes, characters, or bits alone. When
        data is formatted into packets, the bitrate of the communication medium can be
        better shared among users than if the network were circuit switched.


    binary stream
        A binary file is a computer file that is not a text file; it may contain any
        type of data, encoded in binary form for computer storage and processing
        purposes. Many binary file formats contain parts that can be interpreted as
        text; for example, some computer document files containing formatted text,
        such as older Microsoft Word document files, contain the text of the document
        but also contain formatting information in binary form.

    application protocol
        In computer network programming, the application layer is an abstraction layer
        reserved for communications protocols and methods designed for process-to-
        process communications across an Internet Protocol (IP) computer network.
        Application layer protocols use the underlying transport layer protocols to
        establish host-to-host connections.
