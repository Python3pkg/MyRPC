// MyRPC: Chat demo to test long polling.

// FIXME: fix loading...
ChatService = {};
window = {};
var fs = require('fs');
var vm = require('vm');
var includeInThisContext = function(path) {
    var code = fs.readFileSync(path);
    vm.runInThisContext(code, path);
}.bind(this);
var myrpc = require("myrpc-runtime");
require("myrpc-runtime/lib/transport/MemoryTransport");
require("myrpc-runtime/lib/codec/BinaryCodec");
require("myrpc-runtime/lib/util/ProcessorSubr"); // FIXME: not needed
global.myrpc = myrpc;
includeInThisContext("./gen/Types.js");
includeInThisContext("./gen/Processor.js");

var INDEX = "index.html";
var WWW_DIR = "www";
var CONTENT_TYPE = "Content-Type";
var MIMETYPES = {".html": "text/html",
		 ".js": "application/javascript"};
var MAX_MESSAGES = 1000;
var MESSAGEBUFFER_TIMER_INTERVAL = (10 * 1000);
var MESSAGEBUFFER_WAITER_TIMEOUT = (60 * 1000);

var http = require("http");
var path = require("path");
var fs = require("fs");

// WaiterInfo stores waiter callback and wait-until timestamp
// (used for timeout long-waiting clients, which forces clients to
// reconnect).

WaiterInfo = function(waiter)
{
    this._waiter = waiter;
    this._ts = Date.now() + MESSAGEBUFFER_WAITER_TIMEOUT;
};

WaiterInfo.prototype.get_waiter = function()
{
    return this._waiter;
};

WaiterInfo.prototype.has_timeout = function(ts)
{
    var r = (this._ts < ts);

    return r;
};

// MessageBuffer is responsible for storing and retrieving messages.

MessageBuffer = function()
{
    this._messages = [];      // List of stored messages.
    this._next_messageid = 0; // Next message id.
    this._waiterinfos = [];   // List of WaiterInfos.

    setInterval(myrpc.common.proxy(this._timeout_waiters, this), MESSAGEBUFFER_TIMER_INTERVAL);
};

MessageBuffer.prototype.list_messages = function(skip_messageid)
{
    var r;
    var i;
    var found = false;

    // Filter messages according to skip_messageid.

    if (skip_messageid == null) {
	r = this._messages;
    } else {
	for (i = 0; i < this._messages.length; i++) {
	    found = (this._messages[i].get_messageid() == skip_messageid);
	    if (found)
		break;
	}

	r = found ? this._messages.slice(i + 1) : null;
    }

    return r;
};

MessageBuffer.prototype.send_message = function(username, text)
{
    var message;

    // Store new message.
    // TODO: next_messageid will wraparound after 2^32 messages.

    message = new ChatService.Types.Message();
    message.set_messageid(this._next_messageid++);
    message.set_username(username);
    message.set_text(text);

    this._messages.push(message);

    // Delete old messages, if this._messages is large.

    if (this._messages.length > MAX_MESSAGES)
	this._messages.splice(0, 1);

    // Notify waiters about the new message.

    this._notify_waiters(this._waiterinfos, [message]);
};

MessageBuffer.prototype.add_waiter = function(waiter)
{
    var waiterinfo = new WaiterInfo(waiter);

    this._waiterinfos.push(waiterinfo);
};

MessageBuffer.prototype.remove_waiter = function(waiter)
{
    var i;
    var waiter2;

    for (i = 0; i < this._waiterinfos.length; i++) {
	waiter2 = this._waiterinfos[i].get_waiter();

	if (waiter == waiter2) {
	    this._waiterinfos.splice(i, 1);
	    break;
	}
    }
};

MessageBuffer.prototype._timeout_waiters = function()
{
    var ts = Date.now();
    var i = 0;
    var waiterinfos = [];
    var waiterinfo;

    // Remove waiters which have timeout.

    while (i < this._waiterinfos.length) {
	waiterinfo = this._waiterinfos[i];
	if (waiterinfo.has_timeout(ts)) {
	    this._waiterinfos.splice(i, 1);
	    waiterinfos.push(waiterinfo);
	} else {
	    i++;
	}
    }

    // Notify waiters with an empty message list.

    this._notify_waiters(waiterinfos, []);
};

MessageBuffer.prototype._notify_waiters = function(waiterinfos, messages)
{
    // Notify waiters.

    waiterinfos.forEach(function(waiterinfo) {
	var waiter = waiterinfo.get_waiter();

	waiter(messages);
    });

    // Remove waiters from list.

    waiterinfos.splice(0, waiterinfos.length);
};

// HTTP request handler class.

RequestHandler = function(req, resp, message_buffer)
{
    this._req = req;
    this._resp = resp;
    this._message_buffer = message_buffer;
};

