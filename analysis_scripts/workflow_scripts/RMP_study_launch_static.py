#RMP_study_launch.py
 
"""
Samuel Ward
14/10/19
----
script for controlling and launching LOCUST parameter scans for static RMP studies
---
 
notes:         
    launches the workflow defined in RMP_study_run.py
    since only flat arrays are passed to Batch class, __ labels are designed to help distiniguish what variables are needed for 

    directory structure goes as:
        LOCUST_IO
            data
                input_files
                    path_to_master_data - unchanging
                    database_folder_name
                        RMP_study
                            metadata_folder_name - stores all the inputs just before a run is performed, deleted after a run
                output_files
                    database_folder_name
                        RMP_study
                            parameter_folder_name - stores all the outputs permanently
                cache_files
                    database_folder_name
                        RMP_study
        /tmp/<uname>/ (LOCUST root dir)
            InputFiles
            OutputFiles
            CacheFiles
---
"""

###################################################################################################
#Preamble
 
import sys #have global imports --> makes less modular (no "from input_classes import x") but best practice to import whole input_classes module anyway

try:
    import numpy as np
    import pathlib
    import copy
except:
    raise ImportError("ERROR: initial modules could not be imported!\nreturning\n")
    sys.exit(1)

try:
    import context
except:
    raise ImportError("ERROR: context.py could not be imported!\nreturning\n")
    sys.exit(1)

try:
    from run_scripts.batch import Batch
except:
    raise ImportError("ERROR: LOCUST_IO/src/run_scripts/batch.py could not be imported!\nreturning\n")
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
    from settings import *
except:
    raise ImportError("ERROR: LOCUST_IO/src/settings.py could not be imported!\nreturning\n") 
    sys.exit(1)

################################################################## 
#Main 

#random variables to help
DataMarsf_folder_name='DataMarsf' #normal 3D field level name however this can sometimes vary between scenarios...

#some variables to act as notes, storing possible options to choose from
database__options=['ITER_15MAQ10_case5','ITER_15MAQ5_case4','ITER_5MAH_case1','ITER_7d5MAFullB_case3','ITER_7d5MAHalfB_case2']
parameters__toroidal_mode_numbers__options=[1,2,3,4,5,6]
kinetic_profs_n__options=['flat','peaked']
kinetic_profs_tF_tE__options=[0.5,0.57,0.65,0.72,0.73,1.,2.] #0.7 is actually 0.72
kinetic_profs_tF_tE_string__options=['05','057','065','072','073','1','2'] #version used in strings describing data in storage
kinetic_profs_Pr__options=[0.3,1.] #prandl number
kinetic_profs_Pr_string__options=['03','1'] #version used in strings describing data in storage

#################################
#define parameters fixed within a scenario here

parameters__databases=['ITER_15MAQ10_case5'] #these all zipped at same level in main loop because source data is not consistent enough
parameters__sheet_names_kinetic_prof=["'Flat n'"]
parameters__sheet_names_rotation=["'Flat n, Pr=1'"]
parameters__kinetic_profs_n=['flat']

#fixed parameters needed by LOCUST_run
LOCUST_run__system_name='TITAN'
LOCUST_run__repo_URL=None
LOCUST_run__commit_hash=None
#these may vary in future - in which case add a new nesting to the parameter loop below
LOCUST_run__settings_prec_mod={}
#LOCUST_run__settings_prec_mod['']=
LOCUST_run__flags={}
#LOCUST_run__flags['TOKAMAK']=1
#LOCUST_run__flags['']=
#LOCUST_run__flags['']=
#LOCUST_run__flags['']=

#fixed parameters needed by MARS_read
MARS_read__settings={}
MARS_read__settings['TAIL']="['','','']"
MARS_read__flags={}
MARS_read__flags['TOKAMAK']=1

#define parameters needed by the RMP_study workflow for a given scenario
RMP_study__name='test_study'
RMP_study__dir_input_database=support.dir_input_files / 'ITER_fields_yueqiang' / 'DataBase'
RMP_study__filepaths_kinetic_profiles=[list((RMP_study__dir_input_database / parameters__database / 'DataEq').glob('*.xlsx'))[0] for parameters__database in parameters__databases] #define the paths to kinetic profiles

#################################
#define the parameter space which varies for a given scenario

#kinetic profile parameters
parameters__kinetic_profs_tF_tE=[0.5] #0.7 is actually 0.72
parameters__kinetic_profs_tF_tE_string=['05'] #version used in strings describing data in storage

parameters__kinetic_profs_Pr=[0.3] #prandl number
parameters__kinetic_profs_Pr_string=['03'] #version used in strings describing data in storage

