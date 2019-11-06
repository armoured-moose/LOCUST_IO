#RMP_study_run.py

'''
Samuel Ward
14/10/2019
----
workflow designed for RMP studies (with static RMP field)
---
notes: 
    since RMP field is static, total field is combined before LOCUST simulation
    at first care was taken to decide as many parameters as possible outside of this script (best practice to be able to reuse this script) however I ran out of time and started deriving information herein
    all filepaths are absolute at the beginning
TODO:
    NEED TO READ DT KINETIC PROFILES AND THEN JUST READ THE FIRST VALUE OF THE RESPECTIVE KINETIC PROFILES OF THE OTHER ELEMENTS IN ORDER TO CALCULATE RELATIVE CONCENTATIONS AND ZEFF 
    add index to dir_MARS_builder cache run folder location
---
'''


##################################################################
#Preamble

try:
    import sys
    import subprocess
    import pathlib
    import shlex
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
    import run_scripts.workflow
except:
    raise ImportError("ERROR: LOCUST_IO/src/run_scripts/workflow.py could not be imported!\nreturning\n")
    sys.exit(1)
try:
    import run_scripts.LOCUST_run
except:
    raise ImportError("ERROR: LOCUST_IO/src/run_scripts/LOCUST_run.py could not be imported!\nreturning\n")
    sys.exit(1)
try:
    from run_scripts.MARS_builder_run import MARS_builder_run
except:
    raise ImportError("ERROR: LOCUST_IO/src/run_scripts/MARS_builder_run.py could not be imported!\nreturning\n")
    sys.exit(1)
try:
    import run_scripts.utils
except:
    raise ImportError("ERROR: LOCUST_IO/src/run_scripts/utils.py could not be imported!\nreturning\n")
    sys.exit(1)

try:
    from classes.input_classes.temperature import Temperature
except:
    raise ImportError("ERROR: LOCUST_IO/src/classes/input_classes/temperature.py could not be imported!\nreturning\n") 
    sys.exit(1)
try:
    from classes.input_classes.number_density import Number_Density
except:
    raise ImportError("ERROR: LOCUST_IO/src/classes/input_classes/number_density.py could not be imported!\nreturning\n") 
    sys.exit(1)
try:
    from classes.input_classes.rotation import Rotation
except:
    raise ImportError("ERROR: LOCUST_IO/src/classes/input_classes/rotation.py could not be imported!\nreturning\n") 
    sys.exit(1)
try:
    from classes.input_classes.equilibrium import Equilibrium
except:
    raise ImportError("ERROR: LOCUST_IO/src/classes/input_classes/equilibrium.py could not be imported!\nreturning\n") 
    sys.exit(1)

try:
    import support
except:
    raise ImportError("ERROR: LOCUST_IO/src/support.py could not be imported!\nreturning\n") 
    sys.exit(1)
try:
    import settings
except:
    raise ImportError("ERROR: LOCUST_IO/src/settings.py could not be imported!\nreturning\n") 
    sys.exit(1)

##################################################################
#Main

#need to make some additions to the LOCUST_run workflow component
class LOCUST_run_RMP(run_scripts.LOCUST_run.LOCUST_run):
    def get_inputs(self,*args,**kwargs):
        """
        LOCUST_run stage for moving inputs to correct location

        notes:
            edited for RMP workflow to move instead of copy
        """

        #copy input and cache files to correct location
        for file in self.dir_input.glob('*'): #move all input files to correct location
            subprocess.run(shlex.split('mv {file} {inputdir}'.format(file=str(file),inputdir=str(self.root / settings.username / self.tokhead / settings.LOCUST_dir_inputfiles_default))),shell=False)
        for file in self.dir_cache.glob('*'): #move all cache files to correct location
            subprocess.run(shlex.split('mv {file} {cachedir}'.format(file=str(file),cachedir=str(self.root / settings.username / self.tokhead / settings.LOCUST_dir_cachefiles_default))),shell=False)


