Getting Started
===============

Installation
------------

Run in console::

  pip install doker

Usage
-----

Create ``minimal.yaml``::

  root: .

Create ``main.rst``:

.. code:: restructuredtext

   Minimal Document
   ================

   **Hello**, *world*!

And run in console::

  doker --pdf minimal

Find ``minimal.pdf`` in the current directory. It is to look like `this one <https://github.com/doker-project/doker/blob/master/examples/minimal/minimal.pdf>`__.

Deeper diving
-------------

See `examples <https://github.com/doker-project/doker/tree/master/examples>`__ for most popular use cases.