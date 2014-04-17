IDL=chat.idl
NODE_OUTDIR=gen
BROWSER_OUTDIR=www/gen

all:
	myrpcgen -o -d $(NODE_OUTDIR) -g js -P $(IDL)
	myrpcgen -o -d $(BROWSER_OUTDIR) -g js -C $(IDL)

clean:
	rm -rf $(NODE_OUTDIR) $(BROWSER_OUTDIR)
