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
    LOCUST_run__settings_prec_mod['file_tet'] and LOCUST_run__settings_prec_mod['file_eqm'] must be set

todo:

    XXX fix shot/run look up tables
    XXX implement option where LOCUST code can be retrieved from local repository, then copied to LOCUST_dir - in case bitbucket goes down...

    XXX eventually need it so that in launch everything above the parameter loop is pure python, then below all the prec_mod settings are set etc based on that - so set prandl to 1 and that goes into a dispatch table that gives the prandl string etc.
    --> could even make a function to do it for you! you set obvious things pythonically and it then creates the appropriate corresponding prec_mod dictionary

    XXX copy all BPLASMA original files to look the same, then re-run my workflow and see if output is only one coil row




    XXX logic needs testing which copies complete mesh across since it keeps being copied


    XXX in launch.py need it so that multiple toroidal mode numbers are passed in with signs included - must take this into account when producing the filenames (abs)

    XXX for NEMO develop latest need function to edit xml file

    XXX maybe add some clean up scripts for removing input files
    



    XXX have it so that reading kineitc profiles from IDS does not have to read flux_pol.....then can set afterwards :| 

    
    XXX for resolution scans, dXR and dXZ need to be varied

    XXX check I'm calculating rho_tor correctly using QTP? / looking in the equilibrium IDS (plot against rho_tor in there if it already exists)

    XXX try following env + unloading additional libs such as matplotlib
    module load IMAS
    module unload imkl/2018.1.163-iimpi-2018a
    module unload intel/2018a
    module unload Tkinter/3.6.4-intel-2018a-Python-3.6.4
    module unload matplotlib/2.1.2-intel-2018a-Python-3.6.4
    #module load intel/2018a
    module unload Python/3.6.4-intel-2018a
    module unload PyYAML/3.12-intel-2018a-Python-3.6.4
    module unload Anaconda3/5.0.1
    module load Python/3.6.4-foss-2018a

