#!python

# FIXME: Note that any pathnames (files or directories) supplied
#        in the setup script should be written using the Unix convention.
# FIXME: require
# FIXME: doc make
# FIXME: read from README.md

from distutils.core import setup

# Run setup.

setup(name = "myrpc-runtime",
      version = "0.0.3-dev",
      description = "MyRPC Python runtime",
      long_description = """MyRPC is a remote procedure call framework designed to easily connect heterogeneous systems.

Short summary of MyRPC features:

* No external dependencies.
* Cross-platform capability.
* IDL-based client and server stub generation.
* Binary capable (no need for escaping of binary data).
* Single roundtrip protocol, ideal for HTTP (but no limited to).
* Support various data types: string, binary, signed and unsigned
  integers, floating point, list, structure and enumeration.
* All data types are supported on all platforms.
* Support exceptions.
* Correct input validation of the received messages.
* Legacy free code (since we are new :).

Info:

* Feature introduction: http://myrpc.readthedocs.org/en/latest/features.html
* Installation: http://myrpc.readthedocs.org/en/latest/install.html
* Sample code: http://myrpc.readthedocs.org/en/latest/examples.html
* License: http://myrpc.readthedocs.org/en/latest/license.html
* Full doc: http://myrpc.readthedocs.org
""",
      author = "Szalai András",
      author_email = "andrew@bandipapa.com",
      url = "https://github.com/bandipapa/MyRPC",
      platforms = "cross-platform",
      license = "BSD",
      keywords = "rpc, Python, JavaScript, Node.js, cross-platform, framework",
      classifiers = ("Development Status :: 4 - Beta",
                     "Intended Audience :: Developers",
                     "License :: OSI Approved :: BSD License",
                     "Operating System :: OS Independent",
                     "Programming Language :: Python :: 3.3",
                     "Topic :: Software Development :: Object Brokering"),
      package_dir = {"myrpc": "src"},
      packages = ("myrpc",
                  "myrpc.codec",
                  "myrpc.transport",
                  "myrpc.util"))
