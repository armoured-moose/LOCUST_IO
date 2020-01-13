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
                    path_to_additional_data - unchanging
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
    import settings
except:
    raise ImportError("ERROR: LOCUST_IO/src/settings.py could not be imported!\nreturning\n") 
    sys.exit(1)

################################################################## 
#Main 

#random variables to help
folder_name_DataMarsf='DataMarsf' #3D field directory name however this can sometimes vary between scenarios e.g. if using vacuum field
folder_name_DataEq='DataEq' #equilibrium 

#some variables to act as reminders/notes, storing possible options to choose from
database__options=['ITER_15MAQ10_case5','ITER_15MAQ5_case4','ITER_5MAH_case1','ITER_7d5MAFullB_case3','ITER_7d5MAHalfB_case2']
parameters__toroidal_mode_numbers__options=[1,2,3,4,5,6]
kinetic_profs_n__options=['flat','peaked']
kinetic_profs_tF_tE__options=[0.5,0.57,0.65,0.72,0.73,1.,2.] #0.7 is actually 0.72
kinetic_profs_tF_tE_string__options=['05','057','065','072','073','1','2'] #version used in strings describing data in storage
kinetic_profs_Pr__options=[0.3,1.] #prandl number
kinetic_profs_Pr_string__options=['03','1'] #version used in strings describing data in storage

#dispatch table matching parameter values to corresponding IDS shot/run numbers
#XXX NEED TO COMPLETE THIS DISPATCH TABLE
target_IDS_dispatch_shot={}
target_IDS_dispatch_run={}

#XXX might need to add an extra layer here based on parameters__database if this is another deciding factor
#XXX need to check prandl numbers etc. here 
target_IDS_dispatch_shot['ITER_15MAQ5_case4']=131024
target_IDS_dispatch_run['ITER_15MAQ5_case4']={} #run depends on three parameters - dispatch table needs to be three levels deep - first level is scenario, second is Prandl number and third  is tF/tE
target_IDS_dispatch_run['ITER_15MAQ5_case4']['1']={} 
target_IDS_dispatch_run['ITER_15MAQ5_case4']['1']['2']=0
target_IDS_dispatch_run['ITER_15MAQ5_case4']['1']['1']=1 
target_IDS_dispatch_run['ITER_15MAQ5_case4']['1']['05']=2
target_IDS_dispatch_run['ITER_15MAQ5_case4']['03']={} 
target_IDS_dispatch_run['ITER_15MAQ5_case4']['03']['2']=3
target_IDS_dispatch_run['ITER_15MAQ5_case4']['03']['1']=4
target_IDS_dispatch_run['ITER_15MAQ5_case4']['03']['073']=5

target_IDS_dispatch_shot['ITER_15MAQ10_case5']=131025
target_IDS_dispatch_run['ITER_15MAQ10_case5']={}
target_IDS_dispatch_run['ITER_15MAQ10_case5']['1']={} 
target_IDS_dispatch_run['ITER_15MAQ10_case5']['1']['2']=0
target_IDS_dispatch_run['ITER_15MAQ10_case5']['1']['1']=1 
target_IDS_dispatch_run['ITER_15MAQ10_case5']['1']['05']=2
target_IDS_dispatch_run['ITER_15MAQ10_case5']['03']={} 
target_IDS_dispatch_run['ITER_15MAQ10_case5']['03']['2']=3
target_IDS_dispatch_run['ITER_15MAQ10_case5']['03']['1']=4
target_IDS_dispatch_run['ITER_15MAQ10_case5']['03']['073']=5

target_IDS_dispatch_shot['ITER_5MAH_case1']=101007
target_IDS_dispatch_run['ITER_5MAH_case1']={}
target_IDS_dispatch_run['ITER_5MAH_case1']['1']={} 
target_IDS_dispatch_run['ITER_5MAH_case1']['1']['2']=0
target_IDS_dispatch_run['ITER_5MAH_case1']['1']['1']=1 
target_IDS_dispatch_run['ITER_5MAH_case1']['1']['05']=2 

target_IDS_dispatch_shot['ITER_7d5MAHalfB_case2']=131020 #or 131021
target_IDS_dispatch_run['ITER_7d5MAHalfB_case2']={}
target_IDS_dispatch_run['ITER_7d5MAHalfB_case2']['1']={} 
target_IDS_dispatch_run['ITER_7d5MAHalfB_case2']['1']['2']=0 #XXX this could go up to 2

#################################
#define parameters fixed within a scenario here

