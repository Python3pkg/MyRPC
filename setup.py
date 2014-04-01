#!python

# FIXME: Note that any pathnames (files or directories) supplied
#        in the setup script should be written using the Unix convention.
# FIXME: require
# FIXME: doc make

import os
import os.path

from distutils.core import setup

# List of all target languages (py is not included, since py runtime will
# be installed to the site-packages directory).

RUNTIME_LANGS = ("js",)

# Assemble data_files list.

data_files = []

def walk_error(e):
    raise e

for lang in RUNTIME_LANGS:
    runtimedir = os.path.join("runtime", lang)
    walk_r = os.walk(runtimedir, onerror = walk_error)

    for (dirpath, dirnames, filenames) in walk_r:
        if len(filenames) == 0:
            continue

        destdir = os.path.join("share", "myrpc", dirpath)
        srcfiles = [os.path.join(dirpath, filename) for filename in filenames]
        data_files.append((destdir, srcfiles))

# Run setup.

setup(name = "MyRPC",
      version = "0.0.3-dev",
      description = "RPC Framework for Distributed Computing",
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
""",
      author = "Szalai András",
      author_email = "andrew@bandipapa.com",
      url = "https://github.com/bandipapa/MyRPC",
      platforms = "cross-platform",
      license = "BSD",
      keywords = "rpc, Python, JavaScript, cross-platform, framework",
      classifiers = ("Development Status :: 4 - Beta",
                     "Intended Audience :: Developers",
                     "License :: OSI Approved :: BSD License",
                     "Operating System :: OS Independent",
                     "Programming Language :: Python :: 3.3",
                     "Topic :: Software Development :: Object Brokering"),
      scripts = ("bin/myrpcgen",),
      package_dir = {"myrpcgen": "bin/lib",
                     "myrpc": "runtime/py"},
      packages = ("myrpcgen",
                  "myrpc",
                  "myrpc.codec",
                  "myrpc.transport",
                  "myrpc.util"),
      data_files = data_files)
