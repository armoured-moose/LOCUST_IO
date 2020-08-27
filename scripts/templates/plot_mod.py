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

def get_divergence_files(batch_data):
    """
    notes:
        assume divergence is dumped on a rectangular grid
        XXX broken
    """

    for run_number,(parameter_string,dir_output) in enumerate(zip(batch_data.parameter_strings,batch_data.args_batch['LOCUST_run__dir_output'])): #within each GPU folder the path to each output is the same
        #get the equilibrium to get an idea of domain to check over
        equilibrium=Equilibrium(ID='',data_format='GEQDSK',filename=batch_data.args_batch['RMP_study__filepath_equilibrium'][run_number],GEQDSKFIX1=True,GEQDSKFIX2=True)
        dir_output=pathlib.Path(str(dir_output).strip("\'"))
        dir_output_filepaths_RZ=list(dir_output.glob('field_data_divergence_check_RZ.out')) #get all filenames for runs corresponding to this choice of parameters    
        dir_output_filepaths_XY=list(dir_output.glob('field_data_divergence_check_XY.out')) #get all filenames for runs corresponding to this choice of parameters    
        if dir_output_filepaths_RZ and dir_output_filepaths_XY:
            try:

                field_data_RZ=Perturbation(ID=parameter_string,data_format='LOCUST_field_data',filename=dir_output_filepaths_RZ[0])
                field_data_XY=Perturbation(ID=parameter_string,data_format='LOCUST_field_data',filename=dir_output_filepaths_XY[0])
                
                field_data_RZ_nZ=np.where(field_data_RZ['R']==field_data_RZ['R'][0])[0][1]
                field_data_RZ_nR=len(field_data_RZ['R'])/field_data_RZ_nZ
                for quant in field_data_RZ.data:
                    field_data_RZ[quant]=field_data_RZ[quant].reshape(int(field_data_RZ_nR),int(field_data_RZ_nZ)).T
                field_data_RZ['R_1D']=field_data_RZ['R'][:,0]
                field_data_RZ['Z_1D']=field_data_RZ['Z'][0,:]

                field_data_XY_nR=np.where(field_data_XY['phi']==field_data_XY['phi'][0])[0][1]
                field_data_XY_nphi=len(field_data_XY['R'])/field_data_XY_nR
                for quant in field_data_XY.data:
                    field_data_XY[quant]=field_data_XY[quant].reshape(int(field_data_XY_nR),int(field_data_XY_nphi))
                field_data_XY['phi']=field_data_XY['phi'][0,:]
                field_data_XY['R_1D']=field_data_XY['R'][:,0]

                yield field_data_RZ,field_data_XY
                
            except:
                yield None
        else:
            yield None

#################################
 
##################################################################

###################################################################################################