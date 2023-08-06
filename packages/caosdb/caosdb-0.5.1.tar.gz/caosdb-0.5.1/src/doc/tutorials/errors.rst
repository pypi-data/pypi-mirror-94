
Error Handling
--------------

HeartDBException
~~~~~~~~~~~~~~~~

TransactionError
~~~~~~~~~~~~~~~~

Every transaction (calling ``insert``, ``update``, ``retrieve``, or
``delete`` on a container or an entity) may finish with errors. They
indicate, for instance, that an entity does not exist or that you need
to specify a data type for your property and much more. If and only if
one or more errors occur during a transaction a ``TransactionError``
will be raised by the transaction method. The ``TransactionError`` class
is a container for all errors which occur during a transaction. It can
help you to find the crucial problems with your transaction by two
important methods: \* ``get_errors()`` which returns a list of instances
of ``EntityError``. \* ``get_entities()`` which returns a list of
entities in the transaction container which are erroneous.

Additionally, ``print(transaction_error`` prints a tree-like
representation of all errors regarding the transaction in question.

EntityError
~~~~~~~~~~~

An ``EntityError`` represents a single error that has been returned by
the server. You might call \* ``get_entity()`` which returns the entity
which caused the error. \* ``get_description()`` which returns a
description of the error. \* ``get_code()`` which returns the error code
(if specified) or 0 (if not).

In fact, the ``EntityError`` class is a subclass of
``TransactionError``. So, it inherits the ``get_entities()``. Unless
overridden by subclasses of ``EntityError``, it return a list with only
one item—the entity which caused this error. Similarly, unless
overridden by subclasses, the ``get_errors()`` method returns a list
with only one item—``[self]``.

Special Errors
~~~~~~~~~~~~~~

Subclasses of ``EntityError`` for special purposes: \*
``EntityDoesNotExistError`` \* ``EntityHasNoDataTypeError`` \*
``UniqueNamesError`` \* ``UnqualifiedParentsError`` - overrides
``get_entities()``: returns all parent entities with errors. - overrides
``get_errors()``: returns a list of EntityErrors which have been caused
by parent entities. \* ``UnqualifiedPropertiesError`` - overrides
``get_entities()``: returns all properties with errors. - overrides
``get_errors()``: returns a list of EntityErrors which have been caused
by properties.
