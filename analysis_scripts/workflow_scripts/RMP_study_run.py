#RMP_study_run.py

'''
Samuel Ward
14/10/2019
----
modified LOCUST_run script for running LOCUST workflows with additional steps
---
notes: 
TODO:
    need to find way of meshgridding our parameter set (can you do this with lists?)
    need to then apply a filter over the top of this such that impossible combinations are ruled out (set to None or something)
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
    import run_scripts.MARS_builder_run
except:
    raise ImportError("ERROR: LOCUST_IO/src/run_scripts/MARS_builder_run.py could not be imported!\nreturning\n")
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
                LOCUST_run__dir_locust, #variables used by LOCUST_run (called within this workflow)
                LOCUST_run__dir_input,
                LOCUST_run__dir_output,
                LOCUST_run__dir_cache,
                LOCUST_run__system_name,
                LOCUST_run__repo_URL,
                LOCUST_run__commit_hash,
                LOCUST_run__settings_prec_mod,
                LOCUST_run__flags,
                RMP_study__name, #variables defining controlling this workflow
                RMP_study__dir_input_database,
                RMP_study__filepath_kinetic_profiles, 
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
        self.LOCUST_run__dir_locust=pathlib.Path(LOCUST_run__dir_locust) #data needed for LOCUST_run
        self.LOCUST_run__dir_input=pathlib.Path(LOCUST_run__dir_input)
        self.LOCUST_run__dir_output=pathlib.Path(LOCUST_run__dir_output)
        self.LOCUST_run__dir_cache=pathlib.Path(LOCUST_run__dir_cache)
        self.LOCUST_run__system_name=LOCUST_run__system_name
        self.LOCUST_run__repo_URL=LOCUST_run__repo_URL
        self.LOCUST_run__commit_hash=LOCUST_run__commit_hash
        self.LOCUST_run__settings_prec_mod=LOCUST_run__settings_prec_mod
        self.LOCUST_run__flags=LOCUST_run__flags
        self.RMP_study__name=RMP_study__name #data needed for additional steps
        self.RMP_study__dir_input_database=pathlib.Path(RMP_study__dir_input_database)
        self.RMP_study__filepath_kinetic_profiles=pathlib.Path(RMP_study__filepath_kinetic_profiles)
        self.RMP_study__filepaths_3D_field_U=pathlib.Path(RMP_study__filepaths_3D_field_U)
        self.RMP_study__filepaths_3D_field_M=pathlib.Path(RMP_study__filepaths_3D_field_M)
        self.RMP_study__filepaths_3D_field_L=pathlib.Path(RMP_study__filepaths_3D_field_L)

        #################################
        #derive some information

        #################################
        #add workflow stages

        #self.add_command(command_name='test',command_function=self.test,position=1) #add new workflow stages
        self.add_command(command_name='get_kinetic_profiles',command_function=self.get_kinetic_profiles,position=2) #add new workflow stages
        #self.add_command(command_name='kinetics',command_function=self.kinetic_profile_convert,position=self.run_commands.index('mkdir')) #add new workflow stages
        #self.add_command(command_name='mv_files',command_function=self.move_files,position=self.run_commands.index('get_input')) #add new workflow stages


'''    def setup_RMP_study_dirs(*args,**kwargs):
        """
        notes:
        """

        for direc in [
                        self.LOCUST_run__dir_input,
                        self.LOCUST_run__dir_output,
                        self.LOCUST_run__dir_cache,
                        self.LOCUST_run__dir_locust
                        ]:
            if not direc.is_dir(): direc.mkdir(parents=True)'''

    def get_kinetic_profiles(*args,**kwargs):
        """
        notes:
        """


        temperatures=[]
        densities=[]
        for species in ['electrons','tritium','deuterium','helium','hydrogen','tungsten','helium3']:
            temperatures.append(Temperature(ID='',data_format='EXCEL1',species=species,filename=self.RMP_study__filepath_kinetic_profiles))
            densities.append(Number_Density(ID='',data_format='EXCEL1',species=species,filename=self.RMP_study__filepath_kinetic_profiles))
        for temperature in temperatures: temperature.dump_data(data_format='LOCUST')
        for density in densities: density.dump_data(data_format='LOCUST')

        rotation=Rotation(ID='',data_format='EXCEL1')
        rotation.dump_data(data_format='LOCUST')

'''
    def setup_directories(*args,**kwargs):
        """
        notes:
        """

    def setup_directories(*args,**kwargs):
        """
        notes:
        """

    def setup_directories(*args,**kwargs):
        """
        notes:
        """

    def setup_directories(*args,**kwargs):
        """
        notes:
        """

    def setup_directories():
        """
        notes:
        """


    def run_MARS_build(self):
        """
        LOCUST_run stage for running mars_build

        notes:
        """

        #by default this will run compile and run MARS_builder on filepath_input and dump to LOCUST_IO/data/input_files (since output of this function is still a LOCUST input)
        
        mars_buidler_run=run_scripts.MARS_builder_run.MARS_builder_run(filepath_input,dir_output=support.dir_input_files,dir_MARS_builder=support.dir_run_scripts / 'mars_builder',system_name='TITAN',settings_mars_read={},flags={})
        mars_buidler_run.run() #this will do all stages of a mars_build run




    def kinetic_profile_convert(self):
        """

        notes:
        """



    def move_files(self):
        """

        notes:
        """

    def run_LOCUST
        import locust_run here

        this_run=LOCUST_run(system_name=args.system_name,repo_URL=args.repo_URL,commit_hash=args.commit_hash,dir_locust=args.dir_locust,dir_input=args.dir_input,dir_output=args.dir_output,dir_cache=args.dir_cache,settings_prec_mod=settings_prec_mod,flags=flags)
        
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
    parser.add_argument('--LOCUST_run__dir_locust',type=str,action='store',dest='LOCUST_run__dir_locust',help="",default=support.dir_locust)
    parser.add_argument('--LOCUST_run__dir_input',type=str,action='store',dest='LOCUST_run__dir_input',help="",default=support.dir_input_files)
    parser.add_argument('--LOCUST_run__dir_output',type=str,action='store',dest='LOCUST_run__dir_output',help="",default=support.dir_output_files)
    parser.add_argument('--LOCUST_run__dir_cache',type=str,action='store',dest='LOCUST_run__dir_cache',help="",default=support.dir_cache_files)
    parser.add_argument('--LOCUST_run__system_name',type=str,action='store',dest='LOCUST_run__system_name',help="",default='TITAN')
    parser.add_argument('--LOCUST_run__repo_URL',type=str,action='store',dest='LOCUST_run__repo_URL',help="",default=settings.repo_URL_LOCUST)
    parser.add_argument('--LOCUST_run__commit_hash',type=str,action='store',dest='LOCUST_run__commit_hash',help="",default=None)
    parser.add_argument('--LOCUST_run__settings_prec_mod',nargs='+',type=str,action='store',dest='LOCUST_run__settings_prec_mod',help="",default={})
    parser.add_argument('--LOCUST_run__flags',nargs='+',type=str,action='store',dest='LOCUST_run__flags',help="",default={})
    parser.add_argument('--RMP_study__name',type=str,action='store',dest='RMP_study__name',help="",default=None)
    parser.add_argument('--RMP_study__dir_input_database',type=str,action='store',dest='RMP_study__dir_input_database',help="",default=None)
    parser.add_argument('--RMP_study__filepath_kinetic_profiles',type=str,action='store',dest='RMP_study__filepath_kinetic_profiles',help="",default=None)
    parser.add_argument('--RMP_study__filepaths_3D_field_U',type=str,action='store',dest='RMP_study__filepaths_3D_field_U',help="",default=None)
    parser.add_argument('--RMP_study__filepaths_3D_field_M',type=str,action='store',dest='RMP_study__filepaths_3D_field_M',help="",default=None)
    parser.add_argument('--RMP_study__filepaths_3D_field_L',type=str,action='store',dest='RMP_study__filepaths_3D_field_L',help="",default=None)

    args=parser.parse_args()

    #provide some extra parsing steps to dict-like input arguments
    for arg in [args.LOCUST_run__settings_prec_mod,args.LOCUST_run__flags]:
        parsed_subargs=[subarg.split('=') for subarg in arg]    
        subargs={}
        for subarg in parsed_subargs:
            if len(subarg)>1:
                subargs[subarg[0]]=subarg[1]
            else:
                subargs[subarg[0]]=None

    this_run=RMP_study_run(
        parameters__database=args.parameters__database,
        parameters__sheet_name_kinetic_prof=args.parameters__sheet_name_kinetic_prof,
        parameters__sheet_name_rotation=args.parameters__sheet_name_rotation,
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
        LOCUST_run__dir_locust=args.LOCUST_run__dir_locust,
        LOCUST_run__dir_input=args.LOCUST_run__dir_input,
        LOCUST_run__dir_output=args.LOCUST_run__dir_output,
        LOCUST_run__dir_cache=args.LOCUST_run__dir_cache,
        LOCUST_run__system_name=args.LOCUST_run__system_name,
        LOCUST_run__repo_URL=args.LOCUST_run__repo_URL,
        LOCUST_run__commit_hash=args.LOCUST_run__commit_hash,
        LOCUST_run__settings_prec_mod=args.LOCUST_run__settings_prec_mod,
        LOCUST_run__flags=args.LOCUST_run__flags,
        RMP_study__name=args.RMP_study__name,
        RMP_study__dir_input_database=args.RMP_study__dir_input_database,
        RMP_study__filepath_kinetic_profiles=args.RMP_study__filepath_kinetic_profiles,
        RMP_study__filepaths_3D_field_U=args.RMP_study__filepaths_3D_field_U,
        RMP_study__filepaths_3D_field_M=args.RMP_study__filepaths_3D_field_M,
        RMP_study__filepaths_3D_field_L=args.RMP_study__filepaths_3D_field_L
        )
    this_run.run()

#################################

##################################################################

###################################################################################################