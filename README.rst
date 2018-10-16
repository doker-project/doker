Doker
=====

**Doker** stands for **do**\ cument ma\ **ker**.

Installation
============

Run in console::

  pip install doker

Usage
=====

Create ``minimal.yaml``::

  root: .

Create ``main.rst``:

.. code:: restructuredtext

   Minimal Document
   ================

   **Hello**, *world*!

And run in console::

  doker --pdf minimal

Find ``minimal.pdf`` in the current directory.

Deeper diving
=============

See `examples <https://github.com/doker-project/doker/tree/master/examples>`__ for most popular use cases.

Documentation
=============

Read the `user's manual <https://doker.org/manual.pdf>`__ for usage details.

License
=======

Source code is licensed under `MIT license <https://github.com/doker-project/doker/blob/master/LICENSE>`__.