#3D field parameters
parameters__toroidal_mode_numbers=[1]
parameters__phases_upper=[0]
parameters__phases_middle=[0]
parameters__phases_lower=[0]
parameters__rotations_upper=[0]
parameters__rotations_middle=[0]
parameters__rotations_lower=[0]

##################################################################
#initialise __batch args needed for Batch class

parameters__databases__batch=[]
parameters__sheet_names_kinetic_prof__batch=[]
parameters__sheet_names_rotation__batch=[]
parameters__kinetic_profs_n__batch=[]
parameters__kinetic_profs_tF_tE__batch=[]
parameters__kinetic_profs_Pr__batch=[]
parameters__toroidal_mode_numbers__batch=[]
parameters__phases_upper__batch=[]
parameters__phases_middle__batch=[]
parameters__phases_lower__batch=[]
parameters__rotations_upper__batch=[]
parameters__rotations_middle__batch=[]
parameters__rotations_lower__batch=[]
parameters__parameter_string__batch=[]
LOCUST_run__dir_LOCUST__batch=[]
LOCUST_run__dir_input__batch=[]
LOCUST_run__dir_output__batch=[]
LOCUST_run__dir_cache__batch=[]
LOCUST_run__system_name__batch=[]
LOCUST_run__repo_URL__batch=[]
LOCUST_run__commit_hash__batch=[]
LOCUST_run__settings_prec_mod__batch=[]
LOCUST_run__flags__batch=[]
MARS_read__settings__batch=[]
MARS_read__flags__batch=[]
RMP_study__name__batch=[]
RMP_study__dir_input_database__batch=[]
RMP_study__filepaths_kinetic_profiles__batch=[]
RMP_study__filepaths_3D_field_U__batch=[]
RMP_study__filepaths_3D_field_M__batch=[]
RMP_study__filepaths_3D_field_L__batch=[]

##################################################################
#create every valid combination of parameter, returned in flat lists
#use zip and nest levels to define specific combinations which cannot be varied
#e.g. zip together parameters__kinetic_profs_tF_tE and parameters__kinetic_profs_tF_tE_string since these should iterate together

#generate string holding this parameter combination - used for labelling directories/filenames
parameters__parameter_strings__batch=[]
run_number=0

