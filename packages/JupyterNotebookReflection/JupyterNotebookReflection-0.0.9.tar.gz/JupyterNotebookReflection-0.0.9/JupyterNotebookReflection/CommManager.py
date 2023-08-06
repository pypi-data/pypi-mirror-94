###################################
# 
# Reflection for Jupyter Notebooks
#
# Charles Varley, 2391564v
#
###################################


from IPython.core.getipython import get_ipython
from IPython.display import display, Javascript
from ipykernel.comm import Comm

from inspect import currentframe, getframeinfo
from ast import parse


class CommManager():
    def __init__(self):
        # Set up framework for communications with the client server
        self.__create_js_target()
        self.__comm = Comm(target_name='client')
        self.__setup_events()
        self.__get_id()
        
    
    # Create a target on the frontend to send messages to.
    def __create_js_target(self):
        display(Javascript("register_js_target();"))


    # Obtain name of JupyterNotebook instance.
    def __get_id(self):
        frame = currentframe().f_back.f_back.f_back
        context = getframeinfo(frame).code_context
        
        for line in context:
            if "JupyterNotebook()" in line:
                ast_node = parse(line)
                self._id = ast_node.body[0].targets[0].id
                return


    # Main function to communicate with the client server, messages to be processed in JS.
    def send_msg(self, msg):
        self.__comm.send(msg)


    # Register custom methods with IPython shell's event cycle.
    def __setup_events(self):
        #get_ipython().events.register('pre_execute', self.__update_cells)
        #get_ipython().events.register('pre_run_cell', self.__update_cells)
        #get_ipython().events.register('post_execute', self.__update_cells)
        get_ipython().events.register('post_run_cell', self.__update_nb_data)


    # Update saved state of notebook cells, to be invoked by shell.
    def __update_nb_data(self):
        self.send_msg({"update_nb": self._id})

    
    def get_file_data(self):
        self.send_msg({"get_file_data": self._id})