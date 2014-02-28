var client = null;
var last_imgid = null;

function init()
{
    // Instantiate GalleryService client.

    var tr = new myrpc.transport.HTTPClientTransport("/rpc");
    var codec = new myrpc.codec.BinaryCodec();

    client = new GalleryService.Client(tr, codec);

    refresh();
}

function refresh()
{
    enable_button(false);

    // Query list of images and display them.

    client.list_image_info(last_imgid, function() {
	try {
	    // This function is called when the RPC call is finished. According
	    // to the IDL, list_image_info returns with a list of ImageInfo elements.
	    // By calling client.myrpc_continue() we can retrieve this list.

	    var l = client.myrpc_continue();

	    var listelem = document.getElementById("listelem");

	    l.forEach(function(info) {
		var imgid = info.get_imgid();
		var thumb_width = info.get_thumb_width();
		var thumb_height = info.get_thumb_height();

		// Append new images to DOM tree.

		var aelem = document.createElement("a");
		aelem.setAttribute("href", "/normal_img/" + imgid);

		var imgelem = document.createElement("img");
		imgelem.setAttribute("src", "/thumb_img/" + imgid);
		imgelem.setAttribute("width", thumb_width);
		imgelem.setAttribute("height", thumb_height);

		aelem.appendChild(imgelem);
		listelem.appendChild(aelem);

		// Update last imgid.

		if (last_imgid == null || imgid > last_imgid)
		    last_imgid = imgid;
	    });
	} catch (e) {
	    // Exception handling for client.myrpc_continue().

	    if (e instanceof myrpc.common.ServerErrorException) {
		var msg = e.get_msg();

		alert("Server reply: " + msg);
	    } else if (e instanceof myrpc.common.MyRPCException) {
		var msg = e.get_msg();

		alert("MyRPC client error: " + msg);
	    } else {
		// Can't handle exception, throw it further.

		throw e;
	    }
	} finally {
	    enable_button(true);	    
	}
    });
}

function upload()
{
    var file = document.getElementById("fileelem").files[0];
    if (!file) {
	alert("Please select an image file.");
	return;
    }

    var reader = new FileReader();
    reader.onload = function() {
	// Create Uint8Array view on the contents of reader result.

	var buf = reader.result;
	var imgbuf = new Uint8Array(buf);

	enable_button(false);

	client.upload_image(imgbuf, function() {
	    try {
		// upload_image doesn't have return value, but can throw
		// exceptions, see catch below (UnknownFormat, SizeTooLarge).

		client.myrpc_continue();

		// If image upload is successful, then refresh our image list.

		refresh();
	    } catch (e) {
		// Exception handling for client.myrpc_continue().

		if (e instanceof GalleryService.Types.UnknownFormat) {
		    alert("GalleryService reply: Image format is unknown");
		} else if (e instanceof GalleryService.Types.SizeTooLarge) {
		    var max_width = e.get_max_width();
		    var max_height = e.get_max_height();

		    alert("GalleryService reply: Image dimesions are too large (max size: " + max_width + "x" + max_height + ")");
		} else if (e instanceof myrpc.common.ServerErrorException) {
		    var msg = e.get_msg();

		    alert("Server reply: " + msg);
		} else if (e instanceof myrpc.common.MyRPCException) {
		    var msg = e.get_msg();

		    alert("MyRPC client error: " + msg);
		} else {
		    // Can't handle exception, throw it further.

		    throw e;
		}
	    } finally {
		enable_button(true);
	    }
	});
    };
    reader.onerror = function() {
	alert("FileReader error: " + reader.error);
    };
    reader.readAsArrayBuffer(file);
}

function enable_button(b)
{
    var buttonelem = document.getElementById("buttonelem");
    buttonelem.disabled = !b;
}
