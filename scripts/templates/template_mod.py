#template_mod.py
 
"""
Samuel Ward
14/10/19
----
module holding supporting data for template_launch
---
 
notes:         
    mostly dispatch tables mapping excel files to IDSs, initialising blank hyperparameter lists and things like that
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
    import settings
except:
    raise ImportError("ERROR: LOCUST_IO/src/settings.py could not be imported!\nreturning\n") 
    sys.exit(1)

################################################################## 
#Main 

#file structure things
path_template_mod=pathlib.Path(os.path.dirname(os.path.realpath(__file__))) / 'template_mod.py'
path_template_launch=pathlib.Path(os.path.dirname(os.path.realpath(__file__))) / 'template_launch.py'
path_template_run=pathlib.Path(os.path.dirname(os.path.realpath(__file__))) / 'template_run.py'

parameters__kinetic_profs_tF_tE__dispatch={}
parameters__kinetic_profs_tF_tE__dispatch[0.5]='05'
parameters__kinetic_profs_tF_tE__dispatch[0.57]='057'
parameters__kinetic_profs_tF_tE__dispatch[0.65]='065'
parameters__kinetic_profs_tF_tE__dispatch[0.72]='072'
parameters__kinetic_profs_tF_tE__dispatch[0.73]='073'
parameters__kinetic_profs_tF_tE__dispatch[1.]='1'
parameters__kinetic_profs_tF_tE__dispatch[2.]='2'
parameters__kinetic_profs_Pr__dispatch={} #prandl number
parameters__kinetic_profs_Pr__dispatch[0.3]='03'
parameters__kinetic_profs_Pr__dispatch[1.]='1'

#dispatch table matching parameter values to corresponding IDS shot/run numbers
#run depends on three parameters - sp dispatch table needs to be three levels deep - first level is scenario, second is Prandl number and third  is tF/tE - after that comes requested data
#XXX if multiple kinetic profile types (e.g. nT=0.2ne, nT=0.5) exist for same prandl number/tFtE then sheet_name_kinetic_prof will need to be made into its own dispatch level

#target_IDS_dispatch[scenario_name][prandl_number][tftE][requested_data_type]
target_IDS_dispatch={}
target_IDS_dispatch['ITER_5MAH_case1']={}
target_IDS_dispatch['ITER_5MAH_case1']['03']={} 
target_IDS_dispatch['ITER_5MAH_case1']['03']['2']={}
target_IDS_dispatch['ITER_5MAH_case1']['03']['2']['shot']=101007
target_IDS_dispatch['ITER_5MAH_case1']['03']['2']['run']=0
target_IDS_dispatch['ITER_5MAH_case1']['03']['2']['sheet_name_kinetic_prof']='H-5MA-20EC-10NBI'
target_IDS_dispatch['ITER_5MAH_case1']['03']['2']['sheet_name_rotation']='Pr=0.3'
target_IDS_dispatch['ITER_5MAH_case1']['03']['2']['var_name_rotation']='Vt(tF/tE=2)'
target_IDS_dispatch['ITER_5MAH_case1']['03']['1']={}
target_IDS_dispatch['ITER_5MAH_case1']['03']['1']['shot']=101007
target_IDS_dispatch['ITER_5MAH_case1']['03']['1']['run']=1 
target_IDS_dispatch['ITER_5MAH_case1']['03']['1']['sheet_name_kinetic_prof']='H-5MA-20EC-10NBI'
target_IDS_dispatch['ITER_5MAH_case1']['03']['1']['sheet_name_rotation']='Pr=0.3'
target_IDS_dispatch['ITER_5MAH_case1']['03']['1']['var_name_rotation']='Vt(tF/tE=1)'
target_IDS_dispatch['ITER_5MAH_case1']['03']['065']={}
target_IDS_dispatch['ITER_5MAH_case1']['03']['065']['shot']=101007 
target_IDS_dispatch['ITER_5MAH_case1']['03']['065']['run']=2 
target_IDS_dispatch['ITER_5MAH_case1']['03']['065']['sheet_name_kinetic_prof']='H-5MA-20EC-10NBI'
target_IDS_dispatch['ITER_5MAH_case1']['03']['065']['sheet_name_rotation']='Pr=0.3'
target_IDS_dispatch['ITER_5MAH_case1']['03']['065']['var_name_rotation']='Vt(tF/tE=0.65)'
target_IDS_dispatch['ITER_7d5MAHalfB_case2']={}
target_IDS_dispatch['ITER_7d5MAHalfB_case2']['03']={} 
target_IDS_dispatch['ITER_7d5MAHalfB_case2']['03'][None]={}# Pr=0.3
target_IDS_dispatch['ITER_7d5MAHalfB_case2']['03'][None]['shot']=131020
target_IDS_dispatch['ITER_7d5MAHalfB_case2']['03'][None]['run']=0
target_IDS_dispatch['ITER_7d5MAHalfB_case2']['03'][None]['sheet_name_kinetic_prof']='nT=0.2ne'
target_IDS_dispatch['ITER_7d5MAHalfB_case2']['03'][None]['sheet_name_rotation']='Pr=0.3'
target_IDS_dispatch['ITER_7d5MAHalfB_case2']['03'][None]['var_name_rotation']=None
target_IDS_dispatch['ITER_7d5MAHalfB_case2']['03']['2']={}
target_IDS_dispatch['ITER_7d5MAHalfB_case2']['03']['2']['shot']=131021
target_IDS_dispatch['ITER_7d5MAHalfB_case2']['03']['2']['run']=0
target_IDS_dispatch['ITER_7d5MAHalfB_case2']['03']['2']['sheet_name_kinetic_prof']='nT=0.5ne'
target_IDS_dispatch['ITER_7d5MAHalfB_case2']['03']['2']['sheet_name_rotation']='Pr=0.3'
target_IDS_dispatch['ITER_7d5MAHalfB_case2']['03']['2']['var_name_rotation']='Vt(tF/tE=2)'
target_IDS_dispatch['ITER_7d5MAHalfB_case2']['03']['1']={}
target_IDS_dispatch['ITER_7d5MAHalfB_case2']['03']['1']['shot']=131021
target_IDS_dispatch['ITER_7d5MAHalfB_case2']['03']['1']['run']=1
target_IDS_dispatch['ITER_7d5MAHalfB_case2']['03']['1']['sheet_name_kinetic_prof']='nT=0.5ne'
target_IDS_dispatch['ITER_7d5MAHalfB_case2']['03']['1']['sheet_name_rotation']='Pr=0.3'
target_IDS_dispatch['ITER_7d5MAHalfB_case2']['03']['1']['var_name_rotation']='Vt(tF/tE=1)'
target_IDS_dispatch['ITER_7d5MAHalfB_case2']['03']['057']={}
target_IDS_dispatch['ITER_7d5MAHalfB_case2']['03']['057']['shot']=131021
target_IDS_dispatch['ITER_7d5MAHalfB_case2']['03']['057']['run']=2
target_IDS_dispatch['ITER_7d5MAHalfB_case2']['03']['057']['sheet_name_kinetic_prof']='nT=0.5ne'
target_IDS_dispatch['ITER_7d5MAHalfB_case2']['03']['057']['sheet_name_rotation']='Pr=0.3'
target_IDS_dispatch['ITER_7d5MAHalfB_case2']['03']['057']['var_name_rotation']='Vt(tF/tE=0.57)'
target_IDS_dispatch['ITER_7d5MAHalfB_case2']['03'][None]={}
target_IDS_dispatch['ITER_7d5MAHalfB_case2']['03'][None]['shot']=131022
target_IDS_dispatch['ITER_7d5MAHalfB_case2']['03'][None]['run']=0
target_IDS_dispatch['ITER_7d5MAHalfB_case2']['03'][None]['sheet_name_kinetic_prof']='nT=0.76ne'
target_IDS_dispatch['ITER_7d5MAHalfB_case2']['03'][None]['sheet_name_rotation']='Pr=0.3'
target_IDS_dispatch['ITER_7d5MAHalfB_case2']['03'][None]['var_name_rotation']=None
target_IDS_dispatch['ITER_7d5MAHalfB_case2']['03'][None]={}
target_IDS_dispatch['ITER_7d5MAHalfB_case2']['03'][None]['shot']=131023
target_IDS_dispatch['ITER_7d5MAHalfB_case2']['03'][None]['run']=0
target_IDS_dispatch['ITER_7d5MAHalfB_case2']['03'][None]['sheet_name_kinetic_prof']='nT<<ne'
target_IDS_dispatch['ITER_7d5MAHalfB_case2']['03'][None]['sheet_name_rotation']='Pr=0.3'
target_IDS_dispatch['ITER_7d5MAHalfB_case2']['03'][None]['var_name_rotation']=None
target_IDS_dispatch['ITER_15MAQ5_case4']={} 
target_IDS_dispatch['ITER_15MAQ5_case4']['1']={} 
target_IDS_dispatch['ITER_15MAQ5_case4']['1']['2']={}
target_IDS_dispatch['ITER_15MAQ5_case4']['1']['2']['shot']=131024
target_IDS_dispatch['ITER_15MAQ5_case4']['1']['2']['run']=0
target_IDS_dispatch['ITER_15MAQ5_case4']['1']['2']['sheet_name_kinetic_prof']='Out_iterDD.iterDDL-R'
target_IDS_dispatch['ITER_15MAQ5_case4']['1']['2']['sheet_name_rotation']='Pr=1'
target_IDS_dispatch['ITER_15MAQ5_case4']['1']['2']['var_name_rotation']='Vt(tF/tE=2)'
target_IDS_dispatch['ITER_15MAQ5_case4']['1']['1']={}
target_IDS_dispatch['ITER_15MAQ5_case4']['1']['1']['shot']=131024
target_IDS_dispatch['ITER_15MAQ5_case4']['1']['1']['run']=1
target_IDS_dispatch['ITER_15MAQ5_case4']['1']['1']['sheet_name_kinetic_prof']='Out_iterDD.iterDDL-R'
target_IDS_dispatch['ITER_15MAQ5_case4']['1']['1']['sheet_name_rotation']='Pr=1'
target_IDS_dispatch['ITER_15MAQ5_case4']['1']['1']['var_name_rotation']='Vt(tF/tE=1)'
target_IDS_dispatch['ITER_15MAQ5_case4']['1']['05']={}
target_IDS_dispatch['ITER_15MAQ5_case4']['1']['05']['shot']=131024
target_IDS_dispatch['ITER_15MAQ5_case4']['1']['05']['run']=2
target_IDS_dispatch['ITER_15MAQ5_case4']['1']['05']['sheet_name_kinetic_prof']='Out_iterDD.iterDDL-R'
target_IDS_dispatch['ITER_15MAQ5_case4']['1']['05']['sheet_name_rotation']='Pr=1'
target_IDS_dispatch['ITER_15MAQ5_case4']['1']['05']['var_name_rotation']='Vt(tF/tE=0.5)'
target_IDS_dispatch['ITER_15MAQ5_case4']['03']={} 
target_IDS_dispatch['ITER_15MAQ5_case4']['03']['2']={}
target_IDS_dispatch['ITER_15MAQ5_case4']['03']['2']['shot']=131024
target_IDS_dispatch['ITER_15MAQ5_case4']['03']['2']['run']=3
target_IDS_dispatch['ITER_15MAQ5_case4']['03']['2']['sheet_name_kinetic_prof']='Out_iterDD.iterDDL-R'
target_IDS_dispatch['ITER_15MAQ5_case4']['03']['2']['sheet_name_rotation']='Pr=0.3'
target_IDS_dispatch['ITER_15MAQ5_case4']['03']['2']['var_name_rotation']='Vt(tF/tE=2)'
target_IDS_dispatch['ITER_15MAQ5_case4']['03']['1']={}
target_IDS_dispatch['ITER_15MAQ5_case4']['03']['1']['shot']=131024
target_IDS_dispatch['ITER_15MAQ5_case4']['03']['1']['run']=4
target_IDS_dispatch['ITER_15MAQ5_case4']['03']['1']['sheet_name_kinetic_prof']='Out_iterDD.iterDDL-R'
target_IDS_dispatch['ITER_15MAQ5_case4']['03']['1']['sheet_name_rotation']='Pr=0.3'
target_IDS_dispatch['ITER_15MAQ5_case4']['03']['1']['var_name_rotation']='Vt(tF/tE=1)'
target_IDS_dispatch['ITER_15MAQ5_case4']['03']['073']={}
target_IDS_dispatch['ITER_15MAQ5_case4']['03']['073']['shot']=131024
target_IDS_dispatch['ITER_15MAQ5_case4']['03']['073']['run']=5
target_IDS_dispatch['ITER_15MAQ5_case4']['03']['073']['sheet_name_kinetic_prof']='Out_iterDD.iterDDL-R'
target_IDS_dispatch['ITER_15MAQ5_case4']['03']['073']['sheet_name_rotation']='Pr=0.3'
target_IDS_dispatch['ITER_15MAQ5_case4']['03']['073']['var_name_rotation']='Vt(tF/tE=0.73)'
target_IDS_dispatch['ITER_15MAQ10_case5']={}
target_IDS_dispatch['ITER_15MAQ10_case5']['1']={} 
target_IDS_dispatch['ITER_15MAQ10_case5']['1']['2']={}
target_IDS_dispatch['ITER_15MAQ10_case5']['1']['2']['shot']=131025
target_IDS_dispatch['ITER_15MAQ10_case5']['1']['2']['run']=0
target_IDS_dispatch['ITER_15MAQ10_case5']['1']['2']['sheet_name_kinetic_prof']='Flat n'
target_IDS_dispatch['ITER_15MAQ10_case5']['1']['2']['sheet_name_rotation']='Flat n,Pr=1'
target_IDS_dispatch['ITER_15MAQ10_case5']['1']['2']['var_name_rotation']='Vt(tF/tE=2)'
target_IDS_dispatch['ITER_15MAQ10_case5']['1']['1']={}
target_IDS_dispatch['ITER_15MAQ10_case5']['1']['1']['shot']=131025
target_IDS_dispatch['ITER_15MAQ10_case5']['1']['1']['run']=1
target_IDS_dispatch['ITER_15MAQ10_case5']['1']['1']['sheet_name_kinetic_prof']='Flat n'
target_IDS_dispatch['ITER_15MAQ10_case5']['1']['1']['sheet_name_rotation']='Flat n,Pr=1'
target_IDS_dispatch['ITER_15MAQ10_case5']['1']['1']['var_name_rotation']='Vt(tF/tE=1)'
target_IDS_dispatch['ITER_15MAQ10_case5']['1']['05']={} #lowest rotation
target_IDS_dispatch['ITER_15MAQ10_case5']['1']['05']['shot']=131025
target_IDS_dispatch['ITER_15MAQ10_case5']['1']['05']['run']=2
target_IDS_dispatch['ITER_15MAQ10_case5']['1']['05']['sheet_name_kinetic_prof']='Flat n'
target_IDS_dispatch['ITER_15MAQ10_case5']['1']['05']['sheet_name_rotation']='Flat n,Pr=1'
target_IDS_dispatch['ITER_15MAQ10_case5']['1']['05']['var_name_rotation']='Vt(tF/tE=0.5)'
target_IDS_dispatch['ITER_15MAQ10_case5']['03']={} 
target_IDS_dispatch['ITER_15MAQ10_case5']['03']['2']={} #highest rotation
target_IDS_dispatch['ITER_15MAQ10_case5']['03']['2']['shot']=131025 
target_IDS_dispatch['ITER_15MAQ10_case5']['03']['2']['run']=3
target_IDS_dispatch['ITER_15MAQ10_case5']['03']['2']['sheet_name_kinetic_prof']='Flat n'
target_IDS_dispatch['ITER_15MAQ10_case5']['03']['2']['sheet_name_rotation']='Flat n, Pr=0.3'
target_IDS_dispatch['ITER_15MAQ10_case5']['03']['2']['var_name_rotation']='Vt(tF/tE=2)'
target_IDS_dispatch['ITER_15MAQ10_case5']['03']['1']={}
target_IDS_dispatch['ITER_15MAQ10_case5']['03']['1']['shot']=131025
target_IDS_dispatch['ITER_15MAQ10_case5']['03']['1']['run']=4
target_IDS_dispatch['ITER_15MAQ10_case5']['03']['1']['sheet_name_kinetic_prof']='Flat n'
target_IDS_dispatch['ITER_15MAQ10_case5']['03']['1']['sheet_name_rotation']='Flat n, Pr=0.3'
target_IDS_dispatch['ITER_15MAQ10_case5']['03']['1']['var_name_rotation']='Vt(tF/tE=1)'
target_IDS_dispatch['ITER_15MAQ10_case5']['03']['072']={}
target_IDS_dispatch['ITER_15MAQ10_case5']['03']['072']['shot']=131025
target_IDS_dispatch['ITER_15MAQ10_case5']['03']['072']['run']=5
target_IDS_dispatch['ITER_15MAQ10_case5']['03']['072']['sheet_name_kinetic_prof']='Flat n'
target_IDS_dispatch['ITER_15MAQ10_case5']['03']['072']['sheet_name_rotation']='Flat n, Pr=0.3'
target_IDS_dispatch['ITER_15MAQ10_case5']['03']['072']['var_name_rotation']='Vt(tF/tE=0.72)'
target_IDS_dispatch['ITER_15MAQ10_case5'][None]={}
target_IDS_dispatch['ITER_15MAQ10_case5'][None][None]={}
target_IDS_dispatch['ITER_15MAQ10_case5'][None][None]['shot']=131026
target_IDS_dispatch['ITER_15MAQ10_case5'][None][None]['run']=0
target_IDS_dispatch['ITER_15MAQ10_case5'][None][None]['sheet_name_kinetic_prof']='Peaked n'
target_IDS_dispatch['ITER_15MAQ10_case5'][None][None]['sheet_name_rotation']=None
target_IDS_dispatch['ITER_15MAQ10_case5'][None][None]['var_name_rotation']=None

#dispatch tables for species stored in IDSs and prec_mod
table_species_AZ={} #A,Z
table_species_LOCUST={}
table_species_AZ['deuterium']=[2.,1.] #need to stay floats
table_species_LOCUST['deuterium']='AD'
table_species_AZ['tritium']=[3.,1.]
table_species_LOCUST['tritium']='AT'
'''
table_species_AZ['helium3']=[3.,2.]
table_species_LOCUST['helium3']='AHe3'
table_species_AZ['helium']=[4.,2.]
table_species_LOCUST['helium']='AHe4'
table_species_AZ['hydrogen']=[1.,1.]
table_species_LOCUST['hydrogen']='AH'
table_species_AZ['beryllium']=[9.,4.]
table_species_LOCUST['beryllium']='ABe9'
table_species_AZ['neon']=[20.2,10.]
table_species_LOCUST['neon']='ANe20'
table_species_AZ['tungsten']=[183.8,74.]
table_species_LOCUST['tungsten']='AW184'
'''

fraction_beryllium=0.02
fraction_neon=0.002

config_beam_dispatch={}
config_beam_dispatch['on']={}
config_beam_dispatch['on']['on']={}
config_beam_dispatch['on']['on']['shot']=44
config_beam_dispatch['on']['on']['run']=55
config_beam_dispatch['on']['on']['imasdb']='ITER_MD'
config_beam_dispatch['off']={}
config_beam_dispatch['off']['off']={}
config_beam_dispatch['off']['off']['shot']=44
config_beam_dispatch['off']['off']['run']=22
config_beam_dispatch['off']['off']['imasdb']='ITER_MD'
config_beam_dispatch['off']['on']={}
config_beam_dispatch['off']['on']['shot']=44
config_beam_dispatch['off']['on']['run']=33
config_beam_dispatch['off']['on']['imasdb']='ITER_MD'
config_beam_dispatch['default']={}
config_beam_dispatch['default']['default']={}
config_beam_dispatch['default']['default']['shot']=130011
config_beam_dispatch['default']['default']['run']=1
config_beam_dispatch['default']['default']['imasdb']='ITER'
config_beam_1='default' #assign to these variables in run scripts which type of beam configs we want
config_beam_2='default'

##################################################################
#initialise __batch args needed for Batch class
args_batch={}
args_batch['parameters__sheet_name_kinetic_prof']=[]
args_batch['parameters__sheet_name_rotation']=[]
args_batch['parameters__var_name_rotation']=[]
args_batch['parameters__toroidal_mode_numbers']=[]
args_batch['LOCUST_run__dir_LOCUST']=[]
args_batch['LOCUST_run__dir_LOCUST_source']=[]
args_batch['LOCUST_run__dir_input']=[]
args_batch['LOCUST_run__dir_output']=[]
args_batch['LOCUST_run__dir_cache']=[]
args_batch['LOCUST_run__environment_name']=[]
args_batch['LOCUST_run__repo_URL']=[]
args_batch['LOCUST_run__commit_hash']=[]
args_batch['LOCUST_run__settings_prec_mod']=[]
args_batch['LOCUST_run__flags']=[]
args_batch['NEMO_run__dir_NEMO']=[]
args_batch['NEMO_run__xml_settings']=[]
args_batch['MARS_read__tail_U']=[]
args_batch['MARS_read__tail_M']=[]
args_batch['MARS_read__tail_L']=[]
args_batch['MARS_read__settings']=[]
args_batch['MARS_read__flags']=[]
args_batch['RMP_study__name']=[]
args_batch['RMP_study__filepath_kinetic_profiles']=[]
args_batch['RMP_study__filepath_equilibrium']=[]
args_batch['RMP_study__filepath_additional_data']=[]
args_batch['RMP_study__filepaths_3D_fields_U']=[]
args_batch['RMP_study__filepaths_3D_fields_M']=[]
args_batch['RMP_study__filepaths_3D_fields_L']=[]
args_batch['IDS__shot']=[]
args_batch['IDS__run']=[]
args_batch['IDS__username']=[]
args_batch['IDS__imasdb']=[]
args_batch['IDS__target_IDS_shot']=[]
args_batch['IDS__target_IDS_run']=[]
args_batch['IDS__NBI_shot']=[]
args_batch['IDS__NBI_run']=[]
args_batch['IDS__NBI_imasdb']=[]
args_batch['workflow__commands']=[]

commit_hash_dispatch={} #select LOCUST commit hash based on system
commit_hash_dispatch['GPU6']='1c08dca5308cf868771f9deb1f5a4114a0e74378'
commit_hash_dispatch['GPU8']='aea255bae105982a83a9cd1c3d07762284e3461a'
commit_hash_dispatch['GPU9']='aea255bae105982a83a9cd1c3d07762284e3461a'
commit_hash_dispatch['GPU10']='aea255bae105982a83a9cd1c3d07762284e3461a'
commit_hash_dispatch['TITAN']='d1281155ec7e584744536fc0865ad4c2b39cb479'
commit_hash_dispatch['VIKING']='02f4ec69692da67dc2c12bc9e2c2175e689a9a7c'

##################################################################
#define parameters which are fixed throughout a parameter scan - if we want to vary then add as a layer in the for loops

folder_name_DataMarsf='DataMarsf' #3D field directory name however this can sometimes vary between scenarios e.g. if using vacuum field
folder_name_DataEq='DataEq' #equilibrium 

#fixed parameters needed by LOCUST_run
LOCUST_run__environment_name='TITAN'
LOCUST_run__repo_URL=f"'{settings.repo_URL_LOCUST}'"
LOCUST_run__commit_hash="'{}'".format(commit_hash_dispatch[LOCUST_run__environment_name])

#fixed parameters needed for NEMO_run
NEMO_run__dir_NEMO=pathlib.Path('/home') / 'ITER' / f'{settings.username}' / 'scratch' / 'nemo'
NEMO_run__fokker_flag=0

#fixed parameters needed by MARS_read
MARS_read__tail_U='_U_PLS'
MARS_read__tail_M='_M_PLS'
MARS_read__tail_L='_L_PLS'
MARS_read__tails=[MARS_read__tail_U,MARS_read__tail_M,MARS_read__tail_L]
MARS_read__settings={}
MARS_read__settings['TAIL']="{}".format(MARS_read__tails)
MARS_read__flags={}

#IMAS parameters to specify location of locally made input IDS
IDS__shot=1
IDS__run=1
IDS__username=settings.username
IDS__imasdb=settings.imasdb

#################################
 
##################################################################
 
###################################################################################################