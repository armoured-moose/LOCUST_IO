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
try:
    import support
except:
    raise ImportError("ERROR: LOCUST_IO/src/support.py could not be imported!\nreturning\n") 
    sys.exit(1)

################################################################## 
#Main 

##################################################################
#define parameters which are fixed throughout a parameter scan - if we want to vary then add as a layer in the for loops

commit_hash_dispatch={} #select LOCUST commit hash based on system
commit_hash_dispatch['GPU6']='053aefeeccab47bedb11de691a979e769c29630f'
commit_hash_dispatch['GPU7']='053aefeeccab47bedb11de691a979e769c29630f'
commit_hash_dispatch['GPU8']='b304bee99a485a9b44d8350cfa141ed9c1b7d19a'
commit_hash_dispatch['GPU9']='b304bee99a485a9b44d8350cfa141ed9c1b7d19a'
commit_hash_dispatch['GPU10']='b304bee99a485a9b44d8350cfa141ed9c1b7d19a'
commit_hash_dispatch['CUMULUS']='244736c951eba6f788e11f3a1a68553a4abcc2ba'
commit_hash_dispatch['TITAN']='0c2bbb9eab574bb3b6a5d48a8a4cd8ddc6448ee4'
commit_hash_dispatch['VIKING']='908df2997978f99a9f871acb0f4031e56f505727'

#fixed parameters needed by LOCUST_run
LOCUST_run__environment_name='TITAN'
LOCUST_run__repo_URL=f"'{settings.repo_URL_LOCUST}'"
LOCUST_run__commit_hash="'{}'".format(commit_hash_dispatch[LOCUST_run__environment_name])

#IMAS parameters to specify location of locally made input IDS
IDS__shot=1
IDS__run=1
IDS__username=settings.username
IDS__imasdb=settings.imasdb

#file structure things
path_template_mod=pathlib.Path(os.path.dirname(os.path.realpath(__file__))) / 'template_mod.py'
path_template_launch=pathlib.Path(os.path.dirname(os.path.realpath(__file__))) / 'template_launch.py'
path_template_run=pathlib.Path(os.path.dirname(os.path.realpath(__file__))) / 'template_run.py'

RMP_study__dir_input_database=support.dir_input_files / 'ITER_fields_yueqiang' / 'DataBase'
RMP_study__filepaths_additional_data=support.dir_input_files / 'ITER_additional_data'

folder_name_DataMarsf='DataMarsf' #3D field directory name however this can sometimes vary between scenarios e.g. if using vacuum field
folder_name_DataEq='DataEq' #equilibrium 

#fixed parameters needed by MARS_read
MARS_read__tail_U='_U_PLS'
MARS_read__tail_M='_M_PLS'
MARS_read__tail_L='_L_PLS'
MARS_read__tails=[MARS_read__tail_U,MARS_read__tail_M,MARS_read__tail_L]

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
config_beam_dispatch['on']['on']['user']='public'
config_beam_dispatch['off']={}
config_beam_dispatch['off']['off']={}
config_beam_dispatch['off']['off']['shot']=44
config_beam_dispatch['off']['off']['run']=22
config_beam_dispatch['off']['off']['imasdb']='ITER_MD'
config_beam_dispatch['off']['off']['user']='public'
config_beam_dispatch['off']['on']={}
config_beam_dispatch['off']['on']['shot']=44
config_beam_dispatch['off']['on']['run']=33
config_beam_dispatch['off']['on']['imasdb']='ITER_MD'
config_beam_dispatch['off']['on']['user']='public'
config_beam_dispatch['off']['diagnostic']={}
config_beam_dispatch['off']['diagnostic']['shot']=IDS__shot
config_beam_dispatch['off']['diagnostic']['run']=IDS__run+1 #just fill the adjacent run when generating our own NBI
config_beam_dispatch['off']['diagnostic']['imasdb']=IDS__imasdb
config_beam_dispatch['off']['diagnostic']['user']=IDS__username
config_beam_dispatch['on']['diagnostic']={}
config_beam_dispatch['on']['diagnostic']['shot']=IDS__shot
config_beam_dispatch['on']['diagnostic']['run']=IDS__run+1 #just fill the adjacent run when generating our own NBI
config_beam_dispatch['on']['diagnostic']['imasdb']=IDS__imasdb
config_beam_dispatch['on']['diagnostic']['user']=IDS__username
config_beam_dispatch['default']={}
config_beam_dispatch['default']['default']={}
config_beam_dispatch['default']['default']['shot']=130011
config_beam_dispatch['default']['default']['run']=1
config_beam_dispatch['default']['default']['imasdb']='ITER'
config_beam_dispatch['default']['default']['user']='public'

config_beam_1='default' #assign to these variables in run scripts which type of beam configs we want
config_beam_2='default'

##################################################################
#initialise all the lists of arguments passed to the batch study from the launch script
args_batch={}

args_batch_names=['parameters__sheet_name_kinetic_prof',
                  'parameters__sheet_name_rotation',
                  'parameters__var_name_rotation',
                  'parameters__toroidal_mode_numbers',
                  'LOCUST_run__dir_LOCUST',
                  'LOCUST_run__dir_LOCUST_source',
                  'LOCUST_run__dir_input',
                  'LOCUST_run__dir_output',
                  'LOCUST_run__dir_cache',
                  'LOCUST_run__environment_name',
                  'LOCUST_run__repo_URL',
                  'LOCUST_run__commit_hash',
                  'LOCUST_run__settings_prec_mod',
                  'LOCUST_run__flags',
                  'NEMO_run__dir_NEMO',
                  'NEMO_run__xml_settings',
                  'BBNBI_run__dir_BBNBI',
                  'BBNBI_run__xml_settings',
                  'BBNBI_run__number_particles',
                  'MARS_read__tail_U',
                  'MARS_read__tail_M',
                  'MARS_read__tail_L',
                  'MARS_read__settings',
                  'MARS_read__flags',
                  'MARS_read__dir_MARS_builder',
                  'RMP_study__name',
                  'RMP_study__filepath_kinetic_profiles',
                  'RMP_study__filepath_equilibrium',
                  'RMP_study__filepath_additional_data',
                  'RMP_study__filepaths_3D_fields_U',
                  'RMP_study__filepaths_3D_fields_M',
                  'RMP_study__filepaths_3D_fields_L',
                  'RMP_study__workflow_commands',
                  'IDS__shot',
                  'IDS__run',
                  'IDS__username',
                  'IDS__imasdb',
                  'IDS__target_IDS_shot',
                  'IDS__target_IDS_run',
                  'IDS__NBI_shot',
                  'IDS__NBI_run',
                  'IDS__NBI_imasdb',
                  'IDS__NBI_username']

for arg_name in args_batch_names:
    args_batch[arg_name]=[]

#################################
 
##################################################################

###################################################################################################