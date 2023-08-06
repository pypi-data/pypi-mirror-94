///////////////////////////////////
// 
// Reflection for Jupyter Notebooks
//
// Charles Varley, 2391564v
//
///////////////////////////////////


// Main communication setup function
function register_js_target() {
    Jupyter.notebook.kernel.comm_manager.register_target('client',
    function(comm, msg) {
        comm.on_msg(function(msg) { js_on_msg(msg) });
        comm.on_close(function(msg) { js_on_close(msg) });
    });
}


// Processing centre for custom messages...
function js_on_msg(msg) {
    var data = msg.content.data;
    var k = Object.keys(data)[0];
    switch (k) {
        case "update_nb":
            var nb = data[k];
            // Get cell data
            var cells_dict = make_cell_dict();
            var command = nb + "._update_cell_manager(" + JSON.stringify(cells_dict) + ")";
            make_execute_request(command);
            // Get prompt value of most recently executed cell (it cannot do it itself)
            var n = Jupyter.notebook.get_selected_index();
            var command = nb + "._set_cell_prompt(" + n + ")";
            make_execute_request(command);
            // Tell data manager to update the var dictionary
            var command = nb + "._update_data_manager()";
            make_execute_request(command);
            break;

        case "get_file_data":
            var nb = data[k];
            // Set initial metadata
            var data_dict = make_data_dict();
            var command = nb + "._set_file_data(" + JSON.stringify(data_dict) + ")";
            make_execute_request(command);            
            break;

        case "set_cells":
            var type = data[k]['ctype'];
            var text = data[k]['content'];
            var n    = data[k]['index'];
            var run  = data[k]['run'];
            if(Array.isArray(n)) {
                for(var i=0; i<n.length; i++) {
                    set_cell_type(n[i], type[i], false); // dont run cell yet
                    set_cell_content(n[i], text[i], run);    
                }
            }
            else {
                set_cell_type(n, type, false); // dont run cell yet
                set_cell_content(n, text, run);  
            }
            break; 

        case "insert_cells":
            var type = data[k]['ctype'];
            var text = data[k]['content'];
            var n    = data[k]['index'];
            var run  = data[k]['run'];
            // array of indices of cells to be run at the end   
            n_array = []; 
            // Either insert cell at the end of notebook file, or at some index n
            if(n === "end") {
                if(Array.isArray(type)) {
                    for(var i=0; i<type.length; i++) {
                        n_array.push(Jupyter.notebook.get_cells().length);
                        Jupyter.notebook.insert_cell_at_bottom(type[i]);
                    }
                }
                else {
                    n_array.push(Jupyter.notebook.get_cells().length); // Obtain number of cells
                    Jupyter.notebook.insert_cell_at_bottom(type);
                }
            }
            else {
                if(Array.isArray(type)) {
                    for(var i=0; i<type.length; i++) {
                        n_array.push(n+i); // n+i = i_start + i
                        Jupyter.notebook.insert_cell_at_index(type[i], n+i);
                    }
                }
                else {
                    n_array.push(n);
                    Jupyter.notebook.insert_cell_at_index(type, n);
                }
            } 
            // Write to cells once they have been placed in notebook
            set_cell_content(n_array, text, run);
            break;
        
        case "delete_cells":
            Jupyter.notebook.delete_cells(arrayify(data[k]));
            break;

        case "set_cell_attr":
            var attr = data[k]['attr'];
            var val  = data[k]['val'];
            var n    = data[k]['index'];
            var run  = data[k]['run'];
            switch(attr) {
                case "type":
                    set_cell_type(n, val, run);
                    break;
                case "content":
                    set_cell_content(n, val, run);
                    break;
                default:
                    console.log("Unexpected attribute given.");
            }
            break; 

        case "set_data_attr":
            var attr = data[k]['attr'];
            var val  = data[k]['val'];
            switch(attr) {
                case "filename":
                    Jupyter.notebook.notebook_name = val;
                    break;
                case "filepath":
                    Jupyter.notebook.notebook_path = val;
                    break;
                default:
                    console.log("Unexpected attribute given.");
            }

        // Failsafe for unanticipated events.
        default:
            console.log("Error: Unexpected key recieved.");
    }     
}


// Called when comm target is unregistered
function js_on_close(comm, msg) {
    console.log("Closing msg");
}


// Data retrieval functions
function make_cell_dict() {
    var cells = Jupyter.notebook.get_cells();
    var cell_dict = {};
    for(var i=0; i<cells.length; i++) {
        var cell = {};
        cell['ctype'] = cells[i].cell_type;
        cell['content'] = cells[i].get_text();
        cell_dict[i] = cell;
    }
    return cell_dict;
}

function make_data_dict() {
    var data = {}
    var seperator = '\\';
    if(navigator.platform.includes("Win")) 
        seperator = '/';
    
    // Filepath contains both filename and filepath info
    var filepath_split = Jupyter.notebook.notebook_path.split(seperator);
    data['filename'] = filepath_split[filepath_split.length-1];
    data['filepath'] = filepath_split.slice(0, -1).join(seperator);
    
    return data;
}


// Send message to shell
function make_execute_request(command) {
    var content = { 'code': command, 'silent': true, 'store_history': true, 
        'user_expressions': {}, 'allow_stdin': false, 'stop_on_error': false };
    var callbacks = {};
    var metadata = {'type': 'js_response'};
    var buffers = [];
    Jupyter.notebook.kernel.send_shell_message("execute_request", content, callbacks, metadata, buffers);
}


// Functions to change cell display data
function set_cell_type(n, type, run) {
    n_array = arrayify(n);
    switch(type) {
        case "code":
            Jupyter.notebook.cells_to_code(n_array);
            break;
        case "markdown":
            Jupyter.notebook.cells_to_markdown(n_array);
            break;
        default:
            console.log("Unexpected cell type given.");
    }
    if(run)
        Jupyter.notebook.execute_cells(n_array);
}

function set_cell_content(n, text, run) {
    n_array = arrayify(n);
    text_array = arrayify(text);
    for(var i=0; i<n_array.length; i++) {
        var cell = Jupyter.notebook.get_cell(n_array[i]); // get_cells() doesn't work for lists
        switch (cell.cell_type) {
            case "code":
                if(text_array.length === 1) 
                    cell.code_mirror.setValue(text_array[0]);
                else
                    cell.code_mirror.setValue(text_array[i]);
                break;  
            case "markdown":
                if(text_array.length === 1) 
                    cell.set_text(text_array[0]);
                else 
                    cell.set_text(text_array[i]);
                break;
            default:
                console.log("Unexpected cell type detected.");
        }
    }
    if(run)
        Jupyter.notebook.execute_cells(n_array);    
}


// Utility method to use the same code for single and listed values
function arrayify(n) {
    if(Array.isArray(n))
        return n;
    else
        return [n];
}