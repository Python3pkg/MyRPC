// Retry delay in case of error.
var ERROR_DELAY = (5 * 1000);
// Transport timeout (must be bigger than server MESSAGEBUFFER_WAITER_TIMEOUT).
var TRANSPORT_TIMEOUT = (120 * 1000);

var client_recv = null;
var client_send = null;
var last_messageid = null;

function init()
{
    // Instantiate two ChatService clients: one for receiving and one
    // for sending new messages.

    var url = "/rpc";

    var tr_recv = new myrpc.transport.HTTPClientTransport(url);
    var tr_send = new myrpc.transport.HTTPClientTransport(url);
    tr_recv.set_timeout(TRANSPORT_TIMEOUT);
    tr_send.set_timeout(TRANSPORT_TIMEOUT);

    var codec_recv = new myrpc.codec.BinaryCodec();
    var codec_send = new myrpc.codec.BinaryCodec();

    client_recv = new ChatService.Client(tr_recv, codec_recv);
    client_send = new ChatService.Client(tr_send, codec_send);

    // Call send() if you press enter in message textfield.

    var textelem = document.getElementById("textelem");
    textelem.addEventListener("keydown", function(ev) {
	if (ev.keyCode == 13)
	    send();
    });

    refresh();
}

function refresh()
{
    client_recv.list_messages(last_messageid, function(client) {
	var success = false;

	try {
	    var l = client.myrpc_continue();

	    // Display received messages.
	    // TODO: Remove old messages.

	    var messageselem = document.getElementById("messageselem");

	    l.forEach(function(message) {
		var divelem = document.createElement("div");

		var usernameelem = document.createElement("span");
		usernameelem.setAttribute("class", "username");
		var username = document.createTextNode("<" + message.get_username() + "> ");
		usernameelem.appendChild(username);

		var textelem = document.createElement("span");
		var text = document.createTextNode(message.get_text());
		textelem.appendChild(text);

		divelem.appendChild(usernameelem);
		divelem.appendChild(textelem);
		messageselem.appendChild(divelem);
	    });

	    // Scroll to bottom and update last_messageid if we have received
	    // at least one new message.

	    var llen = l.length;

	    if (llen > 0) {
		messageselem.scrollTop = messageselem.scrollHeight;
		last_messageid = l[llen - 1].get_messageid();
	    }

	    success = true;
	} catch (e) {
	    // Exception handling for client.myrpc_continue().

	    if (e instanceof ChatService.Types.UnknownMessageId) {
		// last_messageid is desynced, refresh entire message list.

		var messageselem = document.getElementById("messageselem");
		while (messageselem.firstChild)
		    messageselem.removeChild(messageselem.firstChild);

		last_messageid = null;
		success = true;
	    } else if (e instanceof myrpc.transport.TransportException) {
		// HTTP connection problem, ignore it and retry.
	    } else if (e instanceof myrpc.common.ServerErrorException) {
		var msg = e.get_msg();

		alert("Server error reply: " + msg);
	    } else if (e instanceof myrpc.common.MyRPCException) {
		var msg = e.get_msg();

		alert("MyRPC client error: " + msg);
	    } else {
		// Can't handle exception, propagate it further.

		throw e;
	    }
	}

	if (success)
	    refresh();
	else
	    setTimeout(refresh, ERROR_DELAY);
    });
}

function send()
{
    var username = document.getElementById("usernameelem").value;
    var textelem = document.getElementById("textelem");
    var text = textelem.value;

    if (username == "" || text == "") {
        alert("Please type in an username and a message.");
        return;
    }

    enable_button(false);

    client_send.send_message(username, text, function(client) {
	try {
	    client.myrpc_continue();

	    // Clear message input field on success.

	    textelem.value = "";
	} catch (e) {
	    // Exception handling for client.myrpc_continue().

	    if (e instanceof myrpc.common.ServerErrorException) {
		var msg = e.get_msg();

		alert("Server error reply: " + msg);
	    } else if (e instanceof myrpc.common.MyRPCException) {
		var msg = e.get_msg();

		alert("MyRPC client error: " + msg);
	    } else {
		// Can't handle exception, propagate it further.

		throw e;
	    }
	} finally {
            enable_button(true);
	}
    });
}

function enable_button(b)
{
    var sendelem = document.getElementById("sendelem");
    sendelem.disabled = !b;
}