parameters__databases=['ITER_15MAQ5_case4'] #these all zipped at same level in main loop because source data is not consistent enough
parameters__sheet_names_kinetic_prof=["'Out_iterDD.iterDDL-R'"]
parameters__sheet_names_rotation=["'Pr=0.3'"]
parameters__var_names_rotation=["'Vt(tF/tE=2)'"]
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

#fixed parameters needed for NEMO_run
NEMO_run__dir_NEMO=support.dir_nemo
NEMO_run__nmarker=int(1.e6)
NEMO_run__fokker_flag=0

#fixed parameters needed by MARS_read
MARS_read__tail_U='_U_VAC'
MARS_read__tail_M='_M_VAC'
MARS_read__tail_L='_L_VAC'
MARS_read__tails=[MARS_read__tail_U,MARS_read__tail_M,MARS_read__tail_L]
MARS_read__settings={}
MARS_read__settings['TAIL']="{}".format(MARS_read__tails)
MARS_read__flags={}
MARS_read__flags['TOKAMAK']=1

#define parameters needed by the RMP_study workflow for a given scenario
RMP_study__name='test_study'
RMP_study__dir_input_database=support.dir_input_files / 'ITER_fields_yueqiang' / 'DataBase'
RMP_study__filepaths_kinetic_profiles=[list((RMP_study__dir_input_database / parameters__database / folder_name_DataEq).glob('*.xlsx'))[0] for parameters__database in parameters__databases] #define the paths to kinetic profiles
RMP_study__filepaths_equilibrium=[list((RMP_study__dir_input_database / parameters__database / folder_name_DataEq).glob('eqdsk*'))[0] for parameters__database in parameters__databases] #define the paths to equilibria
RMP_study__filepaths_additional_data=support.dir_input_files / 'ITER_additional_data'

#################################
#define the parameter space which varies for a given scenario

#kinetic profile parameters
parameters__kinetic_profs_tF_tE=[2.0] 
parameters__kinetic_profs_tF_tE_string=['2'] #version used in strings describing data in storage

parameters__kinetic_profs_Pr=[1.0] #prandl number
parameters__kinetic_profs_Pr_string=['1'] #version used in strings describing data in storage

#3D field parameters
parameters__toroidal_mode_numbers=[1]
parameters__phases_upper=[0]
parameters__phases_middle=[0]
parameters__phases_lower=[0]
parameters__rotations_upper=[0]
parameters__rotations_middle=[0]
parameters__rotations_lower=[0]

#################################
#misc workflow settings
IDS__shot=1
IDS__run=1
IDS__username=settings.username
IDS__imasdb=settings.imasdb

##################################################################
#initialise __batch args needed for Batch class