RequestHandler.prototype.start = function()
{
    var found = false;

    switch (this._req.method) {
    case "POST":
	if (this._req.url == "/rpc") {
	    this._handle_rpc();
	    found = true;
	}
	break;

    case "GET":
	found = this._handle_static();
	break;
    }

    if (!found)
	this._handle_notfound();
};

RequestHandler.prototype._handle_static = function()
{
    var url = this._req.url;
    var fd = null;
    var filename;
    var st;
    var buf;
    var headers = {};

    if (url.indexOf("..") != -1) {
	// If the url contains "..", then refuse to serve static files.

	return false;
    }

    // "/" refers to index.html.

    if (url == "/")
	url += INDEX;

    filename = path.join(WWW_DIR, url);

    // Open, read and send static file to client.

    try {
	fd = fs.openSync(filename, "r");

	// Serve only regular files.

	st = fs.fstatSync(fd);
	if (!st.isFile())
	    throw new Error();

	buf = new Buffer(st.size);

	fs.readSync(fd, buf, 0, st.size, 0);
    } catch (e) {
	// TODO: Check exception type.

	return false;
    } finally {
	if (fd != null)
	    fs.closeSync(fd);
    }

    headers[CONTENT_TYPE] = MIMETYPES[path.extname(filename)];

    this._resp.writeHead(200, headers);
    this._resp.end(buf);

    return true;
};

RequestHandler.prototype._handle_notfound = function()
{
    var headers = {};

    headers[CONTENT_TYPE] = "text/html";

    this._resp.writeHead(404, headers);
    this._resp.end("<html><head><title>Not Found</title></head><body>The requested resource is not found.</body></html>");
};

// MyRPC<->HTTP interfacing

RequestHandler.prototype._handle_rpc = function()
{
    var that = this;

    // Read POST body.

    this._rbuf = new Buffer(0);

    this._req.on("data", function(buf) {
	that._rbuf = Buffer.concat([that._rbuf, buf]);
    });

    // Invoke MyRPC processor on received message.

    this._req.on("end", function() {
	var codec;
	var finished;

	that._tr = new myrpc.transport.MemoryTransport(new Uint8Array(that._rbuf));
	codec = new myrpc.codec.BinaryCodec();

	// Instantiate processor, IDL methods are implemented in RequestHandler.

	that._proc = new ChatService.Processor(that);

	finished = that._proc.process_one(that._tr, codec);
	if (finished) {
	    that._send_rpc_response();
	} else {
	    // If we are in a middle of async execution and the client closes
	    // HTTP connection, then remove waiter.

	    that._req.on("close", function() {
		if (that._waiter)
		    that._message_buffer.remove_waiter(that._waiter);
	    });
	}
    });
};

RequestHandler.prototype._send_rpc_response = function()
{
    var buf = this._tr.get_value();
    var headers = {};

    headers[CONTENT_TYPE] = "application/octet-stream";

    this._resp.writeHead(200, headers);
    this._resp.end(new Buffer(buf));

    this._waiter = null;
};

// RPC methods

RequestHandler.prototype.list_messages = function(skip_messageid)
{
    var messages = this._message_buffer.list_messages(skip_messageid);
    var r;

    if (!messages) {
	// If the client and server become desynced about messageids
	// (e.g. server is restarted), then signal client to refresh its
	// last_messageid.

	throw new ChatService.Types.UnknownMessageId();
    }

    if (messages.length > 0) {
	// If we have any messages, return them.

	r = messages;
    } else {
	// If we don't have any new messages, then subscribe to
	// new message event and enter async exection.

	this._waiter = myrpc.common.proxy(this._list_messages_waiter, this);
	this._message_buffer.add_waiter(this._waiter);

	r = myrpc.util.ProcessorNotFinished;
    }

    return r;
};

RequestHandler.prototype.send_message = function(username, text)
{
    this._message_buffer.send_message(username, text);
};

// Waiter implementation

RequestHandler.prototype._list_messages_waiter = function(messages)
{
    // Continue list_messages RPC method.

    this._proc.call_continue(function() {
	return messages;
    });

    this._send_rpc_response();
};

// Main program

if (process.argv.length != 3) {
    console.log("port should be specified");
    process.exit(1);
}

// Instantiate http server

// TODO: Check for 0-65535.
var port = parseInt(process.argv[2]);
if (isNaN(port)) {
    console.log("can't parse port");
    process.exit(1);
}

var message_buffer = new MessageBuffer();

var server = http.createServer(function(req, resp) {
    var reqhandler = new RequestHandler(req, resp, message_buffer);
    reqhandler.start();
});
server.setTimeout(0);
server.listen(port);

console.log("Serving requests on port " + port + "...");