#first level are the data which remain constant for a parameter scan
for parameters__database, \
    parameters__sheet_name_kinetic_prof, \
    parameters__sheet_name_rotation, \
    parameters__kinetic_prof_n, \
    RMP_study__filepath_kinetic_profiles \
    in zip(
        parameters__databases,
        parameters__sheet_names_kinetic_prof,
        parameters__sheet_names_rotation,
        parameters__kinetic_profs_n, \
        RMP_study__filepaths_kinetic_profiles
        ): 
    for parameters__kinetic_prof_tF_tE, \
        parameters__kinetic_prof_tF_tE_string \
        in zip(
            parameters__kinetic_profs_tF_tE,
            parameters__kinetic_profs_tF_tE_string
            ):

        for parameters__kinetic_prof_Pr, \
            parameters__kinetic_prof_Pr_string \
            in zip(
                parameters__kinetic_profs_Pr,
                parameters__kinetic_profs_Pr_string
                ):
            for parameters__toroidal_mode_number in parameters__toroidal_mode_numbers:
                print(parameters__toroidal_mode_number)
                for parameters__phase_upper in parameters__phases_upper:
                    for parameters__phase_middle in parameters__phases_middle:
                        for parameters__phase_lower in parameters__phases_lower:
                            for parameters__rotation_upper in parameters__rotations_upper:
                                for parameters__rotation_middle in parameters__rotations_middle:
                                    for parameters__rotation_lower in parameters__rotations_lower:
                                    
                                        run_number+=1 #increment run counter                                         
                                        parameters__parameter_string=''
                                        for parameter,value in zip([
                                                        'n',
                                                        'tFtE',
                                                        'Pr',
                                                        'ntor',
                                                        'phaseu',
                                                        'phasem',
                                                        'phasel',
                                                        'rotu',
                                                        'rotm',
                                                        'rotl'
                                                        ],[
                                                        parameters__kinetic_prof_n,
                                                        parameters__kinetic_prof_tF_tE,
                                                        parameters__kinetic_prof_Pr,
                                                        parameters__toroidal_mode_number,
                                                        parameters__phase_upper,
                                                        parameters__phase_middle,
                                                        parameters__phase_lower,
                                                        parameters__rotation_upper,
                                                        parameters__rotation_middle,
                                                        parameters__rotation_lower]):
                                            parameters__parameter_string='_'.join([parameters__parameter_string,parameter,str(value)])
                                            parameters__parameter_string=parameters__parameter_string[1:]

                                        #################################
                                        #define corresponding workflow args passed to batch (denoted wth __batch)

                                        parameters__databases__batch.append(parameters__database)
                                        parameters__sheet_names_kinetic_prof__batch.append(parameters__sheet_name_kinetic_prof)
                                        parameters__sheet_names_rotation__batch.append(parameters__sheet_name_rotation)
                                        parameters__kinetic_profs_n__batch.append(parameters__kinetic_prof_n)
                                        parameters__kinetic_profs_tF_tE__batch.append(parameters__kinetic_prof_tF_tE)
                                        parameters__kinetic_profs_Pr__batch.append(parameters__kinetic_prof_Pr)
                                        parameters__toroidal_mode_numbers__batch.append(parameters__toroidal_mode_number)
                                        parameters__phases_upper__batch.append(parameters__phase_upper)
                                        parameters__phases_middle__batch.append(parameters__phase_middle)
                                        parameters__phases_lower__batch.append(parameters__phase_lower)
                                        parameters__rotations_upper__batch.append(parameters__rotation_upper)
                                        parameters__rotations_middle__batch.append(parameters__rotation_middle)
                                        parameters__rotations_lower__batch.append(parameters__rotation_lower)
                                        parameters__parameter_strings__batch.append(parameters__parameter_string)
                                        LOCUST_run__dir_LOCUST__batch.append(support.dir_locust / parameters__database / RMP_study__name / parameters__parameter_string)
                                        LOCUST_run__dir_input__batch.append(support.dir_input_files / parameters__database / RMP_study__name / parameters__parameter_string)
                                        LOCUST_run__dir_output__batch.append(support.dir_output_files / parameters__database / RMP_study__name / parameters__parameter_string)
                                        LOCUST_run__dir_cache__batch.append(support.dir_cache_files / parameters__database / RMP_study__name) #one level less to pool cache files into same directory across simulations
                                        LOCUST_run__system_name__batch.append(LOCUST_run__system_name)
                                        LOCUST_run__repo_URL__batch.append(LOCUST_run__repo_URL)
                                        LOCUST_run__commit_hash__batch.append(LOCUST_run__commit_hash)
                                        LOCUST_run__settings_prec_mod__batch.append(LOCUST_run__settings_prec_mod)
                                        LOCUST_run__flags__batch.append(LOCUST_run__flags)
                                        MARS_read__settings__batch.append(MARS_read__settings)
                                        MARS_read__flags__batch.append(MARS_read__flags)
                                        RMP_study__name__batch.append(RMP_study__name)
                                        RMP_study__dir_input_database__batch.append(RMP_study__dir_input_database)
                                        RMP_study__filepaths_kinetic_profiles__batch.append(RMP_study__filepath_kinetic_profiles)
                                        
                                        #find path to 3D field corresponding to desired parameters here
                                        RMP_study__filepaths_3D_field_head=RMP_study__dir_input_database / parameters__database / DataMarsf_folder_name 
                                        RMP_study__filepaths_3D_field_tail_U='BPLASMA_MARSF_n{parameters__toroidal_mode_number}_cU_Pr{parameters__kinetic_prof_Pr_string}_tfte{parameters__kinetic_prof_tF_tE_string}.IN'.format(
                                                                                                    parameters__toroidal_mode_number=str(parameters__toroidal_mode_number),
                                                                                                    parameters__kinetic_prof_Pr_string=str(parameters__kinetic_prof_Pr_string),
                                                                                                    parameters__kinetic_prof_tF_tE_string=str(parameters__kinetic_prof_tF_tE_string))
                                        RMP_study__filepaths_3D_field_tail_M='BPLASMA_MARSF_n{parameters__toroidal_mode_number}_cM_Pr{parameters__kinetic_prof_Pr_string}_tfte{parameters__kinetic_prof_tF_tE_string}.IN'.format(
                                                                                                    parameters__toroidal_mode_number=str(parameters__toroidal_mode_number),
                                                                                                    parameters__kinetic_prof_Pr_string=str(parameters__kinetic_prof_Pr_string),
                                                                                                    parameters__kinetic_prof_tF_tE_string=str(parameters__kinetic_prof_tF_tE_string))
                                        RMP_study__filepaths_3D_field_tail_L='BPLASMA_MARSF_n{parameters__toroidal_mode_number}_cL_Pr{parameters__kinetic_prof_Pr_string}_tfte{parameters__kinetic_prof_tF_tE_string}.IN'.format(
                                                                                                    parameters__toroidal_mode_number=str(parameters__toroidal_mode_number),
                                                                                                    parameters__kinetic_prof_Pr_string=str(parameters__kinetic_prof_Pr_string),
                                                                                                    parameters__kinetic_prof_tF_tE_string=str(parameters__kinetic_prof_tF_tE_string))
                                        RMP_study__filepaths_3D_field_U__batch.append(RMP_study__filepaths_3D_field_head/RMP_study__filepaths_3D_field_tail_U) 
                                        RMP_study__filepaths_3D_field_M__batch.append(RMP_study__filepaths_3D_field_head/RMP_study__filepaths_3D_field_tail_M) 
                                        RMP_study__filepaths_3D_field_L__batch.append(RMP_study__filepaths_3D_field_head/RMP_study__filepaths_3D_field_tail_L)

