IDL=chat.idl
NODE_OUTDIR=node_modules
BROWSER_OUTDIR=www/gen

all:
	npm install myrpc-runtime
	myrpcgen -o -d $(NODE_OUTDIR)/ChatService -g js --js_target node -P $(IDL)
	myrpcgen -o -d $(BROWSER_OUTDIR) -g js -C $(IDL)

clean:
	rm -rf $(NODE_OUTDIR) $(BROWSER_OUTDIR)
