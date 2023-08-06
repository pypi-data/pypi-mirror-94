Data Insertion
==============

Data Models
~~~~~~~~~~~

Data is stored and structured in CaosDB using a concept of RecordTypes,
Properties, Records etc. If you do not know what these are, please look
at the chapter :any:`caosdb-server:Data Model` .

In order to insert some actual data, we need to create a data model
using RecordTypes and Properties (You may skip this if you use a CaosDB
instance that already has the required types). So, let’s create a simple
Property called “a” of datatype double. This is very easy in pylib:

.. code:: python

   a = db.Property(name="a", datatype=db.DOUBLE)

There are a few basic datatypes: db.INTEGER, db.TEXT. See `data
type <Specification/Datatype>`__ for a full list.

We can create our own small data model for e.g. a simulation by adding
two more Properties and a RecordType:

.. code:: python

   b = db.Property(name="b", datatype=db.DOUBLE)
   epsilon = db.Property(name="epsilon", datatype=db.DOUBLE)
   recordtype = db.RecordType(name="BarkleySimulation")
   recordtype.add_property(a)
   recordtype.add_property(b)
   recordtype.add_property(epsilon)
   container = db.Container()
   container.extend([a, b, epsilon, recordtype])
   container.insert()

Insert Actual Data
~~~~~~~~~~~~~~~~~~

Suppose the RecordType “Experiment” and the Property “date” exist in the
database. You can then create single data Records by using the
corresponding python class:

.. code:: python

   rec = db.Record()
   rec.add_parent(name="Experiment")
   rec.add_property(name="date", value="2020-01-07")
   rec.insert()

Here, the record has a parent: The RecordType “Experiment”. And a
Property: date.

Note, that if you want to use a property that is not a primitive
datatype like db.INTEGER and so on, you need to use the ID of the Entity
that you are referencing.

.. code:: python

   rec = db.Record()
   rec.add_parent(name="Experiment")
   rec.add_property(name="report", value=235507)
   rec.add_property(name="Analysis", value=230007)
   rec.insert()

Of course, the IDs 235507 and 230007 need to exist in CaosDB. The first
example shows how to use a db.REFERENCE Property (report) and the second
shows that you can use any RecordType as Property to reference a Record
that has such a parent.

Most Records do not have name however it can absolutely make sense. In
that case use the name argument when creating it. Another useful feature
is the fact that properties can have units:

.. code:: python

   rec = db.Record("DeviceNo-AB110")
   rec.add_parent(name="SlicingMachine")
   rec.add_property(name="weight", value="1749", unit="kg")
   rec.insert()

If you are in some kind of analysis you can do this in batch mode with a
container. E.g. if you have a python list ``analysis_results``:

.. code:: python

   cont = db.Container()
   for date, result in analysis_results:
      rec = db.Record()
      rec.add_parent(name="Experiment")
      rec.add_property(name="date", value=date)
      rec.add_property(name="result", value=result)
      cont.append(rec)

   cont.insert()

Useful is also, that you can insert directly tabular data.

.. code:: python

   from caosadvancedtools.table_converter import from_tsv     
          
   recs = from_tsv("test.csv", "Experiment")     
   print(recs)     
   recs.insert()  

With this example file
`test.csv <uploads/4f2c8756a26a3984c0af09d206d583e5/test.csv>`__.

Inheritance of Properties
-------------------------

Given, you want to insert a new RecordType “Fridge temperatur
experiment” as a child of the existing RecordType “Experiment”. The
latter may have an obligatory Property “date” (since every experiment is
conducted at some time). It is a natural way of thinking, that every sub
type of “Experiment” also has this obligatory Property—in terms of
object oriented programing the “Fridge temperatur experiment” *inherits*
that Property.

::

       rt = h.RecordType(name="Fridge temperatur experiment", 
                                 description="RecordType which inherits all obligatory properties from Experiment"
                                 ).add_parent(name="Experiment", inheritance="obligatory").insert()
       
       print(rt.get_property(name="date").importance) ### rt now has a "date"-property -> this line prints "obligatory"

The parameter *``inheritance=(obligatory|recommended|fix|all|none)``* of
``add_parent`` tells the server to assign obligatory:: properties of the
parent to the child automatically, recommended:: properties of the
parent to the child automatically, fix:: properties of the parent to the
child automatically, all:: properties of the parent to the child
automatically, none:: of the properties of the parent to child
automatically,

File Update
-----------

Updating an existing file by uploading a new version.

1. Retrieve the file record of interest, e.g. by ID:

.. code:: python

   import caosdb as db

   file_upd = db.File(id=174).retrieve()

2. Set the new local file path. The remote file path is stored in the
   file object as ``file_upd.path`` while the local path can be found in
   ``file_upd.file``.

.. code:: python

   file_upd.file = "./supplements.pdf"

3. Update the file:

.. code:: python

   file_upd.update()
