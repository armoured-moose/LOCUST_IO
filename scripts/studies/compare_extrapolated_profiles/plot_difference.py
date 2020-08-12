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
    import os
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

try:
    cwd=pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
    sys.path.append(str(cwd.parents[1]))
    import templates.plot_mod
except:
    raise ImportError("ERROR: templates/template_mod.py could not be imported!\nreturning\n") 
    sys.exit(1)

################################################################## 
#Main 

import compare_extrapolated_profiles_launch as batch_data

axes=['R','Z']
xmin=0
xmax=0
ymin=0
ymax=0

#plot difference in distribution function
outputs=templates.plot_mod.get_output_files(batch_data,'dfn')
for counter in range(len(batch_data.args_batch['LOCUST_run__dir_output'])):
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