---
'''


##################################################################
#Preamble

try:
    import sys
    import subprocess
    import pathlib
    import shlex
    import copy
    import numpy as np
    import ast
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
    import run_scripts.environment
except:
    raise ImportError("ERROR: LOCUST_IO/src/run_scripts/environment.py could not be imported!\nreturning\n")
    sys.exit(1)
try:
    import run_scripts.LOCUST_run
except:
    raise ImportError("ERROR: LOCUST_IO/src/run_scripts/LOCUST_run.py could not be imported!\nreturning\n")
    sys.exit(1)
try:
    import run_scripts.NEMO_run
except:
    raise ImportError("ERROR: LOCUST_IO/src/run_scripts/NEMO_run.py could not be imported!\nreturning\n")
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
    import processing.utils
except:
    raise ImportError("ERROR: LOCUST_IO/src/processing/utils.py could not be imported!\nreturning\n")
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
    from classes.input_classes.perturbation import Perturbation
except:
    raise ImportError("ERROR: LOCUST_IO/src/classes/input_classes/perturbation.py could not be imported!\nreturning\n") 
    sys.exit(1)
try:
    from classes.input_classes.beam_deposition import Beam_Deposition
except:
    raise ImportError("ERROR: LOCUST_IO/src/classes/input_classes/perturbation.py could not be imported!\nreturning\n") 
    sys.exit(1)
try:
    from classes.input_classes.wall import Wall
except:
    raise ImportError("ERROR: LOCUST_IO/src/classes/input_classes/wall.py could not be imported!\nreturning\n") 
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
                parameters__var_name_rotation,
                parameters__kinetic_prof_n, #variables defining the parameter set
                parameters__kinetic_prof_tF_tE,
                parameters__kinetic_prof_Pr,
                parameters__toroidal_mode_numbers,
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
                NEMO_run__dir_NEMO,
                NEMO_run__nmarker,
                NEMO_run__fokker_flag,
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
                RMP_study__filepaths_3D_fields_U,
                RMP_study__filepaths_3D_fields_M,
                RMP_study__filepaths_3D_fields_L,
                IDS__shot,
                IDS__run,
                IDS__username,
                IDS__imasdb,
                IDS__target_IDS_shot,
                IDS__target_IDS_run,
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
        self.parameters__toroidal_mode_numbers=parameters__toroidal_mode_numbers
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
        self.NEMO_run__dir_NEMO=pathlib.Path(NEMO_run__dir_NEMO)
        self.NEMO_run__nmarker=NEMO_run__nmarker
        self.NEMO_run__fokker_flag=NEMO_run__fokker_flag
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
        self.RMP_study__filepaths_3D_fields_U=[pathlib.Path(path) for path in RMP_study__filepaths_3D_fields_U]
        self.RMP_study__filepaths_3D_fields_M=[pathlib.Path(path) for path in RMP_study__filepaths_3D_fields_M]
        self.RMP_study__filepaths_3D_fields_L=[pathlib.Path(path) for path in RMP_study__filepaths_3D_fields_L]
        self.IDS__shot=IDS__shot
        self.IDS__run=IDS__run
        self.IDS__username=IDS__username
        self.IDS__imasdb=IDS__imasdb
        self.IDS__target_IDS_shot=IDS__target_IDS_shot
        self.IDS__target_IDS_run=IDS__target_IDS_run

        #################################
        #derive some information
        
        #dispatch tables for species stored in IDSs and prec_mod
        self.table_species_AZ={} #A,Z
        self.table_species_AZ['deuterium']=[2.,1.] #need to stay floats
        self.table_species_AZ['tritium']=[3.,1.]
        self.table_species_AZ['helium3']=[3.,2.]
        self.table_species_AZ['helium']=[4.,2.]
        self.table_species_AZ['hydrogen']=[1.,1.]
        self.table_species_AZ['beryllium']=[8.,4.]
        self.table_species_AZ['neon']=[20.2,10.]
        self.table_species_AZ['tungsten']=[183.8,74.]
        self.table_species_LOCUST={}
        self.table_species_LOCUST['deuterium']='AD'
        self.table_species_LOCUST['tritium']='AT'
        self.table_species_LOCUST['helium3']='AHe3'
        self.table_species_LOCUST['helium']='AHe4'
        self.table_species_LOCUST['hydrogen']='AH'
        self.table_species_LOCUST['beryllium']='ABe9'
        self.table_species_LOCUST['neon']='ANe20'
        self.table_species_LOCUST['tungsten']='AW184'

        self.MARS_read__HEAD=pathlib.Path((str(self.LOCUST_run__dir_input / self.RMP_study__filepaths_3D_fields_U[0].parts[-1])).replace('_cU_','_')) #get 3D field filenames

        #################################
        #add workflow stages

        self.add_command(command_name='mkdir',command_function=self.setup_RMP_study_dirs,position=1) #add new workflow stages
        self.add_command(command_name='get_kinetic',command_function=self.get_kinetic_profiles_excel,position=2)
        self.add_command(command_name='get_3D',command_function=self.get_3D_fields,position=3) 
        self.add_command(command_name='calc_3D',command_function=self.calc_3D_fields,position=4) 
        self.add_command(command_name='get_others',command_function=self.get_other_input_files,position=5)
        self.add_command(command_name='create_IDS',command_function=self.create_IDS,position=6) 
        self.add_command(command_name='run_NEMO',command_function=self.run_NEMO,position=7) 
        self.add_command(command_name='get_beam_depo',command_function=self.get_beam_deposition,position=8)
        #self.add_command(command_name='check_B_field',command_function=self.BCHECK,position=9)
        self.add_command(command_name='run_LOCUST',command_function=self.run_LOCUST,position=9)

    def setup_RMP_study_dirs(self,*args,**kwargs):
        """
        notes:
        """

        for direc in [
                        self.LOCUST_run__dir_input,
                        self.LOCUST_run__dir_output,
                        self.LOCUST_run__dir_cache
                        ]:
            if not direc.is_dir(): direc.mkdir(parents=True)

    def get_kinetic_profiles_IDS(self,*args,**kwargs):
        """

        notes:
            cannot currently use since IDSs do not contain:
                ids.core_profiles.profiles_1d[0].grid.rho_pol_norm
                ids.core_profiles.profiles_1d[0].ion[0].rotation_frequency_tor
                ids.core_profiles.profiles_1d[0].grid.psi
            adds prec_mod.f90 settings to adjust background ion fractions
            alternative to get_kinetic_profiles_excel
        """

        #all ion temperatures same so just read Deuterium
        temperature=Temperature(ID='', data_format='IDS',
                    species='deuterium',shot=IDS__target_IDS_shot,
                    run=IDS__target_IDS_run,A=2,Z=1) 
        temperature.dump_data(data_format='LOCUST',
            filename=self.LOCUST_run__dir_input / 'profile_Ti.dat'.format(temperature.properties['species']))
        temperature=Temperature(ID='',data_format='IDS',
                    species='electrons',shot=IDS__target_IDS_shot,
                    run=IDS__target_IDS_run) 
        temperature.dump_data(data_format='LOCUST',
            filename=self.LOCUST_run__dir_input / 'profile_Te.dat'.format(temperature.properties['species']))
        density_electrons=Number_Density(ID='',data_format='IDS',
                species='electrons',shot=IDS__target_IDS_shot,run=IDS__target_IDS_run)
        density_electrons.dump_data(data_format='LOCUST',
            filename=self.LOCUST_run__dir_input / 'profile_ne.dat')

        species_present=[] #record which species stored in IDS
        species_densities=[]
        for species_name,species_AZ in self.table_species_AZ.items(): #loop through all non-electronic ion species and set equal temperature
            try:
                density=Number_Density(ID='',data_format='IDS',
                        species=species_name,shot=IDS__target_IDS_shot,
                        run=IDS__target_IDS_run,A=species_AZ[0],Z=species_AZ[1])
                density.dump_data(data_format='LOCUST',filename=self.LOCUST_run__dir_input / 'density_{}'.format(density.properties['species']))
                species_present.append(species_name)
                species_densities.append(np.mean(density['n'])) #take average density then find Zeff/find Zeff at each point then mean = same thing
                rotation=Rotation(ID='',data_format='IDS',
                        species=species_name,shot=IDS__target_IDS_shot,
                        run=IDS__target_IDS_run,A=species_AZ[0],Z=species_AZ[1])
                rotation.dump_data(data_format='LOCUST',filename=self.LOCUST_run__dir_input / 'rotation_{}'.format(rotation.properties['species']))
            except:
                pass

        #add some setting prec_mod.f90
        self.LOCUST_run__settings_prec_mod['fi']='[{}]'.format(','.join([str(species_density/np.sum(species_densities))+'_gpu' for species_density in species_densities]))
        self.LOCUST_run__settings_prec_mod['Ai']='[{}]'.format(','.join([self.table_species_LOCUST[species_name] for species_name in species_present])) 
        self.LOCUST_run__settings_prec_mod['Zi']='[{}]'.format(','.join([str(self.table_species_AZ[species_name][1])+'_gpu' for species_name in species_present]))
        self.LOCUST_run__settings_prec_mod['nion']=len(species_present)

    def get_kinetic_profiles_excel(self,*args,**kwargs):
        """
        prepare kinetic profiles for LOCUST

        notes:
            extracts from excel spreadsheet provided by Yueqiang
            adds prec_mod.f90 settings to adjust background ion fractions
            alternative to get_kinetic_profiles_IDS
        """

        species_present=[] #record which species we find in excel
        species_densities=[]
        for species_name,species_AZ in self.table_species_AZ.items(): #loop through all non-electronic ion species and set equal temperature
            try: #XXX trying to read all species, some of which might not be present, so until errors are properly raised then errors may be printed - please ignore
                density=Number_Density(ID='',data_format='EXCEL1',species=species_name,filename=self.RMP_study__filepath_kinetic_profiles.relative_to(support.dir_input_files),sheet_name=self.parameters__sheet_name_kinetic_prof)
                density.dump_data(data_format='LOCUST',filename=self.LOCUST_run__dir_input / 'density_{}'.format(density.properties['species']))
                species_present.append(species_name)
                species_densities.append(np.mean(density['n'])) #take average density then find Zeff/find Zeff at each point then mean = same thing
                #species_densities.append(density['n'][0]) #XXX
            except:
                pass
        
        density_electrons=Number_Density(ID='',data_format='EXCEL1',species='electrons',filename=self.RMP_study__filepath_kinetic_profiles.relative_to(support.dir_input_files),sheet_name=self.parameters__sheet_name_kinetic_prof)
        density_electrons.dump_data(data_format='LOCUST',filename=self.LOCUST_run__dir_input / 'profile_ne.dat')

        #add species which are 'assumed' - once these are added to excel/IDS then can delete this
        density_Be=copy.deepcopy(density_electrons)
        density_Be['n']*=0.02
        density_Be.dump_data(data_format='LOCUST',filename=self.LOCUST_run__dir_input / 'density_beryllium')
        species_present.append('beryllium')
        species_densities.append(np.mean(density_Be['n'])) #take average density then find Zeff/find Zeff at each point then mean = same thing
        #species_densities.append(density_Be['n'][0]) #XXX
        density_Ne=copy.deepcopy(density_electrons)
        density_Ne['n']*=0.002
        density_Ne.dump_data(data_format='LOCUST',filename=self.LOCUST_run__dir_input / 'density_neon')
        species_present.append('neon')
        species_densities.append(np.mean(density_Ne['n'])) #take average density then find Zeff/find Zeff at each point then mean = same thing
        #species_densities.append(density_Ne['n'][0]) #XXX
        for species_name in ['electrons','ions']:
            temperature=Temperature(ID='',data_format='EXCEL1',species=species_name,filename=self.RMP_study__filepath_kinetic_profiles.relative_to(support.dir_input_files),sheet_name=self.parameters__sheet_name_kinetic_prof)
            temperature.dump_data(data_format='LOCUST',filename=self.LOCUST_run__dir_input / 'profile_T{}.dat'.format(temperature.properties['species'][0]))
        
        rotation=Rotation(ID='',data_format='EXCEL1',filename=self.RMP_study__filepath_kinetic_profiles.relative_to(support.dir_input_files),sheet_name=self.parameters__sheet_name_kinetic_prof,rotation_name=self.parameters__var_name_rotation,sheet_name_rotation=self.parameters__sheet_name_rotation)
        rotation.dump_data(data_format='LOCUST',filename=self.LOCUST_run__dir_input / 'profile_wT.dat') 

        #add some setting prec_mod.f90
        self.LOCUST_run__settings_prec_mod['fi']='[{}]'.format(','.join([str(species_density/np.sum(species_densities))+'_gpu' for species_density in species_densities]))
        self.LOCUST_run__settings_prec_mod['Ai']='[{}]'.format(','.join([self.table_species_LOCUST[species_name] for species_name in species_present])) 
        self.LOCUST_run__settings_prec_mod['Zi']='[{}]'.format(','.join([str(self.table_species_AZ[species_name][1])+'_gpu' for species_name in species_present]))
        self.LOCUST_run__settings_prec_mod['nion']=len(species_present)

        #print(self.LOCUST_run__settings_prec_mod['fi'])
        #print(np.sum([species_density/(np.sum(species_densities)) for species_density in species_densities]))
        #print(self.LOCUST_run__settings_prec_mod['Ai'])
        #print(self.LOCUST_run__settings_prec_mod['Zi'])

        #compare LOCUST-calculated Zeff with that stored in kinetic profiles        
        zeff_input=run_scripts.utils.read_kinetic_profile_data_excel_1(filepath=self.RMP_study__filepath_kinetic_profiles,
                                                    y='Zeff',x='Fp',sheet_name=self.parameters__sheet_name_kinetic_prof)
        zeff_locust=processing.utils.Zeff_calc(density=[species_density/(np.sum(species_densities)) for species_density in species_densities],charge=[self.table_species_AZ[species_name][1] for species_name in species_present])

        #print(np.sum([(species_density*self.table_species_AZ[species_name][1])/np.mean(density_electrons['n']) for species_density,species_name in zip(species_densities,species_present)]))
        #print(np.sum([(species_density*self.table_species_AZ[species_name][1])/density_electrons['n'][0] for species_density,species_name in zip(species_densities,species_present)]))
        #print(zeff_input)
        #print(zeff_locust)
        '''
        '''

    def get_3D_fields(self,*args,**kwargs):
        """
        notes:
        """

        for counter_mode,mode in enumerate(self.parameters__toroidal_mode_numbers):
            for file,TAIL,section_to_remove in zip( #move all input files to correct location and add appropriate TAIL
                            [self.RMP_study__filepaths_3D_fields_U[counter_mode],self.RMP_study__filepaths_3D_fields_M[counter_mode],self.RMP_study__filepaths_3D_fields_L[counter_mode]],
                            [self.MARS_read__tail_U,self.MARS_read__tail_M,self.MARS_read__tail_L],
                            ['_cU_','_cM_','_cL_']): 
                destination=(str(self.LOCUST_run__dir_input / file.parts[-1])+TAIL).replace(section_to_remove,'_')
                subprocess.run(shlex.split('cp {file} {inputdir}'.format(file=str(file),inputdir=destination)),shell=False)

    def calc_3D_fields(self,*args,**kwargs):
        """
        prepare 3D fields for LOCUST

        notes:
            copies 3D field files from the target folder into destination and renames file correctly before running mars_builder to combine them into single field
            suited for parameter scans involving static RMP fields
            must add file tails here and not in mars_read since no way to discern coil row otherwise
        """

        for counter_mode,mode in enumerate(self.parameters__toroidal_mode_numbers):
            for counter_coil_row in range(3): #now all files in place, run MARS_builder for each coil row
                self.MARS_read__flags['COILROW']=counter_coil_row+1
                self.MARS_read__flags['NC']=np.abs(mode)
                field_builder=MARS_builder_run(filepath_input=self.MARS_read__HEAD,dir_output=self.LOCUST_run__dir_input,
                                                dir_MARS_builder=self.LOCUST_run__dir_cache / 'MARS_builder',system_name='TITAN',
                                                settings_mars_read=self.MARS_read__settings,flags=self.MARS_read__flags)
                field_builder.run()
            '''
            for file in self.LOCUST_run__dir_input.glob(str(self.MARS_read__HEAD.parts[-1])+'*'):
                subprocess.run(shlex.split('rm {file}'.format(file=str(file))),shell=False) #delete old perturbation input files
            '''
            for file in self.LOCUST_run__dir_input.glob('mars_read*CACHE'):
                subprocess.run(shlex.split('rm {file}'.format(file=str(file))),shell=False) #delete cache files after all coilrows (different coilrows can re-use cache!) 

    def get_other_input_files(self,*args,**kwargs):
        """
        fetch/rename 2D equilibrium, tokamak wall description, cross section data and pre-cached files

        notes:
        """

        #fetch equilibrium
        subprocess.run(shlex.split('cp {file} {dir_input}'.format(file=str(self.RMP_study__filepath_equilibrium),
            dir_input=str(self.LOCUST_run__dir_input / self.LOCUST_run__settings_prec_mod['file_eqm']))),shell=False)
        #equilibrium=Equilibrium(ID='',data_format='GEQDSK',filename=self.RMP_study__filepath_equilibrium)
        
        #fetch additional required data
        for file in self.RMP_study__filepath_additional_data.glob('*'):
            if 'ITER_meshC.mesh.inp_ANSYS' in str(file) and not list(self.LOCUST_run__dir_cache.glob('MESH_*CACHE')): #if we are dealing with the mesh, first check if cache files are present in cache dir - since mesh usually large
                dir_input=self.LOCUST_run__dir_input / self.LOCUST_run__settings_prec_mod['file_tet']
                subprocess.run(shlex.split('cp {file} {dir_input}'.format(file=str(file),dir_input=str(dir_input))),shell=False)
            else:
                dir_input=self.LOCUST_run__dir_input
                subprocess.run(shlex.split('cp {file} {dir_input}'.format(file=str(file),dir_input=str(dir_input))),shell=False)

    def create_IDS(self,*args,**kwargs):
        """
        notes:
        """

        try:
            import imas 
        except:
            raise ImportError("ERROR: LOCUST_run_RMP.create_new_IDS could not import IMAS module!\nreturning\n")
            return
        new_IDS=imas.ids(self.IDS__shot,self.IDS__run) #initialise new blank IDS
        new_IDS.create_env(self.IDS__username,self.IDS__imasdb,settings.imas_version) 
        new_IDS_nbi_ctx=new_IDS.nbi.getPulseCtx() #retain file handles for later
        new_IDS_core_profiles_ctx=new_IDS.core_profiles.getPulseCtx()
        new_IDS_equilibrium_ctx=new_IDS.equilibrium.getPulseCtx()
        new_IDS_distribution_sources_ctx=new_IDS.distribution_sources.getPulseCtx()
        new_IDS_distributions_ctx=new_IDS.distributions.getPulseCtx()

        #retrieve ITER NBI geometry/settings
        IDS_nbi=imas.ids(130011,1) #take NBI geometry from sample public IDS
        IDS_nbi.open_env('public','ITER','3')

        IDS_nbi.nbi.get()
        new_IDS.nbi=copy.deepcopy(IDS_nbi.nbi) #grab the part of the IDS we want
        new_IDS.nbi.setPulseCtx(new_IDS_nbi_ctx) #reset file handle

        IDS_nbi.distributions.get()
        new_IDS.distributions=copy.deepcopy(IDS_nbi.distributions) #grab the part of the IDS we want
        new_IDS.distributions.setPulseCtx(new_IDS_distributions_ctx) #reset file handle

        #retrieve rest of data from IDS containing source data
        IDS_source=imas.ids(self.IDS__target_IDS_shot,self.IDS__target_IDS_run)
        IDS_source.open_env('public','ITER','3')
        
        IDS_source.core_profiles.get() 
        new_IDS.core_profiles=copy.deepcopy(IDS_source.core_profiles) #grab the part of the IDS we want
        new_IDS.core_profiles.setPulseCtx(new_IDS_core_profiles_ctx) #reset file handle

        IDS_source.equilibrium.get()
        new_IDS.equilibrium=copy.deepcopy(IDS_source.equilibrium) #grab the part of the IDS we want
        new_IDS.equilibrium.setPulseCtx(new_IDS_equilibrium_ctx) #reset file handle

        IDS_source.distribution_sources.get()
        new_IDS.distribution_sources=copy.deepcopy(IDS_source.distribution_sources) #grab the part of the IDS we want
        new_IDS.distribution_sources.setPulseCtx(new_IDS_distribution_sources_ctx) #reset file handle

        #calculate/fill in blank rho_tor field 
        equilibrium=Equilibrium(ID='',data_format='GEQDSK',filename=self.RMP_study__filepath_equilibrium)

        temperature_example=Temperature(ID='',data_format='EXCEL1',species='ions',filename=self.RMP_study__filepath_kinetic_profiles.relative_to(support.dir_input_files),sheet_name=self.parameters__sheet_name_kinetic_prof)
        temperature_example['flux_pol']=temperature_example['flux_pol_norm']*(equilibrium['sibry']-equilibrium['simag'])+equilibrium['simag']
        rho_tor_eq=np.sqrt(np.abs(equilibrium['flux_tor'])*2.*np.pi/(np.pi*np.abs(equilibrium['bcentr']))) #calculate rho_tor on equilibrium flux grid - rho_tor = sqrt(b_flux_tor/(pi*b0)) where I think b_flux_tor is in [Wb]
        interpolator_rho_tor=processing.utils.interpolate_1D(equilibrium['flux_pol'],rho_tor_eq,type='interp1d') #interpolate this onto flux grid of kinetic profiles - type=RBF currently breaks due to bugs in module environment 
        rho_tor_core_prof=interpolator_rho_tor(temperature_example['flux_pol']) #use grid taken from a random temperature from the source data to determine corresponding rho_tor grid
        new_IDS.core_profiles.profiles_1d[0].grid.rho_tor=rho_tor_core_prof
        new_IDS.core_profiles.profiles_1d[0].grid.rho_tor_norm=(rho_tor_core_prof-rho_tor_core_prof[0])/(rho_tor_core_prof[-1]-rho_tor_core_prof[0]) #remove rho_tor_norm as this grid seems to be different

        #set time data
        new_IDS.equilibrium.ids_properties.homogeneous_time = 1
        new_IDS.core_profiles.ids_properties.homogeneous_time = 1
        new_IDS.nbi.ids_properties.homogeneous_time = 1
        new_IDS.distribution_sources.ids_properties.homogeneous_time = 1
        new_IDS.distributions.ids_properties.homogeneous_time = 1
        new_IDS.wall.ids_properties.homogeneous_time = 1

        new_IDS.equilibrium.time = np.array([0.0])
        new_IDS.core_profiles.time = np.array([0.0])
        new_IDS.nbi.time = np.array([0.0])
        new_IDS.distribution_sources.time = np.array([0.0])
        new_IDS.distributions.time = np.array([0.0])
        new_IDS.wall.time = np.array([0.0])

        new_IDS.nbi.put()
        new_IDS.core_profiles.put()
        new_IDS.equilibrium.put()
        new_IDS.distribution_sources.put()
        new_IDS.distributions.put()
        new_IDS.wall.put()
           
        IDS_nbi.close()
        IDS_source.close()
        new_IDS.close()

        #fill in blank temperatures
        for species,species_AZ in self.table_species_AZ.items(): #loop through all non-electronic ion species and set equal temperature
            temperature=Temperature(ID='',data_format='EXCEL1',species='ions',filename=self.RMP_study__filepath_kinetic_profiles.relative_to(support.dir_input_files),sheet_name=self.parameters__sheet_name_kinetic_prof)
            temperature['flux_pol']=temperature['flux_pol_norm']*(equilibrium['sibry']-equilibrium['simag'])+equilibrium['simag']
            temperature.dump_data(data_format='IDS',shot=self.IDS__shot,run=self.IDS__run,species=species,A=species_AZ[0],Z=species_AZ[1])

        #fill in 2D limiter in wall IDS from GEQDSK
        wall_2D=Wall(ID='',data_format='GEQDSK',filename=self.RMP_study__filepath_equilibrium)
        wall_2D.dump_data(data_format='IDS',shot=self.IDS__shot,run=self.IDS__run)

    def run_NEMO(self,*args,**kwargs):
        """
        notes:
        """

        NEMO_workflow=run_scripts.NEMO_run.NEMO_run(
        dir_NEMO=self.NEMO_run__dir_NEMO,
        shot_in=self.IDS__shot,
        shot_out=self.IDS__shot,
        run_in=self.IDS__run,
        run_out=self.IDS__run,
        username=settings.username,
        imasdb=settings.imasdb,
        imas_version=settings.imas_version,
        nmarker=self.NEMO_run__nmarker,
        fokker_flag=self.NEMO_run__fokker_flag)

        NEMO_workflow.call_NEMO_actor_command_line()

    def get_beam_deposition(self,*args,**kwargs):
        """
        notes:
        """
        beam_deposition.dump_data(data_format='LOCUST_FO_weighted',filename=self.LOCUST_run__dir_input / 'ptcles.dat') 

        beam_deposition=Beam_Deposition(ID='',data_format='IDS',shot=self.IDS__shot,run=self.IDS__run)
        #beam_deposition['X']=beam_deposition['R']*np.cos(beam_deposition['phi'])
        #beam_deposition['Y']=beam_deposition['R']*np.sin(beam_deposition['phi'])
        #beam_deposition.plot(number_bins=300,real_scale=True,axes=['X','Y'])

    def BCHECK(self,*args,**kwargs):
        """
        step for checking 3D field perturbation is correct as separate coils vs combined

        notes:
        """

        for counter_mode,mode in enumerate(self.parameters__toroidal_mode_numbers):

            #rebuild field but already combined into one
            MARS_read__flags=copy.deepcopy(self.MARS_read__flags)
            MARS_read__flags['NC']=np.abs(mode)    
            if 'COILROW' in MARS_read__flags: 
                del(MARS_read__flags['COILROW'])
            field_builder=MARS_builder_run(filepath_input=self.MARS_read__HEAD,dir_output=self.LOCUST_run__dir_input,
                                            dir_MARS_builder=self.LOCUST_run__dir_cache / 'MARS_builder',system_name='TITAN',
                                            settings_mars_read=self.MARS_read__settings,flags=MARS_read__flags)
            field_builder.run()

            #look for BPLASMA file just produced and get the R, Z grid dimensions from them
            combined_field=Perturbation('',data_format='LOCUST',filename=list(self.LOCUST_run__dir_input.glob('BPLASMA_n{}'.format(np.abs(mode))))[0].relative_to(support.dir_input_files))
            combined_field.set(time_point_data=np.full(len(combined_field['R_1D']),0.),phi_point_data=np.full(len(combined_field['R_1D']),0.))
            combined_field.set(R_point_data=combined_field['R_1D'],Z_point_data=combined_field['Z_1D'])
            combined_field.dump_data(data_format='point_data',filename=self.LOCUST_run__dir_input / 'point_data.inp')
            #also evaluate field using my own routine and check against
            dbr,dbtor,dbz=combined_field.evaluate(R=combined_field['R_point_data'],
                                                                phi=combined_field['phi_point_data'],
                                                                Z=combined_field['Z_point_data'],
                                                                mode_number=mode,i3dr=-1,phase=0)
            combined_field.set(dB_field_R=dbr,dB_field_tor=dbtor,dB_field_Z=dbz)
            
            LOCUST_run__flags_combined=copy.deepcopy(self.LOCUST_run__flags) #alter LOCUST compile flags to control run mode
            del(LOCUST_run__flags_combined['NCOILS'])
            LOCUST_run__flags_combined['BCHECK']=1
            LOCUST_run__flags_separate=copy.deepcopy(self.LOCUST_run__flags)
            LOCUST_run__flags_separate['BCHECK']=1

            LOCUST_run__settings_prec_mod_combined=copy.deepcopy(self.LOCUST_run__settings_prec_mod)
            LOCUST_run__settings_prec_mod_combined['phase']='[0.0_gpu]'
            LOCUST_run__settings_prec_mod_combined['omega']='[0.0_gpu]'
            LOCUST_run__settings_prec_mod_combined['nmde']=1
            LOCUST_run__settings_prec_mod_combined['nnum']='[{}]'.format(mode)
            
            LOCUST_workflow=run_scripts.LOCUST_run.LOCUST_run(system_name=self.LOCUST_run__system_name,
                repo_URL=self.LOCUST_run__repo_URL,
                commit_hash=self.LOCUST_run__commit_hash,
                dir_LOCUST=self.LOCUST_run__dir_LOCUST,
                dir_input=self.LOCUST_run__dir_input,
                dir_output=self.LOCUST_run__dir_output,
                dir_cache=self.LOCUST_run__dir_cache,
                settings_prec_mod=LOCUST_run__settings_prec_mod_combined,
                flags=LOCUST_run__flags_combined)
            LOCUST_workflow.run()
            (self.LOCUST_run__dir_output / 'field_data.out').rename(self.LOCUST_run__dir_output / 'field_data_combined.out')

            LOCUST_run__settings_prec_mod_separate=copy.deepcopy(self.LOCUST_run__settings_prec_mod)
            LOCUST_run__settings_prec_mod_separate['phase']='[0.0_gpu,0.0_gpu,0.0_gpu]'
            LOCUST_run__settings_prec_mod_separate['omega']='[0.0_gpu,0.0_gpu,0.0_gpu]'
            LOCUST_run__settings_prec_mod_separate['nmde']=3
            LOCUST_run__settings_prec_mod_separate['nnum']='[{},{},{}]'.format(mode,mode,mode)

            LOCUST_workflow=run_scripts.LOCUST_run.LOCUST_run(system_name=self.LOCUST_run__system_name,
                repo_URL=self.LOCUST_run__repo_URL,
                commit_hash=self.LOCUST_run__commit_hash,
                dir_LOCUST=self.LOCUST_run__dir_LOCUST,
                dir_input=self.LOCUST_run__dir_input,
                dir_output=self.LOCUST_run__dir_output,
                dir_cache=self.LOCUST_run__dir_cache,
                settings_prec_mod=LOCUST_run__settings_prec_mod_separate,
                flags=LOCUST_run__flags_separate)
            LOCUST_workflow.run()
            (self.LOCUST_run__dir_output / 'field_data.out').rename(self.LOCUST_run__dir_output / 'field_data_separate.out')

            field_combined_eval=Perturbation('',data_format='LOCUST_field_data',filename=(self.LOCUST_run__dir_output / 'field_data_combined.out').relative_to(support.dir_output_files))
            field_separate_eval=Perturbation('',data_format='LOCUST_field_data',filename=(self.LOCUST_run__dir_output / 'field_data_separate.out').relative_to(support.dir_output_files))
            field_difference=copy.deepcopy(field_separate_eval)

            field_separate_eval.look()

            import matplotlib.pyplot as plt
            import matplotlib
            fig,(ax1,ax2)=plt.subplots(2,1)
            for quantity in ['dB_field_R','dB_field_tor','dB_field_Z']:
                field_difference[quantity]-=field_combined_eval[quantity]
                field_difference[quantity]/=field_combined_eval[quantity] #get fractional difference between the two fields
                ax1.plot(field_difference[quantity],'m-')
                ax2.plot(field_separate_eval[quantity],'g-')
                ax2.plot(combined_field[quantity],'b-')
                ax2.plot(field_combined_eval[quantity],'r-')
            #plt.savefig('BCHECK_{}.png'.format(mode),bbox_inches='tight')
            plt.show()

    def run_LOCUST(self,*args,**kwargs):
        """
        notes:
        """

        #need to make some custom edits to LOCUST_run workflow class - redefine this workflow stage here
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

        LOCUST_workflow=LOCUST_run_RMP(system_name=self.LOCUST_run__system_name,
            repo_URL=self.LOCUST_run__repo_URL,
            commit_hash=self.LOCUST_run__commit_hash,
            dir_LOCUST=self.LOCUST_run__dir_LOCUST,
            dir_input=self.LOCUST_run__dir_input,
            dir_output=self.LOCUST_run__dir_output,
            dir_cache=self.LOCUST_run__dir_cache,
            settings_prec_mod=self.LOCUST_run__settings_prec_mod,
            flags=self.LOCUST_run__flags)

        LOCUST_workflow.run()


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
    parser.add_argument('--parameters__toroidal_mode_numbers',type=str,action='store',dest='parameters__toroidal_mode_numbers',help="",default=None)
    parser.add_argument('--parameters__parameter_string',type=str,action='store',dest='parameters__parameter_string',help="",default=None)
    parser.add_argument('--LOCUST_run__dir_LOCUST',type=str,action='store',dest='LOCUST_run__dir_LOCUST',help="",default=support.dir_LOCUST)
    parser.add_argument('--LOCUST_run__dir_input',type=str,action='store',dest='LOCUST_run__dir_input',help="",default=support.dir_input_files)
    parser.add_argument('--LOCUST_run__dir_output',type=str,action='store',dest='LOCUST_run__dir_output',help="",default=support.dir_output_files)
    parser.add_argument('--LOCUST_run__dir_cache',type=str,action='store',dest='LOCUST_run__dir_cache',help="",default=support.dir_cache_files)
    parser.add_argument('--LOCUST_run__system_name',type=str,action='store',dest='LOCUST_run__system_name',help="",default='TITAN')
    parser.add_argument('--LOCUST_run__repo_URL',type=str,action='store',dest='LOCUST_run__repo_URL',help="",default=settings.repo_URL_LOCUST)
    parser.add_argument('--LOCUST_run__commit_hash',type=str,action='store',dest='LOCUST_run__commit_hash',help="",default=None)
    parser.add_argument('--LOCUST_run__settings_prec_mod',nargs='+',type=str,action='store',dest='LOCUST_run__settings_prec_mod',help="",default={})
    parser.add_argument('--LOCUST_run__flags',nargs='+',type=str,action='store',dest='LOCUST_run__flags',help="",default={})
    parser.add_argument('--NEMO_run__dir_NEMO',type=str,action='store',dest='NEMO_run__dir_NEMO',help="",default=support.dir_nemo)
    parser.add_argument('--NEMO_run__nmarker',type=int,action='store',dest='NEMO_run__nmarker',help="",default=int(1.e6))
    parser.add_argument('--NEMO_run__fokker_flag',type=int,action='store',dest='NEMO_run__fokker_flag',help="",default=0)
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
    parser.add_argument('--RMP_study__filepaths_3D_fields_U',type=str,action='store',dest='RMP_study__filepaths_3D_fields_U',help="",default=None)
    parser.add_argument('--RMP_study__filepaths_3D_fields_M',type=str,action='store',dest='RMP_study__filepaths_3D_fields_M',help="",default=None)
    parser.add_argument('--RMP_study__filepaths_3D_fields_L',type=str,action='store',dest='RMP_study__filepaths_3D_fields_L',help="",default=None)
    parser.add_argument('--IDS__shot',type=int,action='store',dest='IDS__shot',help="",default=1)
    parser.add_argument('--IDS__run',type=int,action='store',dest='IDS__run',help="",default=1)
    parser.add_argument('--IDS__username',type=str,action='store',dest='IDS__username',help="",default=None)
    parser.add_argument('--IDS__imasdb',type=str,action='store',dest='IDS__imasdb',help="",default=None)
    parser.add_argument('--IDS__target_IDS_shot',type=int,action='store',dest='IDS__target_IDS_shot',help="",default=1)
    parser.add_argument('--IDS__target_IDS_run',type=int,action='store',dest='IDS__target_IDS_run',help="",default=1)

    args=parser.parse_args()

    #provide some extra parsing steps to dict-like and array-like input arguments
    args.LOCUST_run__settings_prec_mod=run_scripts.utils.command_line_arg_parse_dict(args.LOCUST_run__settings_prec_mod)
    args.LOCUST_run__flags=run_scripts.utils.command_line_arg_parse_dict(args.LOCUST_run__flags)
    args.MARS_read__settings=run_scripts.utils.command_line_arg_parse_dict(args.MARS_read__settings)
    args.MARS_read__flags=run_scripts.utils.command_line_arg_parse_dict(args.MARS_read__flags)
    args.RMP_study__filepaths_3D_fields_U=run_scripts.utils.literal_eval(args.RMP_study__filepaths_3D_fields_U)
    args.RMP_study__filepaths_3D_fields_M=run_scripts.utils.literal_eval(args.RMP_study__filepaths_3D_fields_M)
    args.RMP_study__filepaths_3D_fields_L=run_scripts.utils.literal_eval(args.RMP_study__filepaths_3D_fields_L)
    args.parameters__toroidal_mode_numbers=run_scripts.utils.literal_eval(args.parameters__toroidal_mode_numbers)

    RMP_workflow=RMP_study_run(
    parameters__database=args.parameters__database,
    parameters__sheet_name_kinetic_prof=args.parameters__sheet_name_kinetic_prof,
    parameters__sheet_name_rotation=args.parameters__sheet_name_rotation,
    parameters__var_name_rotation=args.parameters__var_name_rotation,
    parameters__kinetic_prof_n=args.parameters__kinetic_prof_n,
    parameters__kinetic_prof_tF_tE=args.parameters__kinetic_prof_tF_tE,
    parameters__kinetic_prof_Pr=args.parameters__kinetic_prof_Pr,
    parameters__toroidal_mode_numbers=args.parameters__toroidal_mode_numbers,
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
    NEMO_run__dir_NEMO=args.NEMO_run__dir_NEMO,
    NEMO_run__nmarker=args.NEMO_run__nmarker,
    NEMO_run__fokker_flag=args.NEMO_run__fokker_flag,
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
    RMP_study__filepaths_3D_fields_U=args.RMP_study__filepaths_3D_fields_U,
    RMP_study__filepaths_3D_fields_M=args.RMP_study__filepaths_3D_fields_M,
    RMP_study__filepaths_3D_fields_L=args.RMP_study__filepaths_3D_fields_L,
    IDS__shot=args.IDS__shot,
    IDS__run=args.IDS__run,
    IDS__username=args.IDS__username,
    IDS__imasdb=args.IDS__imasdb,
    IDS__target_IDS_shot=args.IDS__target_IDS_shot,
    IDS__target_IDS_run=args.IDS__target_IDS_run
        )

    RMP_workflow.run()

#################################

##################################################################

###################################################################################################