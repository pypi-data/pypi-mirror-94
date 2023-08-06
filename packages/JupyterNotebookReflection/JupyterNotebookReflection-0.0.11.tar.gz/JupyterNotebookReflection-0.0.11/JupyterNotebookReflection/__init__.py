###################################
# 
# Reflection for Jupyter Notebooks
#
# Charles Varley, 2391564v
#
###################################


from IPython.display import display, Javascript, HTML
from os import path

from .CellManager import CellManager, Cell
from .CommManager import CommManager
from .DataManager import DataManager


class JupyterNotebook():
    '''
    A class to operate as the interface between user and implementation of reflective-capable features, 
    contains manager objects that process the requests made by the user. 

    A JupyterNotebook instance MUST be created in its own seperate cell before and reflective operations can be performed.

    Eg:

        Cell 1:
            my_nb = JupyterNotebook()

        Cell 2:
            my_nb.get_cells()
            ...
    '''
    def __init__(self):
        # Load JS file to notebook, allows for all scripts to access JS functionality
        module_directory = path.abspath(path.dirname(__file__))
        js_data = open(path.join(module_directory, 'Client.js')).read()
        display(HTML(f"<script type='text/javascript'>{js_data}</script>"))
        # Set up managers
        self._data_mgr = DataManager()
        self._cell_mgr = CellManager()
        self._comm_mgr = CommManager()
        # Save initial metadata state
        self._comm_mgr.get_file_data()


    # Functions to be called by JS.
    def _update_cell_manager(self, cell_dict):
        self._cell_mgr._update_cells(cell_dict)

    def _set_cell_prompt(self, i):
        self._cell_mgr._update_cell_prompt(i)
    
    def _update_data_manager(self):
        self._data_mgr._update_nb_vars()

    def _set_file_data(self, data):
        self._data_mgr._set_metadata(data)


    # General functions.
    def make_cell(self, ctype="code", content="", auto=False):
        ''' Creates an instance of a blank Cell object. '''
        return Cell(ctype, content, auto_execute=auto)
    
    def cell_count(self):
        ''' Returns the number of cells existing in current notebook context. '''
        return len(self._cell_mgr.cells)

    def source_code(self, i_list=None):
        ''' 
        Returns the state of the executed code cells in current notebook context .
        
        input:
            i_list = a list of cell indices to restrict the range of source code with.
                     (can be omitted for the source code of the entire notebook)
        '''
        return self._cell_mgr.source_code(i_list)

    def dump(self):
        ''' Prints a statement about the current notebook context to output box of current cell. '''
        self._data_mgr.dump()
        self._cell_mgr.dump()

    def _check_run(self, r):
        if type(r) is not bool:
            raise TypeError(f"Run argument is not a boolean, got: {type(r)}")

    # Cell manipulation functions.
    def get_cell(self, i):
        ''' 
        Returns Cell instance of currently held cell at index i.
        
        throws:
            IndexError, when index is negative or over the number of cells currently available.
            TypeError, when index is not an int.
        '''
        if type(i) is list:
            raise TypeError("Use get_cells([indices]) to obtain multiple cell instances.")
        else:
            return self._cell_mgr.get_cell(i)

    def get_cells(self, i_list=None):
        ''' 
        Returns a tuple of Cell instances held at indices defined by i list.
        (can be omitted for all Cell instances in current notebook context)   

        throws:
            IndexError, when indices are negative or over the number of cells currently available.
            TypeError, when indices are not ints. 
         '''
        if (type(i_list) is int) or ((type(i_list) is list) and (len(i_list) == 1)):
            raise ValueError("Use get_cell(index) to obtain a single cell instance.")
        elif i_list == None:
            return self._cell_mgr.cells
        else:
            return tuple(self._cell_mgr.get_cells(i_list))
        
    def set_cell(self, cell, i, run=True):
        '''
        Set a cell at index i.

        input:
            run = Should the cell be executed when it is set?

        throws:
            TypeError, when cell is not a Cell object.
            IndexError, when index is negative or over the number of cells currently available.
            TypeError, when index is not an int.
        '''
        self._check_run(run)
        if type(i) is list:
            raise TypeError("Use set_cells([indices]) to set multiple cell instances.")
        else:
            self._cell_mgr.set_cell(cell, i, run)
            self._comm_mgr.send_msg({"set_cells": {"ctype": cell.ctype, "content": cell.content, 
                                                "index": i, "run": 1 if run else 0 }})
    
    def set_cells(self, cell_list, i_list, run=True):
        '''
        Set cells at indices defined by i_list.

        input:
            run = Should the cells be executed when they are set?

        throws:
            TypeError, when cells are not Cell objects.
            IndexError, when indices are negative or over the number of cells currently available.
            TypeError, when indices are not ints. 
            AttributeError, when cell_list and i_list ar enot the same length.
            TypeError, when both cell_list and i_list are not lists.
        '''
        self._check_run(run)
        if (type(i_list) is int) or ((type(i_list) is list) and (len(i_list) == 1)):
            raise ValueError("Use set_cell(index) to set a single cell instance.")
        else:
            self._cell_mgr.set_cells(cell_list, i_list, run)
            self._comm_mgr.send_msg({"set_cells": {"ctype": [c.ctype for c in cell_list], 
                                                "content": [c.content for c in cell_list], 
                                                "index": i_list, "run": 1 if run else 0 }})

    def insert_cell(self, cell, i=None, run=True):
        '''
        Insert a cell at index i.

        input: 
            i = The index to insert cell at. (Can be omitted to insert at the end of notebook)
            run = Should the cell be executed when it is set?

        throws:
            TypeError, when cell is not a Cell object.
            IndexError, when index is negative or over the number of cells currently available.
            TypeError, when index is not an int.
            
        '''
        self._check_run(run)
        if type(cell) is list:
            raise TypeError("Use insert_cells([cells], index_start) to insert multiple cell instances.")
        else:
            self._cell_mgr.insert_cell(cell, i, run)
            self._comm_mgr.send_msg({"insert_cells": {"ctype": cell.ctype, "content": cell.content, 
                                                    "index": i if i is not None else "end", 
                                                    "run": 1 if run else 0 }})

    def insert_cells(self, cell_list, i_start=None, run=True):
        '''
        Insert a cells starting at index i.

        input: 
            i = The start index to insert cells at. (Can be omitted to insert at the end of notebook)
            run = Should the cells be executed when they are set?

        throws:
            TypeError, when cells are not Cell objects.
            IndexError, when index is negative or over the number of cells currently available.
            TypeError, when index is not an int.
            AttributeError, when cell_list and i_list ar enot the same length.
            TypeError, when both cell_list and i_list are not lists.
        '''
        self._check_run(run)
        if (type(cell_list) is Cell) or ((type(cell_list) is list) and (len(cell_list) == 1)):
            raise ValueError("Use insert_cell(cell, index) to insert a single cell instance.")
        self._cell_mgr.insert_cells(cell_list, i_start, run)
        self._comm_mgr.send_msg({"insert_cells": {"ctype": [c.ctype for c in cell_list], 
                                                  "content": [c.content for c in cell_list],  
                                                  "index": i_start if i_start is not None else "end", 
                                                  "run": 1 if run else 0 }})
        
    def delete_cell(self, i):
        '''
        Remove cell at index i.

        throws:
            IndexError, when index is negative or over the number of cells currently available.
            TypeError, when index is not an int.
        '''
        if type(i) is list:
            raise TypeError("Use delete_cells([indices]) to delete multiple cell instances.")
        else:
            self._cell_mgr.delete_cell(i)
            self._comm_mgr.send_msg({"delete_cells": i})

    def delete_cells(self, i_list):
        '''
        Remove cells at indices defined by i_list.

        throws:
            IndexError, when index is negative or over the number of cells currently available.
            TypeError, when index is not an int.
        '''
        if (type(i_list) is int) or ((type(i_list) is list) and (len(i_list) == 1)):
            raise ValueError("Use delete_cell(index) to delete a single cell instance.")
        else:
            self._cell_mgr.delete_cells(i_list)
            self._comm_mgr.send_msg({"delete_cells": i_list})

    def set_cell_type(self, ctype, i, run=True):
        '''
        Set the cell type of the cell at index i.

        input:
            ctype = A string value of a supported cell type.
            run = Should the cells be executed when they are set?

        throws:
            ValueError, when ctype argument isn't supported by notebook.
            TypeError, when ctype isn't a string.
            IndexError, when index is negative or over the number of cells currently available.
            TypeError, when index is not an int.
        '''
        self._check_run(run)
        self._cell_mgr.set_cell_type(ctype, i, run)
        self._comm_mgr.send_msg({"set_cell_attr": {"attr": "type", "val": ctype, "index": i, 
                                                   "run": 1 if run else 0 }})

    def set_cell_content(self, content, i, run=True):
        '''
        Set the content of cell at index i.

        input:
            run = Should the cells be executed when they are set?

        throws:
            TypeError, when content isn't a string.
            IndexError, when index is negative or over the number of cells currently available.
            TypeError, when index is not an int.
        '''
        self._check_run(run)
        self._cell_mgr.set_cell_content(content, i, run)
        self._comm_mgr.send_msg({"set_cell_attr": {"attr": "content", "val": content, "index": i, 
                                                   "run": 1 if run else 0 }})

    def append_to_cell(self, content, i, run=True):
        '''
        Add to the end of the content of cell at index i.

        input:
            run = Should the cells be executed when they are set?

        throws:
            TypeError, when content isn't a string.
            IndexError, when index is negative or over the number of cells currently available.
            TypeError, when index is not an int.
        '''
        self._check_run(run)
        self._cell_mgr.append_to_cell(content, i)
        self._comm_mgr.send_msg({"set_cell_attr": {"attr": "content", "val": self._cell_mgr.cells[i].content, 
                                                   "index": i, "run": 1 if run else 0 }})


    # Data manipulation functions.
    def get_vars(self):
        ''' Get the user-defined variables in current notebook context. ''' 
        return self._data_mgr.nb_vars

    def set_var(self, var, val):
        '''
        Set a user-defiend variable in current notebook context.

        throws:
            KeyError, when variable argument isn't already defined in notebook context.
            TypeError, when variable argument isn't a string. 
        '''
        self._data_mgr.set_var(var, val)

    def get_filename(self):
        ''' Get filename of current notebook context.'''
        return self._data_mgr.get_metadata_attr('filename')

    def get_filepath(self):
        ''' Get filepath of current notebook context. '''
        return self._data_mgr.get_metadata_attr('filepath')