#plot_mod.py
 
"""
Samuel Ward
12/08/20
----
plotting helpers
---
 
notes:
---
"""

###################################################################################################
#Preamble

import sys #have global imports --> makes less modular (no "from input_classes import x") but best practice to import whole input_classes module anyway
try:
    import numpy as np 
    import os
    import pathlib
except:
    raise ImportError("ERROR: initial modules could not be imported!\nreturning\n")
    sys.exit(1)

try:
    from classes.output_classes.distribution_function import Distribution_Function as dfn
except:
    raise ImportError("ERROR: LOCUST_IO/src/classes/output_classes/distribution_function.py could not be imported!\nreturning\n")
    sys.exit(1)
try:
    from classes.output_classes.particle_list import Final_Particle_List as fpl
except:
    raise ImportError("ERROR: LOCUST_IO/src/classes/output_classes/distribution_function.py could not be imported!\nreturning\n")
    sys.exit(1)
try:
    from classes.output_classes.rundata import Rundata as rund
except:
    raise ImportError("ERROR: LOCUST_IO/src/classes/output_classes/distribution_function.py could not be imported!\nreturning\n")
    sys.exit(1)

try:
    import settings
except:
    raise ImportError("ERROR: LOCUST_IO/src/settings.py could not be imported!\nreturning\n") 
    sys.exit(1)
try:
    import support
except:
    raise ImportError("ERROR: LOCUST_IO/src/support.py could not be imported!\nreturning\n") 
    sys.exit(1)

################################################################## 
#Main 

def get_output_files(batch_data,output_type='dfn'):

    outputs=[]
    output_file_dispatch={}
    output_file_dispatch['dfn']='*.dfn'
    output_file_dispatch['fpl']='ptcl_cache.dat'
    output_file_dispatch['rund']='rundata*_1'

    output_classes_dispatch={}
    output_classes_dispatch['dfn']=dfn
    output_classes_dispatch['fpl']=fpl
    output_classes_dispatch['rund']=rund

    for parameter_string,dir_output in zip(batch_data.parameter_strings,batch_data.args_batch['LOCUST_run__dir_output']): #within each GPU folder the path to each output is the same
        dir_output=pathlib.Path(dir_output.strip("\'"))
        dir_output_filepaths=list(dir_output.glob(output_file_dispatch[output_type])) #get all filenames for runs corresponding to this choice of parameters    
        if dir_output_filepaths:
            for dir_output_filepath in dir_output_filepaths:
                try:
                    yield output_classes_dispatch[output_type](ID=parameter_string,data_format='LOCUST',filename=dir_output_filepath)
                except:
                    yield None
        else:
            yield None

#################################
 
##################################################################

###################################################################################################