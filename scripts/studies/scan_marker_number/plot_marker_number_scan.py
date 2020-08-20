#plot_marker_number_scan.py
 
"""
Samuel Ward
17/08/20
----
look at effects of changing number of markers
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

import scan_marker_number_launch as batch_data

outputs=templates.plot_mod.get_output_files(batch_data,'fpl')

fig1,ax1=plt.subplots(1)
fig2,ax2=plt.subplots(1)
for counter,(output,col_val) in enumerate(zip(outputs,np.linspace(0,1,len(batch_data.args_batch['LOCUST_run__dir_output'])))):
    if output: 
        number_markers=batch_data.parameters__number_blocks[counter]*batch_data.parameters__number_threads[counter]*8
        output['weight']/=len(output['weight']) #normalise weights according to number markers
        output.plot(fig=fig1,ax=ax1,axes=['time'],fill=False,label=number_markers,colmap=settings.cmap_default,colmap_val=col_val,number_bins=200,weight=True)
        output['E']/=1000. #convert to keV
        #output.plot(fig=fig2,ax=ax2,axes=['E'],fill=False,label=output.ID,colmap=settings.cmap_default,colmap_val=col_val,number_bins=200,weight=True)
ax1.legend()
#ax2.legend()
ax1.set_xlabel('time [s]')
#ax2.set_xlabel('energy [keV]')
ax1.set_ylabel('losses')
#ax2.set_ylabel('losses')
ax1.set_title('')
#ax2.set_title('')
plt.show()

#################################
 
##################################################################
 
###################################################################################################