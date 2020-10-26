#plot_difference.py
 
"""
Samuel Ward
24/02/20
----
script for plotting difference between outputs with/without impurities
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
    from classes.input_classes.equilibrium import Equilibrium
except:
    raise ImportError("ERROR: LOCUST_IO/src/classes/input_classes/equilibrium.py could not be imported!\nreturning\n") 
    sys.exit(1)
try:
    from classes.input_classes.perturbation import Perturbation
except:
    raise ImportError("ERROR: LOCUST_IO/src/classes/input_classes/perturbation.py could not be imported!\nreturning\n")
    sys.exit(1)
try:
    from classes.output_classes.distribution_function import Distribution_Function
except:
    raise ImportError("ERROR: LOCUST_IO/src/classes/output_classes/distribution_function.py could not be imported!\nreturning\n")
    sys.exit(1)
try:
    from classes.output_classes.particle_list import Final_Particle_List
except:
    raise ImportError("ERROR: LOCUST_IO/src/classes/output_classes/distribution_function.py could not be imported!\nreturning\n")
    sys.exit(1)
try:
    from classes.output_classes.rundata import Rundata
except:
    raise ImportError("ERROR: LOCUST_IO/src/classes/output_classes/distribution_function.py could not be imported!\nreturning\n")
    sys.exit(1)
try:
    from classes.output_classes.poincare import Poincare
except:
    raise ImportError("ERROR: LOCUST_IO/src/classes/output_classes/poincare.py could not be imported!\nreturning\n")
    sys.exit(1)
try:
    from classes.output_classes.orbits import Orbits
except:
    raise ImportError("ERROR: LOCUST_IO/src/classes/output_classes/orbits.py could not be imported!\nreturning\n")
    sys.exit(1)
try:
    from classes.output_classes.output_mesh import Output_Mesh
except:
    raise ImportError("ERROR: LOCUST_IO/src/classes/output_classes/output_mesh.py could not be imported!\nreturning\n")
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

import compare_impurities_on_off_launch as batch_data

def get_output_files(batch_data,output_type='dfn',**kwargs): 

    outputs=[]
    output_file_dispatch={}
    output_file_dispatch['dfn']='*.dfn'
    output_file_dispatch['fpl']='ptcl_cache.dat'
    output_file_dispatch['rund']='rundata*_1'
    output_file_dispatch['poinc']='Poincare_map*.dat'
    output_file_dispatch['orbit2D']='ORBIT_2D'
    output_file_dispatch['orbit3D']='ORBIT_3D'
    output_file_dispatch['pfc']='pfc_hitmap*'

    output_classes_dispatch={}
    output_classes_dispatch['dfn']=Distribution_Function
    output_classes_dispatch['fpl']=Final_Particle_List
    output_classes_dispatch['rund']=Rundata
    output_classes_dispatch['poinc']=Poincare
    output_classes_dispatch['orbit2D']=Orbits
    output_classes_dispatch['orbit3D']=Orbits
    output_classes_dispatch['pfc']=Output_Mesh

    output_dir=pathlib.Path(batch_data.args_batch['LOCUST_run__dir_output'][0].strip("\'")).parents[0]
    output_dirs=list(output_dir.glob('*'))
    print(output_dir)
    print(output_dirs)

    for dir_output in output_dirs:

        parameter_string=dir_output.parts[-1]
        print(parameter_string)
        dir_output=pathlib.Path(dir_output)
        dir_output_filepaths=list(dir_output.glob(output_file_dispatch[output_type])) #get all filenames for runs corresponding to this choice of parameters    
        print(dir_output_filepaths)
        if dir_output_filepaths:
            for dir_output_filepath in dir_output_filepaths:
                try:
                    outputs.append(output_classes_dispatch[output_type](ID=parameter_string,data_format='LOCUST',filename=dir_output_filepath,**kwargs))
                except:
                    outputs.append(None)
        else:
            outputs.append(None)

    return outputs


axes=['E','V_pitch']
xmin=0
xmax=0
ymin=0
ymax=0
  
outputs=get_output_files(batch_data,'fpl')
fig1,ax1=plt.subplots(1)
fig2,ax2=plt.subplots(1)
for output,colour in zip(outputs,[settings.cmap_g,settings.cmap_r]):
    if output:
        output['weight']/=len(output['weight'])
        output['E']/=1000.
        output.plot(fig=fig1,ax=ax1,axes=['time'],fill=False,label=output.ID,colmap=colour,number_bins=100,weight=True)
        output.plot(fig=fig2,ax=ax2,axes=['E'],fill=False,label=output.ID,colmap=colour,number_bins=100,weight=True)
ax1.set_xlabel('Time [s]',fontsize=25)  
ax2.set_xlabel('Energy [keV]',fontsize=25)  
ax1.set_ylabel('loss fraction',fontsize=25)  
ax2.set_ylabel('loss fraction',fontsize=25)  
ax1.legend()
ax2.legend()
plt.show()
'''
'''

#plot difference in distribution function
outputs=get_output_files(batch_data,'dfn')

fig,ax=plt.subplots(1)
for output,colour in zip(outputs,[settings.cmap_g,settings.cmap_r]):
    if output: output.plot(fig=fig,ax=ax,axes=['R'],label=output.ID,colmap=colour,number_bins=100)
ax.legend()
plt.show()

#plot one of the distribution functions
outputs[0].plot(axes=axes)

for counter,output in enumerate(outputs):
    outputs[counter]=output.transform(axes=axes)
DFN_diff=copy.deepcopy(outputs[0])
DFN_diff.ID=f'log_10 {outputs[0]} - {outputs[1]} / {outputs[0]}'
DFN_diff['dfn']=np.nan_to_num(np.log10(np.abs((outputs[0]['dfn']-outputs[1]['dfn'])/outputs[0]['dfn'])),nan=-5.)
DFN_diff['dfn'][DFN_diff['dfn']>1.e3]=-5.
fig,ax=plt.subplots(1)
DFN_diff_mesh=DFN_diff.plot(fig=fig,ax=ax,axes=axes,transform=False,real_scale=False,vminmax=[-5,3],number_bins=9)
cbar=fig.colorbar(DFN_diff_mesh,orientation='vertical')
ax.set_xlabel('R [m]',fontsize=25)  
ax.set_ylabel('Z [m]',fontsize=25)  
#ax.set_title(f'$log_{10}(f_{outputs[0].ID}-f_{outputs[1].ID})\slash f_{outputs[0].ID}$',fontsize=25)
#ax.set_xlim([np.min(equi['R_1D']),np.max(equi['R_1D'])])
#ax.set_ylim([1.1*np.min(equi['lcfs_z']),1.1*np.max(equi['lcfs_z'])])
ax.set_facecolor(settings.cmap_default(0.0))
plt.show()  

#plot the inputs by running just the plot input stages of the batch script 
'''
batch_data.args_batch['RMP_study__workflow_commands']=['plot_inputs']*len(batch_data.args_batch['RMP_study__workflow_commands'])
RMP_batch_run=Batch(**batch_data.args_batch)
RMP_batch_run.launch(
    workflow_filepath='template_run.py', 
    environment_name_batch='TITAN',
    environment_name_workflow='TITAN',
    interactive=True)   
'''

#################################
 
##################################################################
 
###################################################################################################