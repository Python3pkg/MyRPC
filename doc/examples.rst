.. TODO: Sync with examples/gallery/www/index.html.

Examples
========

Here you can find some information about demo code included in MyRPC
source distribution.

Gallery
-------

Source code: https://github.com/bandipapa/MyRPC/tree/master/examples/gallery.

This is an example demonstrating how you can use MyRPC to create a simple
web/ajax-based picture gallery application, with Python server and JavaScript
client code. Try to upload an image and see what happens... :)

Requirements:

* Pillow >= 2.3.0 (http://python-imaging.github.io)

To compile MyRPC IDL files:

.. code-block:: sh

   cd examples/gallery
   make

To start the demo:

.. code-block:: sh

   python gallery 8080

where *8080* is a portnumber, feel free to use any other.

Then point your browser at http://yourip:8080, and upload some images. The
uploaded images are simply stored in memory (not saved to disk).

Source code files:

+-----------------------------+------------------------------------------------------------+
| File                        | Description                                                |
+=============================+============================================================+
| :file:`gallery`             | Contains a standalone webserver and the implementation of  |
|                             | *GalleryService*. Most of the code deals with the HTTP     |
|                             | infrastructure & static file serving, the MyRPC relevant   |
|                             | parts are: *GalleryServiceImpl* class and *handle_rpc*     |
|                             | method.                                                    |
+-----------------------------+------------------------------------------------------------+
| :file:`gallery.idl`         | Interface description of *GalleryService*.                 |
+-----------------------------+------------------------------------------------------------+
| :file:`GalleryService/*.py` | Generated code (stubs) for Python server.                  |
+-----------------------------+------------------------------------------------------------+
| :file:`www/index.html`,     | HTML/JavaScript webcontent, served by the built-in         |
| :file:`www/gallery.js`      | webserver.                                                 |
+-----------------------------+------------------------------------------------------------+
| :file:`www/gen/*.js`        | Generated code (stubs) for JavaScript client.              |
+-----------------------------+------------------------------------------------------------+
| :file:`www/myrpc/*.js`      | MyRPC JavaScript runtime libraries (these are just         |
|                             | symlinks).                                                 |
+-----------------------------+------------------------------------------------------------+
