#plot_difference.py
 
"""
Samuel Ward
24/02/20
----
script for plotting difference between outputs with/without extrapolated profiles
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
    from matplotlib.animation import FuncAnimation
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

import compare_extrapolated_profiles_launch as batch_data

axes=['R','Z']
xmin=0
xmax=0
ymin=0
ymax=0


def get_output_files(output_type='dfn'):

    outputs=[]
    output_file_dispatch={}
    output_file_dispatch['dfn']='*.dfn'
    output_file_dispatch['fpl']='ptcl_cache.dat'

    output_classes_dispatch={}
    output_classes_dispatch['dfn']=dfn
    output_classes_dispatch['fpl']=fpl

    for parameter_string,dir_output in zip(batch_data.parameter_strings,batch_data.args_batch['LOCUST_run__dir_output']): #within each GPU folder the path to each output is the same
        print(dir_output)
        dir_output=pathlib.Path(dir_output.strip("\'")).parents[0]
        print(dir_output)
        for parent_folder in dir_output.glob('*'):
            dir_output_filepaths=list(parent_folder.glob(output_file_dispatch[output_type])) #get all filenames for runs corresponding to this choice of parameters    
            print(dir_output_filepaths)
            if dir_output_filepaths:
                for dir_output_filepath in dir_output_filepaths:
                    outputs.append(output_classes_dispatch[output_type](ID=parameter_string,data_format='LOCUST',filename=dir_output_filepath))

    return outputs

#plot difference in distribution function
outputs=get_output_files('dfn')
for counter in range(len(outputs)):
    outputs[counter]=outputs[counter].transform(axes=axes)
DFN_diff=copy.deepcopy(outputs[0])
DFN_diff.ID=f'log_10 {outputs[0]} - {outputs[1]} / {outputs[0]}'
DFN_diff['dfn']=np.nan_to_num(np.log10(np.abs((outputs[0]['dfn']-outputs[1]['dfn'])/outputs[0]['dfn'])),nan=-5.)
DFN_diff['dfn'][DFN_diff['dfn']>1.e3]=-5.
fig,ax=plt.subplots(1)
DFN_diff_mesh=DFN_diff.plot(fig=fig,ax=ax,axes=axes,transform=False,real_scale=True,vminmax=[-5,3])
cbar=fig.colorbar(DFN_diff_mesh,orientation='vertical')
ax.set_xlabel('R [m]',fontsize=25)  
ax.set_ylabel('Z [m]',fontsize=25)  
ax.set_title('$log_{10}(f_{outputs[0]}-f_{outputs[1]})\slash f_{outputs[0]}$',fontsize=25)
#ax.set_xlim([np.min(equi['R_1D']),np.max(equi['R_1D'])])
#ax.set_ylim([1.1*np.min(equi['lcfs_z']),1.1*np.max(equi['lcfs_z'])])
ax.set_facecolor(settings.cmap_default(0.0))
plt.show()  


#################################
 
##################################################################
 
###################################################################################################