parameters__databases__batch=[]
parameters__sheet_names_kinetic_prof__batch=[]
parameters__sheet_names_rotation__batch=[]
parameters__var_names_rotation__batch=[]
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
NEMO_run__dir_NEMO__batch=[]
NEMO_run__nmarker__batch=[]
NEMO_run__fokker_flag__batch=[]
MARS_read__tail_U__batch=[]
MARS_read__tail_M__batch=[]
MARS_read__tail_L__batch=[]
MARS_read__settings__batch=[]
MARS_read__flags__batch=[]
RMP_study__name__batch=[]
RMP_study__dir_input_database__batch=[]
RMP_study__filepaths_kinetic_profiles__batch=[]
RMP_study__filepaths_equilibrium__batch=[]
RMP_study__filepaths_additional_data__batch=[]
RMP_study__filepaths_3D_field_U__batch=[]
RMP_study__filepaths_3D_field_M__batch=[]
RMP_study__filepaths_3D_field_L__batch=[]
IDS__shot__batch=[]
IDS__run__batch=[]
IDS__username__batch=[]
IDS__imasdb__batch=[]
IDS__target_IDS_shot__batch=[]
IDS__target_IDS_run__batch=[]

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
    parameters__var_name_rotation, \
    parameters__kinetic_prof_n, \
    RMP_study__filepath_kinetic_profiles, \
    RMP_study__filepath_equilibrium \
    in zip(
        parameters__databases,
        parameters__sheet_names_kinetic_prof,
        parameters__sheet_names_rotation,
        parameters__var_names_rotation,
        parameters__kinetic_profs_n,
        RMP_study__filepaths_kinetic_profiles,
        RMP_study__filepaths_equilibrium
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
                                        parameters__var_names_rotation__batch.append(parameters__var_name_rotation)
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
                                        LOCUST_run__dir_LOCUST__batch.append("'{}'".format(str(support.dir_locust / parameters__database / RMP_study__name / parameters__parameter_string)))
                                        LOCUST_run__dir_input__batch.append("'{}'".format(str(support.dir_input_files / parameters__database / RMP_study__name / parameters__parameter_string)))
                                        LOCUST_run__dir_output__batch.append("'{}'".format(str(support.dir_output_files / parameters__database / RMP_study__name / parameters__parameter_string)))
                                        LOCUST_run__dir_cache__batch.append("'{}'".format(str(support.dir_cache_files / parameters__database / RMP_study__name))) #one level less to pool cache files into same directory across simulations
                                        LOCUST_run__system_name__batch.append(LOCUST_run__system_name)
                                        LOCUST_run__repo_URL__batch.append(LOCUST_run__repo_URL)
                                        LOCUST_run__commit_hash__batch.append(LOCUST_run__commit_hash)
                                        LOCUST_run__settings_prec_mod__batch.append(LOCUST_run__settings_prec_mod)
                                        LOCUST_run__flags__batch.append(LOCUST_run__flags)
                                        NEMO_run__dir_NEMO__batch.append(NEMO_run__dir_NEMO)
                                        NEMO_run__nmarker__batch.append(NEMO_run__nmarker)
                                        NEMO_run__fokker_flag__batch.append(NEMO_run__fokker_flag)
                                        MARS_read__tail_U__batch.append(MARS_read__tail_U)
                                        MARS_read__tail_M__batch.append(MARS_read__tail_M)
                                        MARS_read__tail_L__batch.append(MARS_read__tail_L)
                                        MARS_read__settings__batch.append(MARS_read__settings)
                                        MARS_read__flags__batch.append(MARS_read__flags)
                                        RMP_study__name__batch.append(RMP_study__name)
                                        RMP_study__dir_input_database__batch.append(RMP_study__dir_input_database)
                                        RMP_study__filepaths_kinetic_profiles__batch.append(RMP_study__filepath_kinetic_profiles)
                                        RMP_study__filepaths_equilibrium__batch.append(RMP_study__filepath_equilibrium)
                                        RMP_study__filepaths_additional_data__batch.append(RMP_study__filepaths_additional_data)
                                        
                                        #find path to 3D field corresponding to desired parameters here
                                        RMP_study__filepaths_3D_field_head=RMP_study__dir_input_database / parameters__database / folder_name_DataMarsf 
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

                                        IDS__shot__batch.append(IDS__shot)
                                        IDS__run__batch.append(IDS__run)
                                        IDS__username__batch.append(IDS__username)
                                        IDS__imasdb__batch.append(IDS__imasdb)
                                        IDS__target_IDS_shot__batch.append(target_IDS_dispatch_shot[parameters__database])
                                        IDS__target_IDS_run__batch.append(target_IDS_dispatch_run[parameters__database][parameters__kinetic_prof_Pr_string][parameters__kinetic_prof_tF_tE_string])

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
    parameters__var_name_rotation=parameters__var_names_rotation__batch,
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
    NEMO_run__dir_NEMO=NEMO_run__dir_NEMO__batch,
    NEMO_run__nmarker=NEMO_run__nmarker__batch,
    NEMO_run__fokker_flag=NEMO_run__fokker_flag__batch,
    MARS_read__tail_U=MARS_read__tail_U__batch,
    MARS_read__tail_M=MARS_read__tail_M__batch,
    MARS_read__tail_L=MARS_read__tail_L__batch,
    MARS_read__settings=MARS_read__settings__batch,
    MARS_read__flags=MARS_read__flags__batch,
    RMP_study__name=RMP_study__name__batch,
    RMP_study__dir_input_database=RMP_study__dir_input_database__batch,
    RMP_study__filepath_kinetic_profiles=RMP_study__filepaths_kinetic_profiles__batch,
    RMP_study__filepath_equilibrium=RMP_study__filepaths_equilibrium__batch,
    RMP_study__filepath_additional_data=RMP_study__filepaths_additional_data__batch,
    RMP_study__filepaths_3D_field_U=RMP_study__filepaths_3D_field_U__batch,
    RMP_study__filepaths_3D_field_M=RMP_study__filepaths_3D_field_M__batch,
    RMP_study__filepaths_3D_field_L=RMP_study__filepaths_3D_field_L__batch,
    IDS__shot=IDS__shot__batch,
    IDS__run=IDS__run__batch,
    IDS__username=IDS__username__batch,
    IDS__imasdb=IDS__imasdb__batch,
    IDS__target_IDS_shot=IDS__target_IDS_shot__batch,
    IDS__target_IDS_run=IDS__target_IDS_run__batch
    )
RMP_batch_run.launch(workflow_filepath='RMP_study_run_static.py',system_name='TITAN')   

#################################
 
##################################################################
 
###################################################################################################