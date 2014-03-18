Examples
========

Here you can find some information about demo code included in MyRPC
source distribution.

Gallery
-------

Source code: https://github.com/bandipapa/MyRPC/tree/master/examples/gallery.

This is an example demonstrating how you can use MyRPC to create a simple
web/ajax-based picture gallery application. Try to upload an image and see
what happens... :)

Requirements:

* Pillow >= 2.3.0 (http://python-imaging.github.io)

To compile MyRPC IDL files:

.. code-block:: sh

   cd examples/gallery
   make

To start the demo:

.. code-block:: sh

   python gallery 8080

where 8080 is a portnumber, feel free to use any other.

Then point your browser at http://yourip:8080, and upload some images. The
uploaded images are simply stored in memory (not saved to disk).

Source code files:

+----------------------+------------------------------------------------------------+
| File                 | Description                                                |
+======================+============================================================+
| gallery              | Contains a standalone webserver and the implementation of  |
|                      | GalleryService. Most of the code deals with the HTTP       |
|                      | infrastructure & static file serving, the MyRPC relevant   |
|                      | parts are: GalleryServiceImpl class and handle_rpc method. |
+----------------------+------------------------------------------------------------+
| gallery.idl          | Interface description of GalleryService.                   |
+----------------------+------------------------------------------------------------+
| GalleryService/\*.py | Generated code (stubs) for Python server-side.             |
+----------------------+------------------------------------------------------------+
| www/index.html,      | HTML/JavaScript webcontent, served by the built-in         |
| www/gallery.js       | webserver.                                                 |
+----------------------+------------------------------------------------------------+
| www/gen/\*.js        | Generated code (stubs) for JavaScript client-side.         |
+----------------------+------------------------------------------------------------+
| www/myrpc/\*.js      | MyRPC JavaScript runtime libraries (these are just         |
|                      | symlinks).                                                 |
+----------------------+------------------------------------------------------------+
