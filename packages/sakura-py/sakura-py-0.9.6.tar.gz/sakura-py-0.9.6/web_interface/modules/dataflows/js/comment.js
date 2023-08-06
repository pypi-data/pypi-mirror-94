//Code started by Michael Ortega for the LIG
//May 9th, 2017

function context_new_comment() {
    $('#sakura_main_div_contextMenu').css({visibility: "hidden"});
    new_comment();
}


function new_comment() {
    var wrapper = document.createElement('div');
    var id = 0;
    var found = false;
    while (! found) {
        if (index_from_comment_id(id) != -1) {
            id ++
        }
        else {
            found = true;
        }
    }

    load_from_template(
                    wrapper,
                    "comment.html",
                    {'id': id, 'title': "Comment "+id, 'body': "Edit your comment here"},
                    function () {
                        var com         = wrapper.firstChild;
                        com.style.left  = ''+(cursorX - df_main_div().offset().left - 90)+'px';
                        com.style.top   = ''+(cursorY - df_main_div().offset().top)+'px';
                        com.setAttribute("draggable", "true");
                        df_main_div().append(com);

                        $('#comment_'+id+'_title').blur( function (e) {
                            save_dataflow();
                        });
                        $('#comment_'+id+'_body').blur( function (e) {
                            save_dataflow();
                        });

                        global_coms.push({  'id': id,
                                            'div': com});
                        save_dataflow();
                    }
    );
}


function comment_from(com) {
    let wrapper = document.createElement('div');
    let body = com.body.replace(/<br>/g, '\n');
    let title = com.title.replace(/<br>/g, '\n');

    load_from_template(
                    wrapper,
                    "comment.html",
                    {'id': com.id, 'title': title, 'body': body},
                    function () {
                        var ncom             = wrapper.firstChild;
                        ncom.style.left      = com.left;
                        ncom.style.top       = com.top;
                        ncom.style.width     = com.width;
                        ncom.style.height    = com.height;
                        ncom.setAttribute("draggable", "true");

                        df_main_div().append(ncom);

                        $('#comment_'+com.id+'_title').blur( function (e) {
                            save_dataflow()
                        });

                        $('#comment_'+com.id+'_body').html(com.body);
                        $('#comment_'+com.id+'_body').blur( function (e) {
                            save_dataflow()
                        });

                        global_coms.push({  'id': parseInt(com.id),
                                            'div': ncom});

                        //This is for capturing resizing event
                        $('#comment_'+com.id).on('click', function(){
                            save_dataflow()
                        });
                    }
    );
}


function get_comment_info(com) {
    return {'id': com.id,
            'title':    $('#comment_'+com.id+'_title').html(),
            'body':     $('#comment_'+com.id+'_body').html(),
            'left':     com.div.style.left,
            'top':      com.div.style.top,
            'width':    com.div.style.width,
            'height':   com.div.style.height
            };
}


function remove_comment(id) {
    $(comment_from_id(id).div).remove();
    global_coms.splice(index_from_comment_id(id), 1);
    save_dataflow();
}

function index_from_comment_id(id) {
    return global_coms.findIndex( function (e) {
        return e.id === id;
    });
}


function comment_from_id(id) {
    return global_coms.find( function (e) {
        return e.id === id;
    });
}
