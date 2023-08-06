//Code started by Michael Ortega for the LIG
//October 10th, 2016

function open_dataflow() {
    if (! jsPlumbLoaded)
      $.getScript("/webcache/cdnjs/jsPlumb/2.1.7/jsPlumb.min.js").done( function() {
          jsPlumbLoaded = true;
          current_dataflow();
      });
    else
        current_dataflow();
}

function jsPlumb_init() {
    ///////////////DEFAULTS
    let jsplumb_instance = jsPlumb.getInstance({
        PaintStyle : { lineWidth : 3, strokeStyle : "#333333" },
        MaxConnections : 100,
        Endpoint : ["Dot", {radius:6, zindex:20}],
        EndpointStyle : { fillStyle:"black" }
    });

    ///////////////LINKS EVENTS
    //This piece of code is for preventing two or more identical links
    jsplumb_instance.bind("beforeDrop", function(connection) {
        var found = link_exist( parseInt(connection.sourceId.split("_")[2]),
                                parseInt(connection.targetId.split("_")[2]));
        //we test the link existence from our side
        if (found == true) {
            console.log("link already exists !");
            jsplumb_instance.detach(connection);
            jsplumb_instance.repaintEverything();
            return false;
        }
        //here we validate the jsPlumb link creation
        return true;
    });

    // jsplumb_instance.bind("connectionDragStop", function (connection) {
    //     console.log('CONN_DRAG_STOP');
    // });

    //A connection is established
    jsplumb_instance.bind("connection", function(conn) {
        //link creation on hub and other
        //link existence is tested with 'beforeDrop' event
        if (global_dataflow_jsFlag) {
                create_link(  conn.connection,
                              parseInt(conn.sourceId.split("_")[2]),
                              parseInt(conn.targetId.split("_")[2])   );
        }
    });

    //When the target of a link changes
    jsplumb_instance.bind("connectionMoved", function(params) {
    });

    jsplumb_instance.bind("beforeDetach", function (e) {
        if (LOG_INTERACTION_EVENT) {console.log('BEFORE DETACH');}
        //return false; //WARNING !!! Keep this for avoiding deleting connections
    });

    //On double click we open the link parameters
    jsplumb_instance.bind("dblclick", function(connection) {
        open_link_params(connection.id);
    });

    //Context Menu is one of the ways for deleting the link
    jsplumb_instance.bind("contextmenu", function(params, e) {
        e.preventDefault();
        $('#sakura_link_contextMenu').css({
            display: "block",
            left: e.clientX,
            top: e.clientY
        });
        link_focus_id = link_from_id(params.id);
    });
    return jsplumb_instance;
}
