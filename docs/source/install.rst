.. FIXME: Document installation on Windows.
.. FIXME: How to build docs (+ deps).

Installation
============

Requirements:

* For running the code generator tool (myrpcgen), Python >= 3.3 is
  required.
* For building the examples, GNU Make >= 3.82 is required.

The latest stable release of MyRPC can be downloaded from
https://github.com/bandipapa/MyRPC/releases, look for rel-x.x.x tags.

After unpacking the source distribution, change directory to MyRPC-rel-x.x.x.
Here you can do system-wide installation (as root):

.. code-block:: sh

   python setup.py install

or, as an alternative solution, MyRPC can be installed into a user's home
directory:

.. code-block:: sh

   python setup.py install --user

For more information about Distutils based installation, see
http://docs.python.org/3/install/index.html.

Language dependent runtime libraries will be installed into
*prefix*/share/myrpc/runtime, except for Python runtime, which will go
into Python site-packages directory.
