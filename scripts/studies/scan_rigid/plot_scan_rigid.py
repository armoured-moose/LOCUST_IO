#plot_scan_rigid.py
 
"""
Samuel Ward
03/08/20
----
script for plotting rigid rotation 
---
 
notes:         
---
"""

###################################################################################################
#Preamble
 
import sys #have global imports --> makes less modular (no "from input_classes import x") but best practice to import whole input_classes module anyway

try:
    import numpy as np
    import pathlib
    import copy
    import matplotlib.pyplot as plt
    import sys
except:
    raise ImportError("ERROR: initial modules could not be imported!\nreturning\n")
    sys.exit(1)

if __name__=='__main__':

    try:
        import context
    except:
        raise ImportError("ERROR: context.py could not be imported!\nreturning\n")
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
    import support
except:
    raise ImportError("ERROR: LOCUST_IO/src/support.py could not be imported!\nreturning\n") 
    sys.exit(1)
try:
    import constants
except:
    raise ImportError("ERROR: LOCUST_IO/src/constants.py could not be imported!\nreturning\n") 
    sys.exit(1)
try:
    import settings
except:
    raise ImportError("ERROR: LOCUST_IO/src/settings.py could not be imported!\nreturning\n") 
    sys.exit(1)

################################################################## 
#Main 

import scan_rigid_launch as batch_data

def get_output_files(output_type='dfn'):

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
                outputs.append(output_classes_dispatch[output_type](ID=parameter_string,data_format='LOCUST',filename=dir_output_filepath))
        else:
            outputs.append(None)

    return outputs

outputs=get_output_files('rund')

for plasma_state_counter,(Pr,tftE) in enumerate(zip(batch_data.parameters__kinetic_profs_Pr,batch_data.parameters__kinetic_profs_tF_tE)):

    scan_range=len(batch_data.parameters__phases_upper)
    plasma_state_slice=slice(plasma_state_counter*scan_range,(plasma_state_counter+1)*scan_range)
    global_phase_shift=batch_data.parameters__phases_upper
    PFC_power=np.array([output['PFC_power']['total'] if (output is not None and output['run_status']=='completed') else -10. for output in outputs[plasma_state_slice]])

    relative_phases_upper_middle=batch_data.parameters__phases_upper-batch_data.parameters__phases_middle
    relative_phases_upper_lower=batch_data.parameters__phases_upper-batch_data.parameters__phases_lower

    fig,ax=plt.subplots(1)
    ax.scatter(batch_data.parameters__phases_upper,PFC_power/1.e6)
    ax.set_xlabel('Absolute rigid phase $\mathrm{d}\Phi$')
    ax.set_ylabel('PFC power flux [MW]$')
    ax.set_title(f'relative phase U:M={relative_phases_upper_middle[0]}, U:L={relative_phases_upper_lower[0]}')
    plt.show()

#################################
 
##################################################################
 
###################################################################################################