##################################################################
#define and launch the batch scripts
'''
print(parameters__databases__batch)
print(parameters__sheet_names_kinetic_prof__batch)
print(parameters__sheet_names_rotation__batch)
print(parameters__kinetic_profs_n__batch)
print(parameters__kinetic_profs_tF_tE__batch)
print(parameters__kinetic_profs_Pr__batch)
print(parameters__toroidal_mode_numbers__batch)
print(parameters__phases_upper__batch)
print(parameters__phases_middle__batch)
print(parameters__phases_lower__batch)
print(parameters__rotations_upper__batch)
print(parameters__rotations_middle__batch)
print(parameters__rotations_lower__batch)
print(parameters__parameter_strings__batch)
print(LOCUST_run__dir_LOCUST__batch)
print(LOCUST_run__dir_input__batch)
print(LOCUST_run__dir_output__batch)
print(LOCUST_run__dir_cache__batch)
print(LOCUST_run__system_name__batch)
print(LOCUST_run__repo_URL__batch)
print(LOCUST_run__commit_hash__batch)
print(LOCUST_run__settings_prec_mod__batch)
print(LOCUST_run__flags__batch)
print(RMP_study__name__batch)
print(RMP_study__dir_input_database__batch)
print(RMP_study__filepaths_kinetic_profiles__batch)
print(RMP_study__filepaths_3D_field_U__batch)
print(RMP_study__filepaths_3D_field_M__batch)
print(RMP_study__filepaths_3D_field_L__batch)
print(run_number)
'''

RMP_batch_run=Batch(
    parameters__database=parameters__databases__batch,
    parameters__sheet_name_kinetic_prof=parameters__sheet_names_kinetic_prof__batch,
    parameters__sheet_name_rotation=parameters__sheet_names_rotation__batch,
    parameters__kinetic_prof_n=parameters__kinetic_profs_n__batch,
    parameters__kinetic_prof_tF_tE=parameters__kinetic_profs_tF_tE__batch,
    parameters__kinetic_prof_Pr=parameters__kinetic_profs_Pr__batch,
    parameters__toroidal_mode_number=parameters__toroidal_mode_numbers__batch,
    parameters__phase_upper=parameters__phases_upper__batch,
    parameters__phase_middle=parameters__phases_middle__batch,
    parameters__phase_lower=parameters__phases_lower__batch,
    parameters__rotation_upper=parameters__rotations_upper__batch,
    parameters__rotation_middle=parameters__rotations_middle__batch,
    parameters__rotation_lower=parameters__rotations_lower__batch,
    parameters__parameter_string=parameters__parameter_strings__batch,
    LOCUST_run__dir_LOCUST=LOCUST_run__dir_LOCUST__batch,
    LOCUST_run__dir_input=LOCUST_run__dir_input__batch,
    LOCUST_run__dir_output=LOCUST_run__dir_output__batch,
    LOCUST_run__dir_cache=LOCUST_run__dir_cache__batch,
    LOCUST_run__system_name=LOCUST_run__system_name__batch,
    LOCUST_run__repo_URL=LOCUST_run__repo_URL__batch,
    LOCUST_run__commit_hash=LOCUST_run__commit_hash__batch,
    LOCUST_run__settings_prec_mod=LOCUST_run__settings_prec_mod__batch,
    LOCUST_run__flags=LOCUST_run__flags__batch,
    MARS_read__settings=MARS_read__settings__batch,
    MARS_read__flags=MARS_read__flags__batch,
    RMP_study__name=RMP_study__name__batch,
    RMP_study__dir_input_database=RMP_study__dir_input_database__batch,
    RMP_study__filepath_kinetic_profiles=RMP_study__filepaths_kinetic_profiles__batch,
    RMP_study__filepaths_3D_field_U=RMP_study__filepaths_3D_field_U__batch,
    RMP_study__filepaths_3D_field_M=RMP_study__filepaths_3D_field_M__batch,
    RMP_study__filepaths_3D_field_L=RMP_study__filepaths_3D_field_L__batch
    )
RMP_batch_run.launch(workflow_filepath='RMP_study_run.py',system_name='TITAN')   

#################################
 
##################################################################
 
###################################################################################################