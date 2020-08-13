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

import scan_current_n3_n6_launch as batch_data

outputs=templates.plot_mod.get_output_files(batch_data,'fpl')

fig1,ax1=plt.subplots(1)
fig2,ax2=plt.subplots(1)
for output,col_val in zip(outputs,np.linspace(0,1,len(batch_data.args_batch['LOCUST_run__dir_output']))):
    if output: 
        output.plot(fig=fig1,ax=ax1,axes=['time'],fill=False,label=output.ID,colmap=settings.cmap_default,colmap_val=col_val,number_bins=200,weight=True)
        output['E']/=1000. #convert to keV
        output.plot(fig=fig2,ax=ax2,axes=['E'],fill=False,label=output.ID,colmap=settings.cmap_default,colmap_val=col_val,number_bins=200,weight=True)
ax1.legend()
ax2.legend()
ax1.set_xlabel('time [s]')
ax2.set_xlabel('energy [keV]')
ax1.set_ylabel('losses')
ax2.set_ylabel('losses')
ax1.set_title('')
ax1.set_title('')
ax2.set_title('')
plt.show()

outputs=templates.plot_mod.get_output_files(batch_data,'dfn')

fig,ax=plt.subplots(1)
for output,col_val in zip(outputs,np.linspace(0,1,len(batch_data.args_batch['LOCUST_run__dir_output']))):
    if output: output.plot(fig=fig,ax=ax,axes=['R'],label=output.ID,colmap=settings.cmap_default,colmap_val=col_val,number_bins=200)
ax.legend()
plt.show()

outputs=templates.plot_mod.get_output_files(batch_data,'rund')

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