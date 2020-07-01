#plot_current_scan.py
 
"""
Samuel Ward
28/05/20
----
script resolution scan
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

import scan_current_n3_n6_launch as batch_data

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

outputs=get_output_files('fpl')

fig,ax=plt.subplots(1)
for output,col_val in zip(outputs,np.linspace(0,1,len(outputs))):
    if output: output.plot(fig=fig,ax=ax,axes=['time'],fill=False,label=output.ID,colmap=settings.cmap_default,colmap_val=col_val,number_bins=200,weight=True)
ax.legend()
plt.show()
fig,ax=plt.subplots(1)
for output,col_val in zip(outputs,np.linspace(0,1,len(outputs))):
    if output: output.plot(fig=fig,ax=ax,axes=['E'],fill=False,label=output.ID,colmap=settings.cmap_default,colmap_val=col_val,number_bins=200,weight=True)
ax.legend()
plt.show()

outputs=get_output_files('dfn')

fig,ax=plt.subplots(1)
for output,col_val in zip(outputs,np.linspace(0,1,len(outputs))):
    if output: output.plot(fig=fig,ax=ax,axes=['R'],label=output.ID,colmap=settings.cmap_default,colmap_val=col_val,number_bins=200)
ax.legend()
plt.show()

outputs=get_output_files('rund')

for counter,output in enumerate(outputs): #remove the 2D comparison case I put in there
    if 'B3D_EX' not in batch_data.args_batch['LOCUST_run__flags'][counter]:
        
        rundata_2D=output  
        del(outputs[counter])
        batch_data.parameters__currents_upper=np.delete(batch_data.parameters__currents_upper,0)

PFC_power=np.array([output['PFC_power']['total'] if output is not None else -10. for output in outputs ])
fig,ax=plt.subplots(1)
ax.plot(batch_data.parameters__currents_upper/1000.,PFC_power/np.max(PFC_power),color='b',marker='x',linestyle='-',label='3D cases')
ax.axhline(rundata_2D['PFC_power']['total']/np.max(PFC_power),color='red',label='2D case')
ax.set_xlabel("Coil current [kAt]")
ax.set_ylabel("Normalised PFC power flux")
ax.legend()
plt.show()

#################################
 
##################################################################
 
###################################################################################################