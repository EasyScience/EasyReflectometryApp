.. highlight:: shell

==================================
Building a development environment
==================================

The EasyReflectometry project consists of two packages; an application and a library. 
To develop effectively for EasyReflectometry, we work on the :code:`develop` branch of both and then periodically merge to :code:`master` when a release is made. 

With this in mind, the best way to build a development environment for EasyReflectometry is as follows. 

.. code-block:: console

    $ mamba create -y -n easy_refl python=3.9
    $ mamba activate easy_refl
    $ git clone git@github.com:easyScience/EasyReflectometryLib.git
    $ cd EasyReflectometryLib
    $ git checkout develop
    $ pip install -e '.[dev]'
    $ cd ../
    $ git clone git@github.com:easyScience/EasyReflectometryApp.git
    $ cd EasyReflectometryApp
    $ git checkout develop
    $ pip install -e .

Note, that the use of :code:`mamba` is a personal choice, if you prefer building Python environments with :code:`pyenv` that should also work. 
This will build, in-place, versions of both the application and the library. 
The application can then be run (from within the appropriate Python environment) with the following. 

.. code-block:: console

    $ EasyReflectometryApp

Additional requirements
-----------------------

Some additional requirements exist that are operating system specific. 

Linux
^^^^^

.. code-block:: console

    sudo apt install libxcb-xinerama0
