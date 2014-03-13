IDL=gallery.idl

all:
	myrpcgen -d . -g py -P $(IDL)
	myrpcgen -d www/gen -g js -C $(IDL)
