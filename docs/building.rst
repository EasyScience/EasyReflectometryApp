.. highlight:: shell

========
Building
========

The EasyReflectometry project consists of two packages; an application and a library. 
To develop effectively for EasyReflectometry, we work on the :code:`develop` branch of both and then periodically merge to :code:`master` when a release is made. 


Stable release
--------------

To install EasyReflectometry, run this command in your terminal:

.. code-block:: console

    $ pip install git+https://github.com/easyScience/EasyReflectometryLib.git@master

This is the preferred method to install EasyReflectometry, soon EasyReflectometry will also be available on PyPI.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


Developer Instrutions
---------------------

Clone the public repository:

.. code-block:: console

    $ git clone git://github.com/easyScience/EasyReflectometryLib

And install the latest developer version with:

.. code-block:: console

    $ cd EasyReflectometryLib
    $ git checkout develop
    $ pip install -e ".[dev]"
