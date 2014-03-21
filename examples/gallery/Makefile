IDL=gallery.idl
JS_OUTDIR=www/gen

all:
	myrpcgen -d . -g py -P $(IDL)
	myrpcgen -d $(JS_OUTDIR) -g js -C $(IDL)

clean:
	rm -rf GalleryService $(JS_OUTDIR)