class RMP_study_run(run_scripts.workflow.Workflow):
    """
    defines a workflow which runs a 3D field RMP run

    notes:
    usage:
    """ 

    def __init__(self,
                parameters__database,
                parameters__sheet_name_kinetic_prof,
                parameters__sheet_name_rotation,
                parameters__var_name_rotation,
                parameters__kinetic_prof_n, #variables defining the parameter set
                parameters__kinetic_prof_tF_tE,
                parameters__kinetic_prof_Pr,
                parameters__toroidal_mode_number,
                parameters__phase_upper,
                parameters__phase_middle,
                parameters__phase_lower,
                parameters__rotation_upper,
                parameters__rotation_middle,
                parameters__rotation_lower, 
                parameters__parameter_string,
                LOCUST_run__dir_LOCUST, #variables used by LOCUST_run (called within this workflow)
                LOCUST_run__dir_input,
                LOCUST_run__dir_output,
                LOCUST_run__dir_cache,
                LOCUST_run__system_name,
                LOCUST_run__repo_URL,
                LOCUST_run__commit_hash,
                LOCUST_run__settings_prec_mod,
                LOCUST_run__flags,
                MARS_read__tail_U,
                MARS_read__tail_M,
                MARS_read__tail_L,
                MARS_read__settings,
                MARS_read__flags,
                RMP_study__name, #variables defining controlling this workflow
                RMP_study__dir_input_database,
                RMP_study__filepath_kinetic_profiles, 
                RMP_study__filepath_equilibrium,
                RMP_study__filepath_additional_data,
                RMP_study__filepaths_3D_field_U,
                RMP_study__filepaths_3D_field_M,
                RMP_study__filepaths_3D_field_L,
                *args,
                **kwargs):
        """
        notes:
        """


        super().__init__()


        #################################
        #read args needed for workflow steps

        self.parameters__database=parameters__database #variables defining the parameter set
        self.parameters__sheet_name_kinetic_prof=parameters__sheet_name_kinetic_prof
        self.parameters__sheet_name_rotation=parameters__sheet_name_rotation
        self.parameters__var_name_rotation=parameters__var_name_rotation
        self.parameters__kinetic_prof_n=parameters__kinetic_prof_n
        self.parameters__kinetic_prof_tF_tE=parameters__kinetic_prof_tF_tE
        self.parameters__kinetic_prof_Pr=parameters__kinetic_prof_Pr
        self.parameters__toroidal_mode_number=parameters__toroidal_mode_number
        self.parameters__phase_upper=parameters__phase_upper
        self.parameters__phase_middle=parameters__phase_middle
        self.parameters__phase_lower=parameters__phase_lower
        self.parameters__rotation_upper=parameters__rotation_upper
        self.parameters__rotation_middle=parameters__rotation_middle
        self.parameters__rotation_lower=parameters__rotation_lower
        self.parameters__parameter_string=parameters__parameter_string
        self.LOCUST_run__dir_LOCUST=pathlib.Path(LOCUST_run__dir_LOCUST) #data needed for LOCUST_run
        self.LOCUST_run__dir_input=pathlib.Path(LOCUST_run__dir_input)
        self.LOCUST_run__dir_output=pathlib.Path(LOCUST_run__dir_output)
        self.LOCUST_run__dir_cache=pathlib.Path(LOCUST_run__dir_cache)
        self.LOCUST_run__system_name=LOCUST_run__system_name
        self.LOCUST_run__repo_URL=LOCUST_run__repo_URL
        self.LOCUST_run__commit_hash=LOCUST_run__commit_hash
        self.LOCUST_run__settings_prec_mod=LOCUST_run__settings_prec_mod
        self.LOCUST_run__flags=LOCUST_run__flags
        self.MARS_read__tail_U=MARS_read__tail_U
        self.MARS_read__tail_M=MARS_read__tail_M
        self.MARS_read__tail_L=MARS_read__tail_L
        self.MARS_read__settings=MARS_read__settings
        self.MARS_read__flags=MARS_read__flags
        self.RMP_study__name=RMP_study__name #data needed for additional steps
        self.RMP_study__dir_input_database=pathlib.Path(RMP_study__dir_input_database)
        self.RMP_study__filepath_kinetic_profiles=pathlib.Path(RMP_study__filepath_kinetic_profiles)
        self.RMP_study__filepath_equilibrium=pathlib.Path(RMP_study__filepath_equilibrium)
        self.RMP_study__filepath_additional_data=pathlib.Path(RMP_study__filepath_additional_data)
        self.RMP_study__filepaths_3D_field_U=pathlib.Path(RMP_study__filepaths_3D_field_U)
        self.RMP_study__filepaths_3D_field_M=pathlib.Path(RMP_study__filepaths_3D_field_M)
        self.RMP_study__filepaths_3D_field_L=pathlib.Path(RMP_study__filepaths_3D_field_L)

        #################################
        #derive some information

        #################################
        #add workflow stages

        self.add_command(command_name='mkdir',command_function=self.setup_RMP_study_dirs,position=1) #add new workflow stages
        self.add_command(command_name='get_kinetic',command_function=self.get_kinetic_profiles,position=2) #add new workflow stages
        self.add_command(command_name='get_3D',command_function=self.get_3D_fields,position=3) #add new workflow stages
        self.add_command(command_name='get_others',command_function=self.get_other_input_files,position=4) #add new workflow stages

    def setup_RMP_study_dirs(self,*args,**kwargs):
        """
        notes:
        """

        for direc in [
                        self.LOCUST_run__dir_input,
                        self.LOCUST_run__dir_output,
                        self.LOCUST_run__dir_cache,
                        self.LOCUST_run__dir_LOCUST
                        ]:
            if not direc.is_dir(): direc.mkdir(parents=True)

    def get_kinetic_profiles(self,*args,**kwargs):
        """
        prepare kinetic profiles for LOCUST
        notes:
            extracts from excel spreadsheet provided by Yueqiang
        """


        temperatures=[]
        densities=[]
        for species in ['electrons','tritium','deuterium','helium','hydrogen','tungsten','helium3']:
            try:
                densities.append(Number_Density(ID='',data_format='EXCEL1',species=species,filename=self.RMP_study__filepath_kinetic_profiles.relative_to(support.dir_input_files),sheet_name=self.parameters__sheet_name_kinetic_prof))
            except:
                pass
        for species in ['electrons','ions']:
            temperatures.append(Temperature(ID='',data_format='EXCEL1',species=species,filename=self.RMP_study__filepath_kinetic_profiles.relative_to(support.dir_input_files),sheet_name=self.parameters__sheet_name_kinetic_prof))
        for temperature in temperatures: temperature.dump_data(data_format='LOCUST',filename=self.LOCUST_run__dir_input / 'temperature_{}'.format(temperature.properties['species']))
        for density in densities: density.dump_data(data_format='LOCUST',filename=self.LOCUST_run__dir_input / 'density_{}'.format(density.properties['species']))
        rotation=Rotation(ID='',data_format='EXCEL1',filename=self.RMP_study__filepath_kinetic_profiles.relative_to(support.dir_input_files),sheet_name=self.parameters__sheet_name_kinetic_prof,rotation_name=self.parameters__var_name_rotation,sheet_name_rotation=self.parameters__sheet_name_rotation)
        rotation.dump_data(data_format='LOCUST',filename=self.LOCUST_run__dir_input / 'rotation') 

    def get_3D_fields(self,*args,**kwargs):
        """
        prepare 3D fields for LOCUST

        notes:
            copies 3D field files from the target folder into destination and renames file correctly before running mars_builder to combine them into single field
            suited for parameter scans involving static RMP fields
        """

        for file,TAIL,section_to_remove in zip(
                        [self.RMP_study__filepaths_3D_field_U,self.RMP_study__filepaths_3D_field_M,self.RMP_study__filepaths_3D_field_L],
                        [self.MARS_read__tail_U,self.MARS_read__tail_M,self.MARS_read__tail_L],
                        ['_cU_','_cM_','_cL_']
                        ): #move all input files to correct location and add appropriate TAIL

            destination=(str(self.LOCUST_run__dir_input / file.parts[-1])+TAIL).replace(section_to_remove,'_')
            HEAD=pathlib.Path((str(self.LOCUST_run__dir_input / file.parts[-1])).replace(section_to_remove,'_')) #while we are here grab the original filename without added TAIL
            subprocess.run(shlex.split('cp {file} {inputdir}'.format(file=str(file),inputdir=destination)),shell=False)

            field_builder=MARS_builder_run(filepath_input=HEAD,dir_output=self.LOCUST_run__dir_input,dir_MARS_builder=self.LOCUST_run__dir_cache / 'MARS_builder',system_name='TITAN',settings_mars_read=self.MARS_read__settings,flags=self.MARS_read__flags)
            field_builder.run()

    def get_other_input_files(self,*args,**kwargs):
        """
        fetch 2D equilibrium, tokamak wall description and cross section data
        notes:
        """

        #equilibrium=Equilibrium(ID='',data_format='GEQDSK',filename=self.RMP_study__filepath_equilibrium)
        subprocess.run(shlex.split('cp {file} {inputdir}'.format(file=str(self.RMP_study__filepath_equilibrium),inputdir=str(self.LOCUST_run__dir_input / 'LOCUST_GEQDSK'))),shell=False)
        for file in self.RMP_study__filepath_additional_data.glob('*'):
            subprocess.run(shlex.split('cp {file} {inputdir}'.format(file=str(file),inputdir=str(self.LOCUST_run__dir_input / file.parts[-1]))),shell=False)

    def dump_to_IMAS_inputs(self,*args,**kwargs):
        """
        dump current input data to IMAS

        notes:
            dumps kinetic profiles, perturbation and equilibrium 
            allows NEMO to be ran to generate beam deposition
        """

        #densities


