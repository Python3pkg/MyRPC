IDL=gallery.idl
BROWSER_OUTDIR=www/gen

all:
	myrpcgen -o -d . -g py -P $(IDL)
	myrpcgen -o -d $(BROWSER_OUTDIR) -g js -C $(IDL)

clean:
	rm -rf GalleryService $(BROWSER_OUTDIR)
