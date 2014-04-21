JS_SRCDIR=src
BASE_DISTDIR=dist
NODE_DISTDIR=$(BASE_DISTDIR)/node
NODE_PACKAGE_JSON=package.json
README=../../README.md
FILES=$(shell cd $(JS_SRCDIR) && find . -name \*.js)

all:	node

node:
	for file in $(FILES); \
	do \
		dirname=$(NODE_DISTDIR)/lib/`dirname $${file}`; \
		mkdir -p $${dirname}; \
		awk 'BEGIN { print "(function() {"; \
		             print "var myrpc;"; \
		             print ""; \
		             first_dep = 1; } \
		     $$0 ~ /^\/\/ MODULE_EXPORT/ { if (!first_dep) print ""; \
                                                   print "module.exports = myrpc;"; \
		                                   next; } \
		     $$0 ~ /^\/\/ MODULE_DEP/ { if (first_dep) { \
		                                    printf "myrpc = "; \
		                                    first_dep = 0; \
		                                } \
		                                printf "require(\"%s\");\n", $$3; \
		                                next; } \
		     { print $$0; } \
		     END { print "})();"; }' $(JS_SRCDIR)/$${file} > $(NODE_DISTDIR)/lib/$${file}; \
	done
	cp $(NODE_PACKAGE_JSON) $(NODE_DISTDIR)
	cp $(README) $(NODE_DISTDIR)

clean:
	rm -rf $(BASE_DISTDIR)