'''
    def setup_directories(self,*args,**kwargs):
        """
        notes:
        """

    def setup_directories(self,*args,**kwargs):
        """
        notes:
        """

    def run_LOCUST(self,*args,**kwargs)
        import locust_run here

        this_run=LOCUST_run_RMP(system_name=args.system_name,repo_URL=args.repo_URL,commit_hash=args.commit_hash,dir_locust=args.dir_locust,dir_input=args.dir_input,dir_output=args.dir_output,dir_cache=args.dir_cache,settings_prec_mod=settings_prec_mod,flags=flags)
        
        #default run order is: mkdir-get_code-make-get_input-run_code-get_output-cleanup
        #add new step to retrieve cache here
        def retrieve_cache():
            something

        this_run.add_command(retrieve_cache)

        this_run.run()

'''

if __name__=='__main__':

    import argparse
    parser=argparse.ArgumentParser(description='run RMP_study from command line in Python!')
    
    parser.add_argument('--parameters__database',type=str,action='store',dest='parameters__database',help="",default=None)
    parser.add_argument('--parameters__sheet_name_kinetic_prof',type=str,action='store',dest='parameters__sheet_name_kinetic_prof',help="",default=None)
    parser.add_argument('--parameters__sheet_name_rotation',type=str,action='store',dest='parameters__sheet_name_rotation',help="",default=None)
    parser.add_argument('--parameters__var_name_rotation',type=str,action='store',dest='parameters__var_name_rotation',help="",default=None)
    parser.add_argument('--parameters__kinetic_prof_n',type=str,action='store',dest='parameters__kinetic_prof_n',help="",default=None)
    parser.add_argument('--parameters__kinetic_prof_tF_tE',type=str,action='store',dest='parameters__kinetic_prof_tF_tE',help="",default=None)
    parser.add_argument('--parameters__kinetic_prof_Pr',type=str,action='store',dest='parameters__kinetic_prof_Pr',help="",default=None)
    parser.add_argument('--parameters__toroidal_mode_number',type=str,action='store',dest='parameters__toroidal_mode_number',help="",default=None)
    parser.add_argument('--parameters__phase_upper',type=str,action='store',dest='parameters__phase_upper',help="",default=None)
    parser.add_argument('--parameters__phase_middle',type=str,action='store',dest='parameters__phase_middle',help="",default=None)
    parser.add_argument('--parameters__phase_lower',type=str,action='store',dest='parameters__phase_lower',help="",default=None)
    parser.add_argument('--parameters__rotation_upper',type=str,action='store',dest='parameters__rotation_upper',help="",default=None)
    parser.add_argument('--parameters__rotation_middle',type=str,action='store',dest='parameters__rotation_middle',help="",default=None)
    parser.add_argument('--parameters__rotation_lower',type=str,action='store',dest='parameters__rotation_lower',help="",default=None)
    parser.add_argument('--parameters__parameter_string',type=str,action='store',dest='parameters__parameter_string',help="",default=None)
    parser.add_argument('--LOCUST_run__dir_LOCUST',type=str,action='store',dest='LOCUST_run__dir_LOCUST',help="",default=support.dir_locust)
    parser.add_argument('--LOCUST_run__dir_input',type=str,action='store',dest='LOCUST_run__dir_input',help="",default=support.dir_input_files)
    parser.add_argument('--LOCUST_run__dir_output',type=str,action='store',dest='LOCUST_run__dir_output',help="",default=support.dir_output_files)
    parser.add_argument('--LOCUST_run__dir_cache',type=str,action='store',dest='LOCUST_run__dir_cache',help="",default=support.dir_cache_files)
    parser.add_argument('--LOCUST_run__system_name',type=str,action='store',dest='LOCUST_run__system_name',help="",default='TITAN')
    parser.add_argument('--LOCUST_run__repo_URL',type=str,action='store',dest='LOCUST_run__repo_URL',help="",default=settings.repo_URL_LOCUST)
    parser.add_argument('--LOCUST_run__commit_hash',type=str,action='store',dest='LOCUST_run__commit_hash',help="",default=None)
    parser.add_argument('--LOCUST_run__settings_prec_mod',nargs='+',type=str,action='store',dest='LOCUST_run__settings_prec_mod',help="",default={})
    parser.add_argument('--LOCUST_run__flags',nargs='+',type=str,action='store',dest='LOCUST_run__flags',help="",default={})
    parser.add_argument('--MARS_read__tail_U',type=str,action='store',dest='MARS_read__tail_U',help="",default=None)
    parser.add_argument('--MARS_read__tail_M',type=str,action='store',dest='MARS_read__tail_M',help="",default=None)
    parser.add_argument('--MARS_read__tail_L',type=str,action='store',dest='MARS_read__tail_L',help="",default=None)
    parser.add_argument('--MARS_read__settings',nargs='+',type=str,action='store',dest='MARS_read__settings',help="",default={})
    parser.add_argument('--MARS_read__flags',nargs='+',type=str,action='store',dest='MARS_read__flags',help="",default={})
    parser.add_argument('--RMP_study__name',type=str,action='store',dest='RMP_study__name',help="",default=None)
    parser.add_argument('--RMP_study__dir_input_database',type=str,action='store',dest='RMP_study__dir_input_database',help="",default=None)
    parser.add_argument('--RMP_study__filepath_kinetic_profiles',type=str,action='store',dest='RMP_study__filepath_kinetic_profiles',help="",default=None)
    parser.add_argument('--RMP_study__filepath_equilibrium',type=str,action='store',dest='RMP_study__filepath_equilibrium',help="",default=None)
    parser.add_argument('--RMP_study__filepath_additional_data',type=str,action='store',dest='RMP_study__filepath_additional_data',help="",default=None)
    parser.add_argument('--RMP_study__filepaths_3D_field_U',type=str,action='store',dest='RMP_study__filepaths_3D_field_U',help="",default=None)
    parser.add_argument('--RMP_study__filepaths_3D_field_M',type=str,action='store',dest='RMP_study__filepaths_3D_field_M',help="",default=None)
    parser.add_argument('--RMP_study__filepaths_3D_field_L',type=str,action='store',dest='RMP_study__filepaths_3D_field_L',help="",default=None)

    args=parser.parse_args()

    #provide some extra parsing steps to dict-like input arguments
    args.LOCUST_run__settings_prec_mod=run_scripts.utils.command_line_arg_parse_dict(args.LOCUST_run__settings_prec_mod)
    args.LOCUST_run__flags=run_scripts.utils.command_line_arg_parse_dict(args.LOCUST_run__flags)
    args.MARS_read__settings=run_scripts.utils.command_line_arg_parse_dict(args.MARS_read__settings)
    args.MARS_read__flags=run_scripts.utils.command_line_arg_parse_dict(args.MARS_read__flags)

    this_run=RMP_study_run(
    parameters__database=args.parameters__database,
    parameters__sheet_name_kinetic_prof=args.parameters__sheet_name_kinetic_prof,
    parameters__sheet_name_rotation=args.parameters__sheet_name_rotation,
    parameters__var_name_rotation=args.parameters__var_name_rotation,
    parameters__kinetic_prof_n=args.parameters__kinetic_prof_n,
    parameters__kinetic_prof_tF_tE=args.parameters__kinetic_prof_tF_tE,
    parameters__kinetic_prof_Pr=args.parameters__kinetic_prof_Pr,
    parameters__toroidal_mode_number=args.parameters__toroidal_mode_number,
    parameters__phase_upper=args.parameters__phase_upper,
    parameters__phase_middle=args.parameters__phase_middle,
    parameters__phase_lower=args.parameters__phase_lower,
    parameters__rotation_upper=args.parameters__rotation_upper,
    parameters__rotation_middle=args.parameters__rotation_middle,
    parameters__rotation_lower=args.parameters__rotation_lower,
    parameters__parameter_string=args.parameters__parameter_string,
    LOCUST_run__dir_LOCUST=args.LOCUST_run__dir_LOCUST,
    LOCUST_run__dir_input=args.LOCUST_run__dir_input,
    LOCUST_run__dir_output=args.LOCUST_run__dir_output,
    LOCUST_run__dir_cache=args.LOCUST_run__dir_cache,
    LOCUST_run__system_name=args.LOCUST_run__system_name,
    LOCUST_run__repo_URL=args.LOCUST_run__repo_URL,
    LOCUST_run__commit_hash=args.LOCUST_run__commit_hash,
    LOCUST_run__settings_prec_mod=args.LOCUST_run__settings_prec_mod,
    LOCUST_run__flags=args.LOCUST_run__flags,
    MARS_read__tail_U=args.MARS_read__tail_U,
    MARS_read__tail_M=args.MARS_read__tail_M,
    MARS_read__tail_L=args.MARS_read__tail_L,
    MARS_read__settings=args.MARS_read__settings,
    MARS_read__flags=args.MARS_read__flags,
    RMP_study__name=args.RMP_study__name,
    RMP_study__dir_input_database=args.RMP_study__dir_input_database,
    RMP_study__filepath_kinetic_profiles=args.RMP_study__filepath_kinetic_profiles,
    RMP_study__filepath_equilibrium=args.RMP_study__filepath_equilibrium,
    RMP_study__filepath_additional_data=args.RMP_study__filepath_additional_data,
    RMP_study__filepaths_3D_field_U=args.RMP_study__filepaths_3D_field_U,
    RMP_study__filepaths_3D_field_M=args.RMP_study__filepaths_3D_field_M,
    RMP_study__filepaths_3D_field_L=args.RMP_study__filepaths_3D_field_L
        )
    this_run.get_other_input_files()

#################################

##################################################################

###################################################################################################