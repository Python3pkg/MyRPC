README=../README.md
MANIFEST=../etc/MANIFEST.in
DISTUTILS_HELPER=../etc/distutils_helper.py

all:
	cp $(README) $(MANIFEST) $(DISTUTILS_HELPER) .
	python3.3 setup.py sdist

clean:
	rm -rf README.md MANIFEST* distutils_helper.py dist build __pycache__
