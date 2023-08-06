###################################
# 
# Reflection for Jupyter Notebooks
#
# Charles Varley, 2391564v
#
###################################


from IPython.core.getipython import get_ipython
import types


class DataManager():
    ''' A class to manage the storage and manipulation of data relevant to a notebook document. '''
    def __init__(self):
        # Create an exclusion list of variables defined by IPython and JupyterNotebook itself.
        self._exclude_list = ['In', 'Out', 'get_ipython', 'exit', 'quit', 'Cell']
        initial_vars = get_ipython().ns_table['user_global']
        self._exclude_list += [v for v in initial_vars.keys() if v.startswith('_') or v.startswith('@')]
        self._exclude_list += [v for v in initial_vars.values() if type(v) == types.ModuleType]
        # Dictionary of user-defined variables.
        self._nb_vars = {}
        self._metadata = {"filename": "", "filepath": ""}

    @property
    def nb_vars(self):
        return self._nb_vars

    @nb_vars.setter
    def nb_vars(self, v):
        if type(v) is not dict:
            raise TypeError(f"Var dictionary must be of type dict, got: {type(v)}")
        self._nb_vars = v
        

    # Update function, invoked by JS.
    def _update_nb_vars(self):
        new_dict = {k:v for k,v in get_ipython().ns_table['user_global'].items() if k not in self._exclude_list}
        # Filter out cell input/output entries added by shell
        for k in list(new_dict.keys()):
            if k.startswith("_i"):
                # Get corresponding output key
                out_k = "_" + k[2:] 
                # Remove input/output entries from dict
                new_dict.pop(k)
                if out_k in new_dict: # sometimes shell won't produce an output
                    new_dict.pop(out_k)
                # Add input/output keys to exlude list
                self._exclude_list.append(k) 
                self._exclude_list.append(out_k)
        self.nb_vars = new_dict
   
    def _set_metadata(self, data):
        for d in data.keys():
            if d in self._metadata:
                self._metadata[d] = data[d]


    # Data manipulation functions.
    def set_var(self, var, val):
        if var not in self.nb_vars:
            raise KeyError(f"Variable not recognised, got: {var}")
        if type(var) is not str:
            raise TypeError(f"Variable name must be passed as a string, got: {type(var)}")
        # Set variable value in shell
        get_ipython().ns_table['user_global'][var] = val
        # Set variable value in io manager 
        self.nb_vars[var] = val  

    def get_metadata_attr(self, attr):
        if attr not in self._metadata:
            raise KeyError(f"Attribute not recognised, got: {attr}")
        if type(attr) is not str:
            raise TypeError(f"Metadata attributes need to be string, got: {type(attr)}")
        return self._metadata[attr]

    def set_metadata_attr(self, attr, val):
        if attr not in self._metadata:
            raise KeyError(f"Attribute not recognised, got: {attr}")
        if type(attr) is not str:
            raise TypeError(f"Metadata attributes need to be string, got: {type(attr)}")
        if type(val) is not str:
            raise TypeError(f"Metadata values need to be string, got: {type(attr)}")
        self._metadata[attr] = val


    # Print out notebook data.
    def dump(self):
        for k in self._metadata.keys():
            print(f"{k.capitalize()}: {self._metadata[k]}")
        print("\n")