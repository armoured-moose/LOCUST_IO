#template_run.py

'''
Samuel Ward
14/10/2019
----
workflow designed for RMP studies
---
notes: 
    file is designed to not assume anything about the study being performed, so is almost entirely controlled by the launch file
    all filepaths are absolute at the beginning
    LOCUST_run__settings_prec_mod['file_tet'] and LOCUST_run__settings_prec_mod['file_eqm'] must be set
    ! setting interpolation type=RBF currently breaks due to bugs in module environment
todo:

    create helper functions e.g. for reading kinetic profiles, strategy behaviour decided by template_launch i.e. whether to read from excel or IDS 

    XXX logic needs testing which copies complete mesh across since it keeps being copied
    
    XXX have it so that reading kinetic profiles from IDS does not have to read flux_pol.....then can set afterwards :| 

    XXX check I'm calculating rho_tor correctly using QTP? / looking in the equilibrium IDS (plot against rho_tor in there if it already exists)
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
    import run_scripts.BBNBI_run
except:
    raise ImportError("ERROR: LOCUST_IO/src/run_scripts/BBNBI_run.py could not be imported!\nreturning\n")
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
    from classes.output_classes.particle_list import Final_Particle_List
except:
    raise ImportError("ERROR: LOCUST_IO/src/classes/input_classes/particle_list.py could not be imported!\nreturning\n") 
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

try:
    from template_mod import *
except:
    raise ImportError("ERROR: template_mod.py could not be imported!\nreturning\n") 
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
                *args,
                **kwargs):
        """
        notes:
        """


        super().__init__()


        #################################
        #read args needed for workflow steps

        self.args={**kwargs}

        #do some processing
        
        self.args['LOCUST_run__dir_LOCUST']=pathlib.Path(self.args['LOCUST_run__dir_LOCUST']) 
        self.args['LOCUST_run__dir_LOCUST_source']=pathlib.Path(self.args['LOCUST_run__dir_LOCUST_source'])
        self.args['LOCUST_run__dir_input']=pathlib.Path(self.args['LOCUST_run__dir_input'])
        self.args['LOCUST_run__dir_output']=pathlib.Path(self.args['LOCUST_run__dir_output'])
        self.args['LOCUST_run__dir_cache']=pathlib.Path(self.args['LOCUST_run__dir_cache'])
        self.args['NEMO_run__dir_NEMO']=pathlib.Path(self.args['NEMO_run__dir_NEMO'])
        self.args['BBNBI_run__dir_BBNBI']=pathlib.Path(self.args['BBNBI_run__dir_BBNBI'])
        self.args['MARS_read__dir_MARS_builder']=pathlib.Path(self.args['MARS_read__dir_MARS_builder'])
        self.args['RMP_study__filepath_kinetic_profiles']=pathlib.Path(self.args['RMP_study__filepath_kinetic_profiles'])
        self.args['RMP_study__filepath_equilibrium']=pathlib.Path(self.args['RMP_study__filepath_equilibrium'])
        self.args['RMP_study__filepath_additional_data']=pathlib.Path(self.args['RMP_study__filepath_additional_data'])
        self.args['RMP_study__filepaths_3D_fields_U']=[pathlib.Path(path) for path in self.args['RMP_study__filepaths_3D_fields_U']]
        self.args['RMP_study__filepaths_3D_fields_M']=[pathlib.Path(path) for path in self.args['RMP_study__filepaths_3D_fields_M']]
        self.args['RMP_study__filepaths_3D_fields_L']=[pathlib.Path(path) for path in self.args['RMP_study__filepaths_3D_fields_L']]

        #################################
        #derive some information

        #get 3D field filename heads for mars_read
        self.args['MARS_read__HEAD']=[self.args['LOCUST_run__dir_input'] / str(filepath_3D_field.parts[-1]).replace('_cU_','_') for filepath_3D_field in self.args['RMP_study__filepaths_3D_fields_U']] 

        #################################
        #add workflow stages

        self.commands_available={}
        self.commands_available['pass']=self.pass_command
        self.commands_available['mkdir']=self.setup_RMP_study_dirs
        self.commands_available['save_args']=self.write_batch_args
        self.commands_available['kin_get']=self.get_kinetic_profiles_excel
        self.commands_available['3D_get']=self.get_3D_fields
        self.commands_available['3D_calc']=self.calc_3D_fields
        self.commands_available['input_get']=self.get_other_input_files
        self.commands_available['IDS_create_DNB']=self.create_IDS_DNB
        self.commands_available['IDS_create']=self.create_IDS
        self.commands_available['kin_extrap']=self.extrapolate_kinetic_profiles
        self.commands_available['kin_plot']=self.plot_kinetic_profiles
        self.commands_available['run_NEMO']=self.run_NEMO
        self.commands_available['run_BBNBI']=self.run_BBNBI
        self.commands_available['depo_get']=self.get_beam_deposition_IDS
        self.commands_available['depo_get_premade']=self.get_beam_deposition_file
        self.commands_available['depo_plot']=self.plot_beam_deposition
        self.commands_available['B_check_2D']=self.plot_equilibrium
        self.commands_available['B_check_3D']=self.BCHECK_3D
        self.commands_available['calc_divB']=self.calc_divergence
        self.commands_available['plot_inputs']=self.plot_inputs
        self.commands_available['calc_poinc']=self.create_Poincare
        self.commands_available['run_LOCUST']=self.run_LOCUST
        self.commands_available['calc_orb']=self.calculate_orbits
        self.commands_available['clean_input']=self.clean_input
        self.commands_available['clean_cache']=self.clean_cache

        #check output directory contains no distribution functions already in which case skip (unless just wanting tests e.g. Poincaré map, trajectories or BCHECKing)
        
        if not all([list(self.args['LOCUST_run__dir_output'].glob(output_glob)) for output_glob in ['*.dfn','ORBIT*','Poincare_map*.dat']]): 
            if not any([list(self.args['LOCUST_run__dir_output'].glob(output_glob)) for output_glob in ['*.dfn','ORBIT*','Poincare_map*.dat']]):      
                if list(self.args['LOCUST_run__dir_output'].glob('*')): #if some outputs at all already then clear before performing run
                    try:
                        subprocess.run(shlex.split('rm -r {dir}'.format(dir=str(self.args['LOCUST_run__dir_output']))),shell=False) 
                    except:
                        print(f"ERROR: {self.workflow_name} could not clear contents of output directory {str(self.args['LOCUST_run__dir_output'])}!\nreturning\n")
                        return
                        
            for command in self.args['RMP_study__workflow_commands']:
                self.add_command(command_name=command,command_function=self.commands_available[command]) #add all workflow stages
            
        else: #if distribution functions in output directory then skip this simulation
            self.add_command(command_name='pass',command_function=self.commands_available['pass'])
            print(f"WARNING: {self.workflow_name} found files already in output folder at {self.args['LOCUST_run__dir_output']}!\npassing\n")
        
    ################################################################## helper functions

    def _plot_perturbations(self,*args,**kwargs):
        """
        helper to wrap plot_scripts.plot_perturbations
        """

        import plot_scripts.plot_perturbations
        perturbations=[]
        for counter_mode,mode in enumerate(self.args['parameters__toroidal_mode_numbers']):
            filename=list(self.args['LOCUST_run__dir_input'].glob(f'BPLASMA_n{np.abs(mode)}'))[0].relative_to(support.dir_input_files)
            perturbations.append(Perturbation(ID='',data_format='LOCUST',filename=filename,mode_number=mode))
        plot_scripts.plot_perturbations.plot_perturbations(perturbations,*args,**kwargs)

    def _plot_beam_deposition(self,*args,**kwargs):
        """
        """

        #get full beam deposition object
        beam_deposition_full=Beam_Deposition(ID='',data_format='LOCUST_FO_weighted',filename=self.args['LOCUST_run__dir_input'] / 'ptcles.dat') 
        beam_deposition_full.plot(*args,**kwargs)

        try:
            import imas 
        except:
            raise ImportError("ERROR: read_beam_depo_IDS could not import IMAS module!\nreturning\n")
            return

        '''
        beam_deposition_beamlets=[]
        #read in deposition one beamlet at a time - code taken from Beam_Deposition.read_beam_depo_IDS
        new_IDS=imas.ids(self.args['IDS__shot'],self.args['IDS__run']) #read from our newly created IDS
        new_IDS.open_env(self.args['IDS__username'],self.args['IDS__imasdb'],settings.imas_version)
        new_IDS.distribution_sources.get() #open the file and get all the data from it
        for source in new_IDS.distribution_sources.source: 
            deposition = {} #initialise blank dictionary to hold the data
            deposition['weight']=[]
            for identifier in new_IDS.distribution_sources.source[0].markers[0].coordinate_identifier: #generate keys for deposition by looking at the coordinates of the particle markers
                deposition[identifier.name.replace('\x00','').strip()]=[] #need to remove the unicode bits
            if len(source.markers)>0:
                if len(source.markers[0].positions)>0:
                    for coordinate_index in range(len(source.markers[0].positions[0,:])): #loop over the possible coordinate types e.g. r, phi, z
                        coordinate_name=source.markers[0].coordinate_identifier[coordinate_index].name.replace('\x00','').strip()
                        for marker in source.markers[0].positions[:,coordinate_index]: #this range should/must be the same for all values of coordinate_index
                            deposition[coordinate_name].extend([marker])    
                if len(source.markers[0].weights)>0: #if markers have defined weights
                    deposition['weight'].extend(source.markers[0].weights)
            
            for key in deposition: #convert to numpy arrays
                deposition[key]=np.asarray(deposition[key])

            #check for common field names to convert to LOCUST_IO variable names
            locust_io_names=['E','rho','V_phi','V_pitch'] #LOCUST_IO fields that we want to retain
            nemo_names=['Energy','Rhotor','V_PHI','Pitch angle'] #first check possible matching NEMO field names
            for nemo_name,locust_io_name in zip(nemo_names,locust_io_names):
                if nemo_name in deposition.keys():
                    deposition[locust_io_name]=deposition.pop(nemo_name)
         
            beamlet=Beam_Deposition(ID='') #spawn new blank Beam_Deposition and assign data above
            beamlet.data=copy.deepcopy(deposition)
            beam_deposition_beamlets.append(beamlet)
        
        new_IDS.close()

        '''
        #plot what we have
        '''
        import matplotlib.pyplot as plt
        fig,(ax1,ax2)=plt.subplots(2,1)
        for beamlet in beam_deposition_beamlets:
            beamlet.plot(ax=ax1,fig=fig,axes=axes,style='scatter',real_scale=True,quivers=True)
        plt.show() 
        '''
    def _plot_kinetic_profiles(self,*args,**kwargs):

        import matplotlib.pyplot as plt
        ax=kwargs.get('ax',None)
        fig=kwargs.get('fig',None)
        if fig: 
            del(kwargs['fig'])
        else:
            fig=plt.figure()
        if ax: 
            del(kwargs['ax'])
        else:
            ax=fig.add_subplot(111)

        densities=[]
        temperatures=[]
        rotations=[]
        for species_name,species_AZ in table_species_AZ.items(): #loop through all non-electronic ion species and grab number density
            try:
                for filename in list((support.dir_input_files / self.args['LOCUST_run__dir_input']).glob(f'density_{species_name}*')):
                    densities.append(Number_Density(ID=filename.parts[-1],data_format='LOCUST',species=species_name,filename=filename.relative_to(support.dir_input_files)))
            except:
                print(f'WARNING: template_run.plot_kinetic_profiles() could not find density profile for {species_name}')
        for filename in list((support.dir_input_files / self.args['LOCUST_run__dir_input']).glob('profile_ne*')):
            densities.append(Number_Density(ID=filename.parts[-1],data_format='LOCUST',species='electrons',filename=filename.relative_to(support.dir_input_files)))
        for filename in list((support.dir_input_files / self.args['LOCUST_run__dir_input']).glob('profile_Te*')):
            temperatures.append(Temperature(ID=filename.parts[-1],data_format='LOCUST',species='electrons',filename=filename.relative_to(support.dir_input_files)))
        for filename in list((support.dir_input_files / self.args['LOCUST_run__dir_input']).glob('profile_Ti*')):
            temperatures.append(Temperature(ID=filename.parts[-1],data_format='LOCUST',species='ions',filename=filename.relative_to(support.dir_input_files)))
        for filename in list((support.dir_input_files / self.args['LOCUST_run__dir_input']).glob('profile_wT*')):
            rotations.append(Rotation(ID=filename,data_format='LOCUST',species='ions',filename=self.args['LOCUST_run__dir_input'] / filename))

        axes=[ax]
        position_y_ax=0
        for colour,kinetic_profile_group,plotting_variable in zip([settings.cmap_g,settings.cmap_r,settings.cmap_b],[densities,temperatures,rotations],['density','temperature','rotation']):
            axes.append(axes[0].twinx())
            axes[-1].tick_params(axis='y', labelcolor=colour(0.5))
            axes[-1].set_ylabel(plotting_variable,color=colour(0.5)) 
            axes[-1].spines['right'].set_position(('outward', position_y_ax))
            position_y_ax+=60      
            for kinetic_profile in kinetic_profile_group: #XXX should vary symbol here
                kinetic_profile.plot(label=kinetic_profile.ID,colmap=colour,ax=axes[-1],fig=fig,*args,**kwargs)
            axes[-1].set_title('')
            axes[-1].legend()
        del(axes[0])

        #line_label=[ax.get_legend_handles_labels() for ax in axes]
        #axes[-1].legend([line[0] for line in line_label],[label[1] for label in line_label], loc=0)
    
    ################################################################## possible commands

    def pass_command(self,*args,**kwargs):
        """
        notes:
        """
        pass

    def write_batch_args(self,*args,**kwargs):
        """
        notes:
        """

        import time

        arg_string=run_scripts.utils.command_line_arg_parse_generate_string(command_number_=0,**{key:[value] for key,value in self.args.items()})
        with open(self.args['LOCUST_run__dir_output']/f"run_args{time.strftime('%d-%m-%Y_%S-%M-%H')}.txt",'w') as file:
            file.write(arg_string)

    def setup_RMP_study_dirs(self,*args,**kwargs):
        """
        notes:
        """

        for direc in [
                        self.args['LOCUST_run__dir_input'],
                        self.args['LOCUST_run__dir_output'],
                        self.args['LOCUST_run__dir_cache']
                        ]:
            if not direc.is_dir(): direc.mkdir(parents=True)

    def get_kinetic_profiles_IDS(self,*args,**kwargs):
        """

        notes:
            cannot currently use since IDSs do not contain:
                ids.core_profiles.profiles_1d[0].grid.rho_tor
                ids.core_profiles.profiles_1d[0].grid.rho_tor_norm
                ids.core_profiles.profiles_1d[0].ion[0].rotation_frequency_tor
                ids.core_profiles.profiles_1d[0].grid.psi
            adds prec_mod.f90 settings to adjust background ion fractions
            alternative to get_kinetic_profiles_excel
        """

        #all ion temperatures same so just read Deuterium
        temperature=Temperature(ID='', data_format='IDS',
                    species='deuterium',shot=self.args['IDS__target_IDS_shot'],
                    run=self.args['IDS__target_IDS_run'],A=2,Z=1) 
        temperature.dump_data(data_format='LOCUST',
            filename=self.args['LOCUST_run__dir_input'] / 'profile_Ti.dat'.format(temperature.properties['species']))
        temperature=Temperature(ID='',data_format='IDS',
                    species='electrons',shot=self.args['IDS__target_IDS_shot'],
                    run=IDS__target_IDS_run) 
        temperature.dump_data(data_format='LOCUST',
            filename=self.args['LOCUST_run__dir_input'] / 'profile_Te.dat'.format(temperature.properties['species']))
        density_electrons=Number_Density(ID='',data_format='IDS',
                species='electrons',shot=self.args['IDS__target_IDS_shot'],run=self.args['IDS__target_IDS_run'])
        density_electrons.dump_data(data_format='LOCUST',
            filename=self.args['LOCUST_run__dir_input'] / 'profile_ne.dat')

        species_present=[] #record which species stored in IDS
        species_densities=[]
        for species_name,species_AZ in table_species_AZ.items(): #loop through all non-electronic ion species and set number density
            try:
                density=Number_Density(ID='',data_format='IDS',
                        species=species_name,shot=IDS__target_IDS_shot,
                        run=IDS__target_IDS_run,A=species_AZ[0],Z=species_AZ[1])
                density.dump_data(data_format='LOCUST',filename=self.args['LOCUST_run__dir_input'] / 'density_{}'.format(density.properties['species']))
                species_present.append(species_name)
                species_densities.append(np.mean(density['n'])) #take average density then find Zeff/find Zeff at each point then mean = same thing
                rotation=Rotation(ID='',data_format='IDS',
                        species=species_name,shot=IDS__target_IDS_shot,
                        run=IDS__target_IDS_run,A=species_AZ[0],Z=species_AZ[1])
                rotation.dump_data(data_format='LOCUST',filename=self.args['LOCUST_run__dir_input'] / 'rotation_{}'.format(rotation.properties['species']))
            except:
                pass

        if {species for species in species_present}=={'deuterium','tritium'}: #if running pure DT set DT densities to half electron density 
            species_densities=[density_electrons['n'][0]/2.]*2
            density=copy.deepcopy(density_electrons)
            density['n']*=.5 #assumed 50% electron density
            for species in species_present: 
                density.dump_data(data_format='LOCUST',filename=self.args['LOCUST_run__dir_input'] / f'density_{species}')

        #add some setting prec_mod.f90
        self.args['LOCUST_run__settings_prec_mod']['fi']='[{}]'.format(','.join([str(species_density/np.sum(species_densities))+'_gpu' for species_density in species_densities]))
        self.args['LOCUST_run__settings_prec_mod']['Ai']='[{}]'.format(','.join([table_species_LOCUST[species_name] for species_name in species_present])) 
        self.args['LOCUST_run__settings_prec_mod']['Zi']='[{}]'.format(','.join([str(table_species_AZ[species_name][1])+'_gpu' for species_name in species_present]))
        self.args['LOCUST_run__settings_prec_mod']['nion']=len(species_present)

    def get_kinetic_profiles_excel(self,*args,**kwargs):
        """
        prepare kinetic profiles for LOCUST

        notes:
            extracts from excel spreadsheet provided by Yueqiang
            adds prec_mod.f90 settings to adjust background ion fractions
            alternative to get_kinetic_profiles_IDS
        """

        #start with electron density
        density_electrons=Number_Density(ID='',data_format='EXCEL1',species='electrons',filename=self.args['RMP_study__filepath_kinetic_profiles'].relative_to(support.dir_input_files),sheet_name=self.args['parameters__sheet_name_kinetic_prof'])
        density_electrons.dump_data(data_format='LOCUST',filename=self.args['LOCUST_run__dir_input'] / 'profile_ne.dat')

        #now grab ion densities
        species_present=[] #record which ion species we find in excel
        species_densities=[]
        for species_name,species_AZ in table_species_AZ.items(): #loop through all non-electronic ion species and set number density

            if species_name is 'beryllium':
                density=copy.deepcopy(density_electrons)
                density['n']*=fraction_beryllium #assumed 2% electron density
                density.properties['species']=species_name #re-label species type

            elif species_name is 'neon':
                density=copy.deepcopy(density_electrons)
                density['n']*=fraction_neon #assumed .2% electron density
                density.properties['species']=species_name #re-label species type

            elif {species for species in table_species_AZ}=={'deuterium','tritium'}: #if running pure DT set DT densities to half electron density 
                density=copy.deepcopy(density_electrons)
                density['n']*=.5 #assumed 50% electron density
                density.properties['species']=species_name #re-label species type

            else:
                try: #just try to read all species, some (e.g. Ne and Be) of which might not be present, so until errors are properly raised then errors may be printed - please ignore
                    density=Number_Density(ID='',data_format='EXCEL1',species=species_name,filename=self.args['RMP_study__filepath_kinetic_profiles'].relative_to(support.dir_input_files),sheet_name=self.args['parameters__sheet_name_kinetic_prof'])
                except:
                    density=None

            if density is not None:
                density.dump_data(data_format='LOCUST',filename=self.args['LOCUST_run__dir_input'] / 'density_{}'.format(density.properties['species']))
                species_present.append(species_name)
                #species_densities.append(np.mean(density['n'])) #take average density then find Zeff/find Zeff at each point then mean = same thing
                species_densities.append(density['n'][0]) #XXX take core value of impurity to set LOCUST density

        for species_name in ['electrons','ions']:
            temperature=Temperature(ID='',data_format='EXCEL1',species=species_name,filename=self.args['RMP_study__filepath_kinetic_profiles'].relative_to(support.dir_input_files),sheet_name=self.args['parameters__sheet_name_kinetic_prof'])
            temperature.dump_data(data_format='LOCUST',filename=self.args['LOCUST_run__dir_input'] / 'profile_T{}.dat'.format(temperature.properties['species'][0]))
        
        rotation=Rotation(ID='',data_format='EXCEL1',filename=self.args['RMP_study__filepath_kinetic_profiles'].relative_to(support.dir_input_files),sheet_name=self.args['parameters__sheet_name_kinetic_prof'],rotation_name=self.args['parameters__var_name_rotation'],sheet_name_rotation=self.args['parameters__sheet_name_rotation'])
        rotation.dump_data(data_format='LOCUST',filename=self.args['LOCUST_run__dir_input'] / 'profile_wT.dat') 

        #add some setting prec_mod.f90
        self.args['LOCUST_run__settings_prec_mod']['fi']='[{}]'.format(','.join([str(species_density/np.sum(species_densities))+'_gpu' for species_density in species_densities]))
        self.args['LOCUST_run__settings_prec_mod']['Ai']='[{}]'.format(','.join([table_species_LOCUST[species_name] for species_name in species_present])) 
        self.args['LOCUST_run__settings_prec_mod']['Zi']='[{}]'.format(','.join([str(table_species_AZ[species_name][1])+'_gpu' for species_name in species_present]))
        self.args['LOCUST_run__settings_prec_mod']['nion']=len(species_present)

        #print(self.args['LOCUST_run__settings_prec_mod['fi'])
        #print(np.sum([species_density/(np.sum(species_densities)) for species_density in species_densities]))
        #print(self.args['LOCUST_run__settings_prec_mod['Ai'])
        #print(self.args['LOCUST_run__settings_prec_mod['Zi'])

        #compare LOCUST-calculated Zeff with that stored in kinetic profiles        
        zeff_input=run_scripts.utils.read_kinetic_profile_data_excel_1(filepath=self.args['RMP_study__filepath_kinetic_profiles'],
                                                    y='Zeff',x='Fp',sheet_name=self.args['parameters__sheet_name_kinetic_prof'])
        zeff_locust=processing.utils.Zeff_calc(density=[species_density/(np.sum(species_densities)) for species_density in species_densities],
                                            charge=[table_species_AZ[species_name][1] for species_name in species_present])

        #print(np.sum([(species_density*self.args['table_species_AZ[species_name][1])/np.mean(density_electrons['n']) for species_density,species_name in zip(species_densities,species_present)]))
        #print(np.sum([(species_density*self.args['table_species_AZ[species_name][1])/density_electrons['n'][0] for species_density,species_name in zip(species_densities,species_present)]))
        #print(zeff_input)
        #print(zeff_locust)
        '''
        '''

    def get_3D_fields(self,*args,**kwargs):
        """
        notes:
        """

        for counter_mode,mode in enumerate(self.args['parameters__toroidal_mode_numbers']):
            for file,TAIL,section_to_remove in zip( #move all input files to correct location and add appropriate TAIL
                            [self.args['RMP_study__filepaths_3D_fields_U'][counter_mode],self.args['RMP_study__filepaths_3D_fields_M'][counter_mode],self.args['RMP_study__filepaths_3D_fields_L'][counter_mode]],
                            [self.args['MARS_read__tail_U'],self.args['MARS_read__tail_M'],self.args['MARS_read__tail_L']],
                            ['_cU_','_cM_','_cL_']): 
                destination=(str(self.args['LOCUST_run__dir_input'] / file.parts[-1])+TAIL).replace(section_to_remove,'_')
                subprocess.run(shlex.split('cp {file} {inputdir}'.format(file=str(file),inputdir=destination)),shell=False)

    def calc_3D_fields(self,*args,**kwargs):
        """
        prepare 3D fields for LOCUST

        notes:
            copies 3D field files from the target folder into destination and renames file correctly before running mars_builder to combine them into single field
            suited for parameter scans involving static RMP fields
            must add file tails here and not in mars_read since no way to discern coil row otherwise
        """

        NCOILS=self.args['LOCUST_run__flags']['NCOILS'] if 'NCOILS' in self.args['LOCUST_run__flags'] else 1 #if we are running for multiple coilsets then run mars_read separately this many times per toroidal harmonic
        for counter_mode,mode in enumerate(self.args['parameters__toroidal_mode_numbers']):
            for counter_coil_row in range(NCOILS): #now all files in place, run MARS_builder for each coil row
                if NCOILS>1: self.args['MARS_read__flags']['COILROW']=counter_coil_row+1
                self.args['MARS_read__flags']['NC']=np.abs(mode)
                field_builder=MARS_builder_run(filepath_input=self.args['MARS_read__HEAD'][counter_mode],dir_output=self.args['LOCUST_run__dir_input'],
                                                dir_MARS_builder=self.args['MARS_read__dir_MARS_builder'],environment_name=self.args['LOCUST_run__environment_name'],
                                                settings_mars_read=self.args['MARS_read__settings'],flags=self.args['MARS_read__flags'])
                field_builder.run()

            #for file in self.args['LOCUST_run__dir_input'].glob(str(self.args['MARS_read__HEAD'][counter_mode].parts[-1])+'*'): #delete old perturbation input files
            #    subprocess.run(shlex.split('rm {file}'.format(file=str(file))),shell=False) 
            for file in self.args['LOCUST_run__dir_input'].glob('mars_read*CACHE'):
                subprocess.run(shlex.split('rm {file}'.format(file=str(file))),shell=False) #delete cache files after all coil_rows (different coil_rows can re-use cache!) 

    def get_other_input_files(self,*args,**kwargs):
        """
        fetch/rename 2D equilibrium, tokamak wall description, cross section data and pre-cached files

        notes:
        """

        #fetch equilibrium
        subprocess.run(shlex.split('cp {file} {dir_input}'.format(file=str(self.args['RMP_study__filepath_equilibrium']),
            dir_input=str(self.args['LOCUST_run__dir_input'] / self.args['LOCUST_run__settings_prec_mod']['file_eqm']))),shell=False)
        #equilibrium=Equilibrium(ID='',data_format='GEQDSK',filename=self.args['RMP_study__filepath_equilibrium'],GEQDSKFIX1=True,GEQDSKFIX2=True)
        
        #fetch additional required data
        for file in self.args['RMP_study__filepath_additional_data'].glob('*'):
            if 'ITER_meshC.mesh.inp_ANSYS' in str(file) and not list(self.args['LOCUST_run__dir_cache'].glob('MESH_*CACHE')): #if we are dealing with the mesh, first check if cache files are present in cache dir - since mesh usually large
                if 'PFC_MOD' in self.args['LOCUST_run__flags'] and 'NOPFC' not in self.args['LOCUST_run__flags'] and 'PFC2D' not in self.args['LOCUST_run__flags']:
                    dir_input=self.args['LOCUST_run__dir_input'] / self.args['LOCUST_run__settings_prec_mod']['file_tet']
                    subprocess.run(shlex.split('cp {file} {dir_input}'.format(file=str(file),dir_input=str(dir_input))),shell=False)
            else:
                dir_input=self.args['LOCUST_run__dir_input']
                subprocess.run(shlex.split('cp {file} {dir_input}'.format(file=str(file),dir_input=str(dir_input))),shell=False)

    def create_IDS_DNB(self,*args,**kwargs):
        """
        create NBI IDS to be copied into IDS created in create_IDS

        notes:
        """
    
        run_scripts.utils.create_IDS_NBI(
        shot=self.args['IDS__NBI_shot'],
        run=self.args['IDS__NBI_run'],
        username=self.args['IDS__NBI_username'],
        imasdb=self.args['IDS__NBI_imasdb'],
        imas_version='3',
        machine='ITER',
        beam_name='diagnostic',
        )

    def create_IDS(self,*args,**kwargs):
        """
        notes:
        """

        try:
            import imas 
        except:
            raise ImportError("ERROR: LOCUST_run_RMP.create_new_IDS could not import IMAS module!\nreturning\n")
            return

        #open equilibrium that we will need for later
        equilibrium=Equilibrium(
            ID='',
            data_format='IDS',
            shot=self.args['IDS__target_IDS_shot'],
            run=self.args['IDS__target_IDS_run'],
            username='public',
            imasdb='ITER',
            imas_version='3'
            ) #use equilibrium stored in IDS here to be consistent - including calculating flux_pol from psirz

        new_IDS=imas.ids(self.args['IDS__shot'],self.args['IDS__run']) #initialise new blank IDS
        new_IDS.create_env(self.args['IDS__username'],self.args['IDS__imasdb'],settings.imas_version) 
        new_IDS_nbi_ctx=new_IDS.nbi.getPulseCtx() #retain file handles for later
        new_IDS_core_profiles_ctx=new_IDS.core_profiles.getPulseCtx()
        new_IDS_equilibrium_ctx=new_IDS.equilibrium.getPulseCtx()
        new_IDS_distribution_sources_ctx=new_IDS.distribution_sources.getPulseCtx()
        new_IDS_distributions_ctx=new_IDS.distributions.getPulseCtx()
        new_IDS_wall_ctx=new_IDS.wall.getPulseCtx()

        #retrieve ITER NBI geometry/settings
        IDS_nbi=imas.ids(self.args['IDS__NBI_shot'],self.args['IDS__NBI_run']) #take NBI geometry from sample public IDS
        IDS_nbi.open_env(self.args['IDS__NBI_username'],self.args['IDS__NBI_imasdb'],'3')

        IDS_nbi.nbi.get()
        new_IDS.nbi=copy.deepcopy(IDS_nbi.nbi) #grab the part of the IDS we want
        new_IDS.nbi.setPulseCtx(new_IDS_nbi_ctx) #reset file handle

        IDS_nbi.wall.get()
        new_IDS.wall=copy.deepcopy(IDS_nbi.wall) #grab the part of the IDS we want
        new_IDS.wall.setPulseCtx(new_IDS_wall_ctx) #reset file handle

        IDS_nbi.distributions.get()
        new_IDS.distributions=copy.deepcopy(IDS_nbi.distributions) #grab the part of the IDS we want
        new_IDS.distributions.setPulseCtx(new_IDS_distributions_ctx) #reset file handle

        #retrieve rest of data from IDS containing source data
        IDS_source=imas.ids(self.args['IDS__target_IDS_shot'],self.args['IDS__target_IDS_run'])
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
        #does not matter whether equilibrium comes from IDS or GEQDSK - as long as the equilibrium is consistent with iteslf and we consistently use that equilibrium... 
        #... since the different equilibria's psi grids might be shifted with respect to each other but that does not matter since rho_tor_eq will always be same (only gradient of psi matters in toroidal flux calc)  
        rho_tor_eq=np.sqrt(np.abs(equilibrium['flux_tor'])*2.*np.pi/(np.pi*np.abs(equilibrium['bcentr']))) #calculate rho_tor on equilibrium flux grid - rho_tor = sqrt(b_flux_tor/(pi*b0)) where I think b_flux_tor is in Wb==[mag field][length]**2
        interpolator_rho_tor=processing.utils.interpolate_1D(equilibrium['flux_pol'],rho_tor_eq,type='interp1d') #interpolate this onto flux grid of kinetic profiles 
        temperature_example=Temperature(ID='',data_format='EXCEL1',species='ions',filename=self.args['RMP_study__filepath_kinetic_profiles'].relative_to(support.dir_input_files),sheet_name=self.args['parameters__sheet_name_kinetic_prof'])
        temperature_example['flux_pol']=temperature_example['flux_pol_norm']*(equilibrium['sibry']-equilibrium['simag'])+equilibrium['simag']
        rho_tor_core_prof=interpolator_rho_tor(temperature_example['flux_pol']) #use grid taken from a random temperature from the source data to determine corresponding rho_tor grid
        new_IDS.core_profiles.profiles_1d[0].grid.rho_tor=rho_tor_core_prof
        new_IDS.core_profiles.profiles_1d[0].grid.rho_tor_norm=(rho_tor_core_prof-rho_tor_core_prof[0])/(rho_tor_core_prof[-1]-rho_tor_core_prof[0]) #remove rho_tor_norm as this grid seems to be different

        #if species not present in table_species_AZ - i.e. we do not want it in there - set density to very low
        az_avail=list(table_species_AZ.values())
        for ion_counter,ion in enumerate(new_IDS.core_profiles.profiles_1d[0].ion):
            if [ion.element[0].a,ion.element[0].z_n] not in az_avail: 
                new_IDS.core_profiles.profiles_1d[0].ion[ion_counter].density=np.full(len(new_IDS.core_profiles.profiles_1d[0].ion[ion_counter].density),1.)
                new_IDS.core_profiles.profiles_1d[0].ion[ion_counter].density_thermal=np.full(len(new_IDS.core_profiles.profiles_1d[0].ion[ion_counter].density),1.)

        #set time data
        new_IDS.nbi.ids_properties.homogeneous_time = 1
        new_IDS.equilibrium.ids_properties.homogeneous_time = 1
        new_IDS.core_profiles.ids_properties.homogeneous_time = 1
        new_IDS.distribution_sources.ids_properties.homogeneous_time = 1
        new_IDS.distributions.ids_properties.homogeneous_time = 1
        new_IDS.wall.ids_properties.homogeneous_time = 1

        new_IDS.nbi.time = np.array([0.0])
        new_IDS.equilibrium.time = np.array([0.0])
        new_IDS.core_profiles.time = np.array([0.0])
        new_IDS.distribution_sources.time = np.array([0.0])
        new_IDS.distributions.time = np.array([0.0])
        new_IDS.wall.time = np.array([0.0])

        new_IDS.nbi.put()
        new_IDS.equilibrium.put()
        new_IDS.core_profiles.put()
        new_IDS.distribution_sources.put()
        new_IDS.distributions.put()
        new_IDS.wall.put()
           
        IDS_nbi.close()
        IDS_source.close()
        new_IDS.close()

        #fill in temperatures, density and rotations for ALL species we want

        density_electrons=Number_Density(ID='',data_format='EXCEL1',species='electrons',filename=self.args['RMP_study__filepath_kinetic_profiles'].relative_to(support.dir_input_files),sheet_name=self.args['parameters__sheet_name_kinetic_prof'])
        density_electrons['flux_pol']=density_electrons['flux_pol_norm']*(equilibrium['sibry']-equilibrium['simag'])+equilibrium['simag']
        density_electrons.dump_data(data_format='IDS',shot=self.args['IDS__shot'],run=self.args['IDS__run'],species='electrons')

        for species_name,species_AZ in table_species_AZ.items(): #loop through all non-electronic ion species and set equal temperature

            temperature=Temperature(ID='',data_format='EXCEL1',species='ions',filename=self.args['RMP_study__filepath_kinetic_profiles'].relative_to(support.dir_input_files),sheet_name=self.args['parameters__sheet_name_kinetic_prof'])
            rotation=Rotation(ID='',data_format='EXCEL1',filename=self.args['RMP_study__filepath_kinetic_profiles'].relative_to(support.dir_input_files),sheet_name=self.args['parameters__sheet_name_kinetic_prof'],rotation_name=self.args['parameters__var_name_rotation'],sheet_name_rotation=self.args['parameters__sheet_name_rotation'])

            if species_name is 'beryllium':
                density=copy.deepcopy(density_electrons)
                density['n']*=fraction_beryllium #assumed 2% electron density
                density.properties['species']=species_name #re-label species type

            elif species_name is 'neon':
                density=copy.deepcopy(density_electrons)
                density['n']*=fraction_neon #assumed .2% electron density
                density.properties['species']=species_name #re-label species type

            elif {species for species in table_species_AZ}=={'deuterium','tritium'}: #if running pure DT set DT densities to half electron density 
                density=copy.deepcopy(density_electrons)
                density['n']*=.5 #assumed 50% electron density
                density.properties['species']=species_name #re-label species type
        
            else:
                try: #just try to read all species, some (e.g. Ne and Be) of which might not be present, so until errors are properly raised then errors may be printed - please ignore
                    density=Number_Density(ID='',data_format='EXCEL1',species=species_name,filename=self.args['RMP_study__filepath_kinetic_profiles'].relative_to(support.dir_input_files),sheet_name=self.args['parameters__sheet_name_kinetic_prof'])
                except:
                    density=None

            for inpt in [temperature,rotation,density]:
                if inpt is not None:
                    inpt['flux_pol']=inpt['flux_pol_norm']*(equilibrium['sibry']-equilibrium['simag'])+equilibrium['simag']
                    inpt.dump_data(data_format='IDS',shot=self.args['IDS__shot'],run=self.args['IDS__run'],species=species_name,A=species_AZ[0],Z=species_AZ[1])

        #add wall
        wall=Wall(ID='',data_format='GEQDSK',filename=self.args['RMP_study__filepath_equilibrium'])
        wall.dump_data(data_format='IDS_2D',shot=self.args['IDS__shot'],run=self.args['IDS__run'])

    def extrapolate_kinetic_profiles(self,*args,**kwargs):
        """
        notes:
        """

        #read all the kinetic profiles

        densities=[]
        temperatures=[]
        rotations=[]

        density_electrons=Number_Density(ID='',
                                        data_format='EXCEL1',
                                        species='electrons',
                                        A=None,
                                        Z=None,
                                        filename=self.args['RMP_study__filepath_kinetic_profiles'].relative_to(support.dir_input_files),
                                        sheet_name=self.args['parameters__sheet_name_kinetic_prof'])                 
        density_electrons.set(          output_filename=self.args['LOCUST_run__dir_input'] / 'profile_ne.dat') #include filename for dumping later
        densities.append(density_electrons)

        for species_name,species_AZ in table_species_AZ.items(): #loop through all non-electronic ion species and set number density            
            density=None
            #XXX add species which are 'assumed' - these are not contained in the data anywhere right now
            if species_name is 'beryllium':
                density=copy.deepcopy(density_electrons)
                density['n']*=fraction_beryllium #assumed 2% electron density
            elif species_name is 'neon':
                density=copy.deepcopy(density_electrons)
                density['n']*=fraction_neon #assumed .2% electron density
            else:
                try: #just try to read all species, some (e.g. Ne and Be) of which might not be present, so until errors are properly raised then errors may be printed - please ignore
                    density=Number_Density(
                        ID='',
                        data_format='EXCEL1',
                        species=species_name,
                        A=species_AZ[0],
                        Z=species_AZ[1],
                        filename=self.args['RMP_study__filepath_kinetic_profiles'].relative_to(support.dir_input_files),
                        sheet_name=self.args['parameters__sheet_name_kinetic_prof'])
                except:
                    pass
            if density is not None: 
                density.properties['species']=species_name #re-label species type and A and Z 
                density.properties['A']=species_AZ[0] 
                density.properties['Z']=species_AZ[1] 
                density.set(output_filename=self.args['LOCUST_run__dir_input'] / 'density_{}'.format(density.properties['species'])) #include filename for dumping later 
                densities.append(density)

        for species_name in ['electrons','ions']:
            temperature=Temperature(
                            ID='',
                            data_format='EXCEL1',
                            species=species_name,
                            A=None,
                            Z=None,
                            filename=self.args['RMP_study__filepath_kinetic_profiles'].relative_to(support.dir_input_files),
                            sheet_name=self.args['parameters__sheet_name_kinetic_prof'])
            temperature.set(output_filename=self.args['LOCUST_run__dir_input'] / 'profile_T{}.dat'.format(temperature.properties['species'][0])) #include filename for dumping later 
            temperatures.append(temperature)

        rotation=Rotation(ID='',
                        data_format='EXCEL1',
                        filename=self.args['RMP_study__filepath_kinetic_profiles'].relative_to(support.dir_input_files),
                        sheet_name=self.args['parameters__sheet_name_kinetic_prof'],
                        rotation_name=self.args['parameters__var_name_rotation'],
                        sheet_name_rotation=self.args['parameters__sheet_name_rotation'],
                        species='ions',
                        A=None,
                        Z=None)
        rotation.set(   output_filename=self.args['LOCUST_run__dir_input'] / 'profile_wT.dat') #include filename for dumping later 
        rotations.append(rotation)

        equilibrium=Equilibrium(ID='', #since kinetic profiles do not extend past LCFS must use equilibrium data
                                data_format='IDS',
                                shot=self.args['IDS__target_IDS_shot'],
                                run=self.args['IDS__target_IDS_run'],
                                username='public',
                                imasdb='ITER',
                                imas_version='3'
                                ) #extrapolate using IDS equilibrium since it contains toroidal flux for NEMO
        
        rmaxis,zmaxis,simag=equilibrium.mag_axis_calc()
        equilibrium.set(rmaxis=rmaxis,zmaxis=zmaxis,simag=simag)

        density_extrapolate_settings={}
        temperature_extrapolate_settings={}
        rotation_extrapolate_settings={}
        density_extrapolate_settings['decay_length']=.03
        temperature_extrapolate_settings['decay_length']=.015
        rotation_extrapolate_settings['decay_length']=0.0000000001
        density_extrapolate_settings['floor_distance']=0.045
        temperature_extrapolate_settings['floor_value']=20
        rotation_extrapolate_settings['floor_value']=0

        #for kinetic_profile_group,extrapolate_settings in zip([temperatures],[temperature_extrapolate_settings]):
        for kinetic_profile_group,extrapolate_settings in zip([densities,temperatures,rotations],[density_extrapolate_settings,temperature_extrapolate_settings,rotation_extrapolate_settings]):
            kinetic_profile_group=processing.utils.extrapolate_kinetic_profiles_ITER(equilibrium,*kinetic_profile_group,**extrapolate_settings)
            for kinetic_profile in kinetic_profile_group:
                kinetic_profile.dump_data(data_format='LOCUST',filename=str(kinetic_profile['output_filename']))#first dump to LOCUST format

        '''                
                #then re-dump to IDS - making sure ion temperature/rotation is set equal across all ion species in IDS
                if (kinetic_profile.LOCUST_input_type is 'temperature' or kinetic_profile.LOCUST_input_type is 'rotation') and kinetic_profile.properties['species'] is 'ions': 
                    for species_name,species_AZ in table_species_AZ.items():
                        kinetic_profile.dump_data(  
                                                    data_format='IDS',
                                                    shot=self.args['IDS__shot'],
                                                    run=self.args['IDS__run'],
                                                    species=species_name,
                                                    A=species_AZ[0],
                                                    Z=species_AZ[1],
                                                    username=self.args['IDS__username'],
                                                    imasdb=self.args['IDS__imasdb'],
                                                    imas_version=settings.imas_version
                                                    )
                else:
                    kinetic_profile.dump_data(  
                                                data_format='IDS',
                                                shot=self.args['IDS__shot'],
                                                run=self.args['IDS__run'],
                                                species=kinetic_profile.properties['species'],
                                                A=kinetic_profile.properties['A'],
                                                Z=kinetic_profile.properties['Z'],
                                                username=self.args['IDS__username'],
                                                imasdb=self.args['IDS__imasdb'],
                                                imas_version=settings.imas_version
                                                )

        #since no delete API in IMAS at the moment we need to re-overwrite profiles of unwanted species since axes will have changed  
        try:
            import imas 
        except:
            raise ImportError("ERROR: read_beam_depo_IDS could not import IMAS module!\nreturning\n")
            return
        az_avail=list(table_species_AZ.values())
        IDS=imas.ids(self.args['IDS__shot'],self.args['IDS__run'])
        IDS.open_env(self.args['IDS__username'],self.args['IDS__imasdb'],settings.imas_version) 
        IDS.core_profiles.get()
        for ion_counter,ion in enumerate(IDS.core_profiles.profiles_1d[0].ion):
            if [ion.element[0].a,ion.element[0].z_n] not in az_avail: 
                IDS.core_profiles.profiles_1d[0].ion[ion_counter].density=np.full(len(IDS.core_profiles.profiles_1d[0].grid.psi),1.) #make sure all data used by NBI component is overwritten here
                IDS.core_profiles.profiles_1d[0].ion[ion_counter].density_thermal=np.full(len(IDS.core_profiles.profiles_1d[0].grid.psi),1.)
                IDS.core_profiles.profiles_1d[0].ion[ion_counter].temperature=np.full(len(IDS.core_profiles.profiles_1d[0].grid.psi),1.)
                IDS.core_profiles.profiles_1d[0].ion[ion_counter].rotation_frequency_tor=np.full(len(IDS.core_profiles.profiles_1d[0].grid.psi),1.)
                IDS.core_profiles.profiles_1d[0].ion[ion_counter].velocity.toroidal=np.full(len(IDS.core_profiles.profiles_1d[0].grid.psi),1.)
        IDS.core_profiles.put()
        IDS.close()
        '''                

    def plot_kinetic_profiles(self,*args,**kwargs):
        """
        notes:
        """
        
        import matplotlib.pyplot as plt
        fig,ax=plt.subplots(1)
        self._plot_kinetic_profiles(ax=ax,fig=fig)

    def run_NEMO(self,*args,**kwargs):
        """
        notes:
        """

        NEMO_workflow=run_scripts.NEMO_run.NEMO_run(
        dir_NEMO=self.args['NEMO_run__dir_NEMO'],
        shot_in=self.args['IDS__shot'],
        shot_out=self.args['IDS__shot'],
        run_in=self.args['IDS__run'],
        run_out=self.args['IDS__run'],
        username=settings.username,
        imasdb=settings.imasdb,
        imas_version=settings.imas_version,
        xml_settings=self.args['NEMO_run__xml_settings'])

        NEMO_workflow.call_NEMO_actor_command_line()

    def run_BBNBI(self,*args,**kwargs):
        """
        notes:
        """

        BBNBI_workflow=run_scripts.BBNBI_run.BBNBI_run(
                dir_BBNBI=self.args['BBNBI_run__dir_BBNBI'],
                shot_in=self.args['IDS__shot'],
                shot_out=self.args['IDS__shot'],
                run_in=self.args['IDS__run'],
                run_out=self.args['IDS__run'],
                username=settings.username,
                imasdb=settings.imasdb,
                imas_version=settings.imas_version,
                xml_settings=self.args['BBNBI_run__xml_settings'],
                number_particles=self.args['BBNBI_run__number_particles'],
                number_processors=1
            )
        
        BBNBI_workflow.call_BBNBI_actor_command_line()

    def get_beam_deposition_IDS(self,*args,**kwargs):
        """
        notes:
        """

        beam_deposition=Beam_Deposition(ID='',data_format='IDS',shot=self.args['IDS__shot'],run=self.args['IDS__run'])
        beam_deposition.dump_data(data_format='LOCUST_FO_weighted',filename=self.args['LOCUST_run__dir_input'] / 'ptcles.dat') 

    def get_beam_deposition_file(self,*args,**kwargs):
        """ 
        fetch pre-calculated beam deposition from file

        notes:
            currently looks in run cache folder only
            in case system does not support NEMO
        """ 

        file=str(self.args['LOCUST_run__dir_cache'] / 'ptcles.dat')
        dir_input=str(self.args['LOCUST_run__dir_input'])
        try:
            subprocess.run(shlex.split('cp {file} {dir_input}'.format(file=file,dir_input=dir_input)),shell=False)
        except:
            print(f"ERROR: {self.workflow_name}.{self.command_running_name}() could not find beam depo {file}!")

    def plot_beam_deposition(self,*args,**kwargs):
        """
        plots the beam deposition stored in target IDS

        notes:
        """

        equilibrium=Equilibrium(ID='',data_format='GEQDSK',filename=self.args['RMP_study__filepath_equilibrium'],GEQDSKFIX1=True,GEQDSKFIX2=True)
        self._plot_beam_deposition(axes=['R','Z'],number_bins=500,real_scale=True,LCFS=equilibrium,limiters=equilibrium,style='scatter')

    def plot_equilibrium(self,*args,**kwargs):
        """
        notes:
        """

        equilibrium=Equilibrium(ID='',data_format='GEQDSK',filename=self.args['RMP_study__filepath_equilibrium'],GEQDSKFIX1=True,GEQDSKFIX2=True)
        equilibrium.B_calc()
        equilibrium.plot(key='B_field_tor')

    def BCHECK_3D(self,*args,**kwargs):
        """
        step for checking 3D field perturbation is correct as separate coils vs combined vs vacuum field supplied

        notes:
            if running LOCUST with separate coil_rows then script will include combined field, if running LOCUST with combined field separate field is not generated here
            (although could be in future by just evoking self.calc_3D_fields() and editing prec_mod settings)
            can only compare with probe_g vacuum data if n=3 or n=3
        """

        #define 1D of points to compare at
        num_points=1000
        R_point=6.2273
        Z_point=0.0571
        #R_point=6.08
        #Z_point=-0.5
        phi_points=np.linspace(0,2.*np.pi,num_points)
        rad_2_deg=180./np.pi
        time_points=np.full(num_points,0.)

        for counter_mode,mode in enumerate(self.args['parameters__toroidal_mode_numbers']):

            field_type=None #flag for toggling combined or separate 3D fields

            #if workflow using separate coilsets then create combined 3D field
            field_type='separate' if 'COILROW' in self.args['MARS_read__flags'] else 'combined'

            if field_type is 'separate': #then create the combined field
                MARS_read__flags=copy.deepcopy(self.args['MARS_read__flags'])
                del(MARS_read__flags['COILROW'])
                MARS_read__flags['NC']=np.abs(mode)    
                field_builder=MARS_builder_run(filepath_input=self.args['MARS_read__HEAD'][counter_mode],dir_output=self.args['LOCUST_run__dir_input'],
                                                dir_MARS_builder=self.args['MARS_read__dir_MARS_builder'],environment_name=self.args['LOCUST_run__environment_name'],
                                                settings_mars_read=self.args['MARS_read__settings'],flags=MARS_read__flags)
                field_builder.run()

            #look for combined BPLASMA file and create point_data.inp field checking file for LOCUST based on the grid dimensions
            combined_field=Perturbation('',data_format='LOCUST',filename=(self.args['LOCUST_run__dir_input'] / f'BPLASMA_n{np.abs(mode)}').relative_to(support.dir_input_files))

            combined_field.set(
                time_point_data=time_points,
                phi_point_data=phi_points,
                R_point_data=np.full(num_points,R_point),
                Z_point_data=np.full(num_points,Z_point))
            
            dbr,dbtor,dbz=combined_field.evaluate( #evaluate field using my own routine to check 
                R=combined_field['R_point_data'], 
                phi=combined_field['phi_point_data'],
                Z=combined_field['Z_point_data'],
                mode_number=mode,
                i3dr=self.args['LOCUST_run__settings_prec_mod']['i3dr'], #XXX CURRENTLY WAITING FOR FIX
                phase=0)
            combined_field.set(dB_field_R=dbr,dB_field_tor=dbtor,dB_field_Z=dbz) 

            #now time to run LOCUST BCHECK on combined field
            combined_field.dump_data(data_format='point_data',filename=self.args['LOCUST_run__dir_input'] / 'point_data.inp')
            LOCUST_run__flags_combined=copy.deepcopy(self.args['LOCUST_run__flags']) #alter LOCUST compile flags to control run mode
            LOCUST_run__flags_combined['NOPFC']=True #speed up by ignoring large mesh
            if 'SPLIT' in LOCUST_run__flags_combined: del(LOCUST_run__flags_combined['SPLIT'])
            if 'NCOILS' in LOCUST_run__flags_combined: del(LOCUST_run__flags_combined['NCOILS'])
            LOCUST_run__flags_combined['BCHECK']=1
            LOCUST_run__settings_prec_mod_combined=copy.deepcopy(self.args['LOCUST_run__settings_prec_mod'])
            LOCUST_run__settings_prec_mod_combined['phase']='[0.0_gpu]'
            LOCUST_run__settings_prec_mod_combined['omega']='[0.0_gpu]'
            LOCUST_run__settings_prec_mod_combined['nmde']=1
            LOCUST_run__settings_prec_mod_combined['nnum']='[{}]'.format(mode)
            
            LOCUST_workflow=run_scripts.LOCUST_run.LOCUST_run(
                environment_name=self.args['LOCUST_run__environment_name'],
                repo_URL=self.args['LOCUST_run__repo_URL'],
                commit_hash=self.args['LOCUST_run__commit_hash'],
                dir_LOCUST=self.args['LOCUST_run__dir_LOCUST'],
                dir_LOCUST_source=self.args['LOCUST_run__dir_LOCUST_source'],
                dir_input=self.args['LOCUST_run__dir_input'],
                dir_output=self.args['LOCUST_run__dir_output'],
                dir_cache=self.args['LOCUST_run__dir_cache'],
                settings_prec_mod=LOCUST_run__settings_prec_mod_combined,
                flags=LOCUST_run__flags_combined)
            LOCUST_workflow.run()

            (self.args['LOCUST_run__dir_output'] / 'field_data.out').rename(self.args['LOCUST_run__dir_output'] / 'field_data_combined.out')
            combined_field_BCHECK=Perturbation('',data_format='LOCUST_field_data',filename=(self.args['LOCUST_run__dir_output'] / 'field_data_combined.out').relative_to(support.dir_output_files))
            
            #now time to run LOCUST BCHECK on separate field
            if field_type is 'separate':
                LOCUST_run__flags_separate=copy.deepcopy(self.args['LOCUST_run__flags'])
                LOCUST_run__flags_separate['BCHECK']=1
                LOCUST_run__flags_separate['NOPFC']=True #speed up by ignoring large mesh
                if 'SPLIT' in LOCUST_run__flags_separate: del(LOCUST_run__flags_separate['SPLIT'])
                LOCUST_run__settings_prec_mod_separate=copy.deepcopy(self.args['LOCUST_run__settings_prec_mod'])
                LOCUST_run__settings_prec_mod_separate['phase']='[0.0_gpu,0.0_gpu,0.0_gpu]'
                LOCUST_run__settings_prec_mod_separate['omega']='[0.0_gpu,0.0_gpu,0.0_gpu]'
                LOCUST_run__settings_prec_mod_separate['nmde']=3
                LOCUST_run__settings_prec_mod_separate['nnum']='[{},{},{}]'.format(mode,mode,mode)

                LOCUST_workflow=run_scripts.LOCUST_run.LOCUST_run(
                    environment_name=self.args['LOCUST_run__environment_name'],
                    repo_URL=self.args['LOCUST_run__repo_URL'],
                    commit_hash=self.args['LOCUST_run__commit_hash'],
                    dir_LOCUST=self.args['LOCUST_run__dir_LOCUST'],
                    dir_LOCUST_source=self.args['LOCUST_run__dir_LOCUST_source'],
                    dir_input=self.args['LOCUST_run__dir_input'],
                    dir_output=self.args['LOCUST_run__dir_output'],
                    dir_cache=self.args['LOCUST_run__dir_cache'],
                    settings_prec_mod=LOCUST_run__settings_prec_mod_separate,
                    flags=LOCUST_run__flags_separate)
                LOCUST_workflow.run()
        
                (self.args['LOCUST_run__dir_output'] / 'field_data.out').rename(self.args['LOCUST_run__dir_output'] / 'field_data_separate.out')
                field_separate_BCHECK=Perturbation('',data_format='LOCUST_field_data',filename=(self.args['LOCUST_run__dir_output'] / 'field_data_separate.out').relative_to(support.dir_output_files))

            combined_field.look()
            combined_field_BCHECK.look()

            #now plot combined field evaluated by me and locust, separate field evaluated by LOCUST and fractional difference between combined and separate field
            if field_type is 'separate':
                field_difference=copy.deepcopy(field_separate_BCHECK)
            import matplotlib.pyplot as plt
            fig,(ax1,ax2)=plt.subplots(2,1)
            for quantity_MARSF in ['dB_field_R','dB_field_tor','dB_field_Z']:
                if field_type is 'separate':
                    field_difference[quantity_MARSF]-=combined_field_BCHECK[quantity_MARSF]
                    field_difference[quantity_MARSF]/=combined_field_BCHECK[quantity_MARSF] #get fractional difference between the two fields
                    ax1.plot(field_difference[quantity_MARSF],'m-')
                    ax2.plot(field_separate_BCHECK[quantity_MARSF],'g-')
                ax2.plot(phi_points*rad_2_deg,combined_field[quantity_MARSF],'b',linestyle='--')
                ax2.plot(phi_points*rad_2_deg,combined_field_BCHECK[quantity_MARSF],'b',linestyle='-')
            #plt.savefig('BCHECK_{}.png'.format(mode),bbox_inches='tight')
            plt.show()

            fig,(axes)=plt.subplots(3,1)

            #read probe_g biot-savart code vacuum data
            d={}
            filename=pathlib.Path('..') / 'field_check' / 'probe_gb_TMB.out'
            with open(filename) as file:
                lines=file.readlines()
                while 'phi_tor(deg)' not in lines[0]:
                    del(lines[0])
                for column_number,variable in enumerate(lines[0].replace('%','').replace('(deg)','').replace('(m)','').split()): 
                    d[column_number]={}
                    d[column_number]['variable_name']=variable
                    d[column_number]['data']=[]
                del(lines[0])
                for line in lines:
                    for column_number,column in enumerate(line.split()):
                        d[column_number]['data'].append(float(column))

                for column_number in list(d.keys()):
                    #print(type(d[column_number]))
                    #print(column_number)
                    variable_name=d[column_number]['variable_name']
                    d[variable_name]=d.pop(column_number)
                    d[variable_name]=np.array(d[variable_name]['data'])

            x = d['phi_tor']*np.pi/180.#np.linspace(0,2*np.pi,361)
            y = np.array([d['B_R'],d['B_phi'],d['B_Z']]).T
            yn3 = np.full((y.shape[1]),1,dtype=complex)
            yn6 = np.full((y.shape[1]),1,dtype=complex)

            for k in range(y.shape[1]):
                yn3[k] = np.sum(y[:,k]*np.exp(-1j*3*x,dtype=complex),dtype=complex)
                yn6[k] = np.sum(y[:,k]*np.exp(-1j*6*x,dtype=complex),dtype=complex)

            yn3 = yn3*(x[1]-x[0])/2/np.pi*2 #XXX original - (x[1]-x[0]) factor needed due to transition from continuous to DFT
            yn6 = yn6*(x[1]-x[0])/2/np.pi*2 #XXX original 

            phi0 = 30. #origin for probe_g data
            Cphi = np.exp((d['phi_tor'])*3*1j*np.pi/180) 
            rBRn3 = (yn3[0]*Cphi).real
            rBPn3 = (yn3[1]*Cphi).real
            rBZn3 = (yn3[2]*Cphi).real

            Cphi = np.exp((d['phi_tor'])*6*1j*np.pi/180) 
            rBRn6 = (yn6[0]*Cphi).real
            rBPn6 = (yn6[1]*Cphi).real
            rBZn6 = (yn6[2]*Cphi).real

            if np.abs(mode)==3:
                dBR,dBphi,dBZ=rBRn3,rBPn3,rBZn3
            elif np.abs(mode)==6:
                dBR,dBphi,dBZ=rBRn6,rBPn6,rBZn6
            else:
                dBR,dBphi,dBZ=[np.full(num_points,0.)]*3

            for ax,quantity_MARSF,quantity_probeG in zip(axes,['dB_field_R','dB_field_tor','dB_field_Z'],[dBR,dBphi,dBZ]):
                ax.plot(d['phi_tor']+phi0,quantity_probeG,'g-',label=f'{quantity_MARSF} probe_g')
                ax.plot(phi_points*rad_2_deg,combined_field[quantity_MARSF],'b',linestyle='--',label=f'{quantity_MARSF} eval') #overplot these as they SHOULD be the same
                ax.plot(phi_points*rad_2_deg,combined_field_BCHECK[quantity_MARSF],'b',linestyle='-',label=f'{quantity_MARSF} bchck')
                ax.legend() #XXX added
                ax.set_ylabel('mag [T]') #XXX added
            axes[-1].set_xlabel('$\phi$ [degrees]') #XXX added

            plt.show()

    def calc_divergence(self,*args,**kwargs):
        """
        step for calculating B field divergence - in R,Z plane and X,Y planes

        notes:
        """
        
        import matplotlib.pyplot as plt

        #modify current LOCUST run flags
        LOCUST_run__flags_div_check=copy.deepcopy(self.args['LOCUST_run__flags'])
        LOCUST_run__flags_div_check['BCHECK']=1
        LOCUST_run__flags_div_check['NOPFC']=True #speed up by ignoring large mesh
        if 'SPLIT' in LOCUST_run__flags_div_check: del(LOCUST_run__flags_div_check['SPLIT'])

        #check the equilibrium to get an idea of domain to check over
        equilibrium=Equilibrium(ID='',data_format='GEQDSK',filename=self.args['RMP_study__filepath_equilibrium'],GEQDSKFIX1=True,GEQDSKFIX2=True)
        
        if not list(self.args['LOCUST_run__dir_output'].glob('field_data_divergence_check_RZ.out')):
            #check divergence in poloidal plane
            field_data=Perturbation('') 
            Z_points,R_points=np.meshgrid(equilibrium['Z_1D'],equilibrium['R_1D'])
            Z_points_flat,R_points_flat=Z_points.flatten(),R_points.flatten()
            time_points_flat=np.zeros(len(R_points_flat))
            phi_slice=0.
            phi_points_flat=np.full(len(R_points_flat),phi_slice)
            
            field_data.set(
                time_point_data=time_points_flat,
                phi_point_data=phi_points_flat,
                R_point_data=R_points_flat,
                Z_point_data=Z_points_flat)
            field_data.dump_data(data_format='point_data',filename=self.args['LOCUST_run__dir_input'] / 'point_data.inp')
            LOCUST_workflow=run_scripts.LOCUST_run.LOCUST_run(
                environment_name=self.args['LOCUST_run__environment_name'],
                repo_URL=self.args['LOCUST_run__repo_URL'],
                commit_hash=self.args['LOCUST_run__commit_hash'],
                dir_LOCUST=self.args['LOCUST_run__dir_LOCUST'],
                dir_LOCUST_source=self.args['LOCUST_run__dir_LOCUST_source'],
                dir_input=self.args['LOCUST_run__dir_input'],
                dir_output=self.args['LOCUST_run__dir_output'],
                dir_cache=self.args['LOCUST_run__dir_cache'],
                settings_prec_mod=self.args['LOCUST_run__settings_prec_mod'],
                flags=LOCUST_run__flags_div_check)
            LOCUST_workflow.run()
            (self.args['LOCUST_run__dir_output'] / 'field_data.out').rename(self.args['LOCUST_run__dir_output'] / 'field_data_divergence_check_RZ.out')

        if not list(self.args['LOCUST_run__dir_output'].glob('field_data_divergence_check_XY.out')):
            #check divergence in XY plane
            field_data=Perturbation('')
            number_phi_points=100
            phi_points=np.linspace(0.,2.*np.pi,number_phi_points) 
            R_points,phi_points=np.meshgrid(equilibrium['R_1D'],phi_points)
            phi_points_flat,R_points_flat=phi_points.flatten(),R_points.flatten()
            time_points_flat=np.zeros(len(R_points_flat))
            Z_slice=0.
            Z_points_flat=np.full(len(R_points_flat),Z_slice)
            
            field_data.set(
                time_point_data=time_points_flat,
                phi_point_data=phi_points_flat,
                R_point_data=R_points_flat,
                Z_point_data=Z_points_flat)
            field_data.dump_data(data_format='point_data',filename=self.args['LOCUST_run__dir_input'] / 'point_data.inp')
            LOCUST_workflow=run_scripts.LOCUST_run.LOCUST_run(
                environment_name=self.args['LOCUST_run__environment_name'],
                repo_URL=self.args['LOCUST_run__repo_URL'],
                commit_hash=self.args['LOCUST_run__commit_hash'],
                dir_LOCUST=self.args['LOCUST_run__dir_LOCUST'],
                dir_LOCUST_source=self.args['LOCUST_run__dir_LOCUST_source'],
                dir_input=self.args['LOCUST_run__dir_input'],
                dir_output=self.args['LOCUST_run__dir_output'],
                dir_cache=self.args['LOCUST_run__dir_cache'],
                settings_prec_mod=self.args['LOCUST_run__settings_prec_mod'],
                flags=LOCUST_run__flags_div_check)
            LOCUST_workflow.run()
            (self.args['LOCUST_run__dir_output'] / 'field_data.out').rename(self.args['LOCUST_run__dir_output'] / 'field_data_divergence_check_XY.out')
        
    def plot_inputs(self,*args,**kwargs):
        """
        notes:

            XXX could eventually make this into a class - define an axes then attach different LOCUST_IO quantities to it and then it can plot them
        """ 

        axes=['phi','R']

        import matplotlib.pyplot as plt

        fig1=plt.figure()
        polar=True if axes==['phi','R'] else False
        ax1=fig1.add_subplot(111,polar=polar)
        equilibrium=Equilibrium(ID='',data_format='GEQDSK',filename=self.args['RMP_study__filepath_equilibrium'],GEQDSKFIX1=True,GEQDSKFIX2=True)

        self._plot_perturbations(key='dB_field_mag',axes=axes,LCFS=False,limiters=False,number_bins=100,fill=True,vminmax=None,i3dr=self.args['LOCUST_run__settings_prec_mod']['i3dr'],phase=0.,colmap=settings.cmap_default,colmap_val=np.random.uniform(),line_style=settings.plot_line_style,gridlines=False,label='',ax=ax1,fig=fig1)
        #XXX self._plot_beam_deposition(fill=False,style='scatter',colmap=settings.cmap_g,number_bins=5,axes=axes,ax=ax1,fig=fig1)

        #now deal with static add-on features to plot e.g. coils
        plot_coils=True
        if plot_coils:
            from plot_scripts.plot_coils_RMP_ITER import plot_coils_RMP_ITER
            plot_coils_RMP_ITER(axes=axes,shot=1180,run=17,username='public',imasdb='ITER_MD',imas_version='3',imas_entry=0,plot_centres=True,colmap=settings.cmap_k,colmap_val=np.random.uniform(),ax=ax1,fig=fig1)
            #title_string_phases=f"phase U={self.args['MARS_read__flags']['UPHASE']} M={self.args['MARS_read__flags']['MPHASE']} L={self.args['MARS_read__flags']['LPHASE']}"

        fig2,ax2=plt.subplots(1)
        self._plot_kinetic_profiles(ax=ax2,fig=fig2)
        
        plt.show()

    def run_LOCUST(self,*args,**kwargs):
        """
        notes:
        """

        if not list(self.args['LOCUST_run__dir_output'].glob('*.dfn')):
            LOCUST_workflow=run_scripts.LOCUST_run.LOCUST_run(
                environment_name=self.args['LOCUST_run__environment_name'],
                repo_URL=self.args['LOCUST_run__repo_URL'],
                commit_hash=self.args['LOCUST_run__commit_hash'],
                dir_LOCUST=self.args['LOCUST_run__dir_LOCUST'],
                dir_LOCUST_source=self.args['LOCUST_run__dir_LOCUST_source'],
                dir_input=self.args['LOCUST_run__dir_input'],
                dir_output=self.args['LOCUST_run__dir_output'],
                dir_cache=self.args['LOCUST_run__dir_cache'],
                settings_prec_mod=self.args['LOCUST_run__settings_prec_mod'],
                flags=self.args['LOCUST_run__flags'])
            LOCUST_workflow.run()

    def create_Poincare(self,*args,**kwargs):
        """
        notes:
        """


        if not list(self.args['LOCUST_run__dir_output'].glob('Poincare_map*.dat')):
            poincare_flags=copy.deepcopy(self.args['LOCUST_run__flags'])
            poincare_flags['POINCARE']=3
            poincare_flags['NOPFC']=True #speed up by ignoring large mesh
            if 'SPLIT' in poincare_flags: del(poincare_flags['SPLIT']) #stop junk particle cache from Poincaré mode overwriting result
            poincare_workflow=run_scripts.LOCUST_run.LOCUST_run(
                environment_name=self.args['LOCUST_run__environment_name'],
                repo_URL=self.args['LOCUST_run__repo_URL'],
                commit_hash=self.args['LOCUST_run__commit_hash'],
                dir_LOCUST=self.args['LOCUST_run__dir_LOCUST'],
                dir_LOCUST_source=self.args['LOCUST_run__dir_LOCUST_source'],
                dir_input=self.args['LOCUST_run__dir_input'],
                dir_output=self.args['LOCUST_run__dir_output'],
                dir_cache=self.args['LOCUST_run__dir_cache'],
                settings_prec_mod=self.args['LOCUST_run__settings_prec_mod'],
                flags=poincare_flags)
            poincare_workflow.run()

    def calculate_orbits(self,*args,**kwargs):
        """
        run LOCUST to calculate trajectory of markers with termination flag=status_flags in 2D and 3D field

        args:
            status_flags - plot trajectories for markers which satisfy these termination flags
            number_markers - number of trajectories to plot
        notes:
            assume beam deposition already generated in the input directory and is in LOCUST_FO_weighted format
            assume output particle list already generated in the output directory
            works by exploiting the fact that the marker index does not change from input to output
        """

        number_markers=10
        ptcles_input=self.args['LOCUST_run__dir_input'] / 'ptcles.dat'
        ptcles_orbit=self.args['LOCUST_run__dir_input'] / 'ptcles.dat_orbit'

        input_list=Beam_Deposition(ID='',data_format='LOCUST_FO_weighted',filename=ptcles_input)
        output_list=Final_Particle_List(ID='',data_format='LOCUST',filename=self.args['LOCUST_run__dir_output']/'ptcl_cache.dat')
        indices=[]
        status_flags=['PFC_intercept_3D']
        for status_flag in status_flags:
            indices.extend(np.where(output_list['status_flag']==status_flag)[0])

        beam_depo=Beam_Deposition(ID='')
        beam_depo['R']=input_list['R'][indices]
        beam_depo['phi']=input_list['phi'][indices]
        beam_depo['Z']=input_list['Z'][indices]
        beam_depo['V_R']=input_list['V_R'][indices]
        beam_depo['V_phi']=input_list['V_phi'][indices]
        beam_depo['V_Z']=input_list['V_Z'][indices]
        beam_depo['weight']=input_list['weight'][indices]
        beam_depo.look()
        beam_depo.dump_data(data_format='LOCUST_FO_weighted',filename=ptcles_orbit,shuffle=False) 

        #rename files for LOCUST and to avoid overwriting
        ptcles_input.rename(self.args['LOCUST_run__dir_input'] / 'ptcles.dat_locust')
        ptcles_orbit.rename(self.args['LOCUST_run__dir_input'] / 'ptcles.dat')

        LOCUST_run__flags_orbit=copy.deepcopy(self.args['LOCUST_run__flags'])
        LOCUST_run__flags_orbit['PLOT']=number_markers
        LOCUST_run__flags_orbit['NOPFC']=True #speed up by ignoring large mesh
        if 'SPLIT' in LOCUST_run__flags_orbit: del(LOCUST_run__flags_orbit['SPLIT'])

        if all([arg in LOCUST_run__flags_orbit for arg in ['B3D','B3D_EX']]):

            if not list(self.args['LOCUST_run__dir_output'].glob('ORBIT_3D')):

                LOCUST_run__flags_orbit['TIMAX']='0.05D0' #0.01s~5GB for 10 markers, 1 bounce ~ 10us

                LOCUST_workflow=run_scripts.LOCUST_run.LOCUST_run(
                    environment_name=self.args['LOCUST_run__environment_name'],
                    repo_URL=self.args['LOCUST_run__repo_URL'],
                    commit_hash=self.args['LOCUST_run__commit_hash'],
                    dir_LOCUST=self.args['LOCUST_run__dir_LOCUST'],
                    dir_LOCUST_source=self.args['LOCUST_run__dir_LOCUST_source'],
                    dir_input=self.args['LOCUST_run__dir_input'],
                    dir_output=self.args['LOCUST_run__dir_output'],
                    dir_cache=self.args['LOCUST_run__dir_cache'],
                    settings_prec_mod=self.args['LOCUST_run__settings_prec_mod'],
                    flags=LOCUST_run__flags_orbit)
                LOCUST_workflow.run()
                list(self.args['LOCUST_run__dir_output'].glob('ORBIT*.dat'))[0].rename(self.args['LOCUST_run__dir_output'] / 'ORBIT_3D')
               
            del(LOCUST_run__flags_orbit['B3D'])
            del(LOCUST_run__flags_orbit['B3D_EX'])

        if not list(self.args['LOCUST_run__dir_output'].glob('ORBIT_2D')):

            LOCUST_run__flags_orbit['TIMAX']='0.00003D0' #1 bounce ~ 10us
            LOCUST_workflow=run_scripts.LOCUST_run.LOCUST_run(
                environment_name=self.args['LOCUST_run__environment_name'],
                repo_URL=self.args['LOCUST_run__repo_URL'],
                commit_hash=self.args['LOCUST_run__commit_hash'],
                dir_LOCUST=self.args['LOCUST_run__dir_LOCUST'],
                dir_LOCUST_source=self.args['LOCUST_run__dir_LOCUST_source'],
                dir_input=self.args['LOCUST_run__dir_input'],
                dir_output=self.args['LOCUST_run__dir_output'],
                dir_cache=self.args['LOCUST_run__dir_cache'],
                settings_prec_mod=self.args['LOCUST_run__settings_prec_mod'],
                flags=LOCUST_run__flags_orbit)
            LOCUST_workflow.run()
            list(self.args['LOCUST_run__dir_output'].glob('ORBIT*.dat'))[0].rename(self.args['LOCUST_run__dir_output'] / 'ORBIT_2D')

        #reverse file renaming
        ptcles_orbit.rename(self.args['LOCUST_run__dir_input'] / 'ptcles.dat_orbit')
        ptcles_input.rename(self.args['LOCUST_run__dir_input'] / 'ptcles.dat')

    def clean_input(self,*args,**kwargs):
        """

        notes:
        """

        #remove generated input files
        for file in self.args['LOCUST_run__dir_input'].glob('*'): 
            subprocess.run(shlex.split('rm {file}'.format(file=str(file))),shell=False)

    def clean_cache(self,*args,**kwargs):
        """

        notes:
        """

        #remove generated cache files
        for file in self.args['LOCUST_run__dir_cache'].glob('*'): 
            subprocess.run(shlex.split('rm {file}'.format(file=str(file))),shell=False)

if __name__=='__main__':

    import argparse
    parser=argparse.ArgumentParser(description='run RMP_study from command line in Python!')
    
    parser.add_argument('--parameters__sheet_name_kinetic_prof',type=str,action='store',dest='parameters__sheet_name_kinetic_prof',help="",default=None)
    parser.add_argument('--parameters__sheet_name_rotation',type=str,action='store',dest='parameters__sheet_name_rotation',help="",default=None)
    parser.add_argument('--parameters__var_name_rotation',type=str,action='store',dest='parameters__var_name_rotation',help="",default=None)
    parser.add_argument('--parameters__toroidal_mode_numbers',type=str,action='store',dest='parameters__toroidal_mode_numbers',help="",default=None)
    parser.add_argument('--LOCUST_run__dir_LOCUST',type=str,action='store',dest='LOCUST_run__dir_LOCUST',help="",default=support.dir_locust)
    parser.add_argument('--LOCUST_run__dir_LOCUST_source',type=str,action='store',dest='LOCUST_run__dir_LOCUST_source',help="",default=support.dir_locust / 'source')
    parser.add_argument('--LOCUST_run__dir_input',type=str,action='store',dest='LOCUST_run__dir_input',help="",default=support.dir_input_files)
    parser.add_argument('--LOCUST_run__dir_output',type=str,action='store',dest='LOCUST_run__dir_output',help="",default=support.dir_output_files)
    parser.add_argument('--LOCUST_run__dir_cache',type=str,action='store',dest='LOCUST_run__dir_cache',help="",default=support.dir_cache_files)
    parser.add_argument('--LOCUST_run__environment_name',type=str,action='store',dest='LOCUST_run__environment_name',help="",default='TITAN')
    parser.add_argument('--LOCUST_run__repo_URL',type=str,action='store',dest='LOCUST_run__repo_URL',help="",default=settings.repo_URL_LOCUST)
    parser.add_argument('--LOCUST_run__commit_hash',type=str,action='store',dest='LOCUST_run__commit_hash',help="",default=None)
    parser.add_argument('--LOCUST_run__settings_prec_mod',nargs='+',type=str,action='store',dest='LOCUST_run__settings_prec_mod',help="",default={})
    parser.add_argument('--LOCUST_run__flags',nargs='+',type=str,action='store',dest='LOCUST_run__flags',help="",default={})
    parser.add_argument('--NEMO_run__dir_NEMO',type=str,action='store',dest='NEMO_run__dir_NEMO',help="",default=support.dir_nemo)
    parser.add_argument('--NEMO_run__xml_settings',nargs='+',type=str,action='store',dest='NEMO_run__xml_settings',help="",default={})
    parser.add_argument('--BBNBI_run__dir_BBNBI',type=str,action='store',dest='BBNBI_run__dir_BBNBI',help="",default=support.dir_bbnbi)
    parser.add_argument('--BBNBI_run__xml_settings',nargs='+',type=str,action='store',dest='BBNBI_run__xml_settings',help="",default={})
    parser.add_argument('--BBNBI_run__number_particles',type=int,action='store',dest='BBNBI_run__number_particles',help="",default=10000)
    parser.add_argument('--MARS_read__tail_U',type=str,action='store',dest='MARS_read__tail_U',help="",default=None)
    parser.add_argument('--MARS_read__tail_M',type=str,action='store',dest='MARS_read__tail_M',help="",default=None)
    parser.add_argument('--MARS_read__tail_L',type=str,action='store',dest='MARS_read__tail_L',help="",default=None)
    parser.add_argument('--MARS_read__settings',nargs='+',type=str,action='store',dest='MARS_read__settings',help="",default={})
    parser.add_argument('--MARS_read__flags',nargs='+',type=str,action='store',dest='MARS_read__flags',help="",default={})
    parser.add_argument('--MARS_read__dir_MARS_builder',type=str,action='store',dest='MARS_read__dir_MARS_builder',help="",default=support.dir_cache_files / 'MARS_builder')
    parser.add_argument('--RMP_study__name',type=str,action='store',dest='RMP_study__name',help="",default=None)
    parser.add_argument('--RMP_study__filepath_kinetic_profiles',type=str,action='store',dest='RMP_study__filepath_kinetic_profiles',help="",default=None)
    parser.add_argument('--RMP_study__filepath_equilibrium',type=str,action='store',dest='RMP_study__filepath_equilibrium',help="",default=None)
    parser.add_argument('--RMP_study__filepath_additional_data',type=str,action='store',dest='RMP_study__filepath_additional_data',help="",default=None)
    parser.add_argument('--RMP_study__filepaths_3D_fields_U',type=str,action='store',dest='RMP_study__filepaths_3D_fields_U',help="",default=None)
    parser.add_argument('--RMP_study__filepaths_3D_fields_M',type=str,action='store',dest='RMP_study__filepaths_3D_fields_M',help="",default=None)
    parser.add_argument('--RMP_study__filepaths_3D_fields_L',type=str,action='store',dest='RMP_study__filepaths_3D_fields_L',help="",default=None)
    parser.add_argument('--RMP_study__workflow_commands',type=str,action='store',dest='RMP_study__workflow_commands',help="",default="")
    parser.add_argument('--IDS__shot',type=int,action='store',dest='IDS__shot',help="",default=1)
    parser.add_argument('--IDS__run',type=int,action='store',dest='IDS__run',help="",default=1)
    parser.add_argument('--IDS__username',type=str,action='store',dest='IDS__username',help="",default=None)
    parser.add_argument('--IDS__imasdb',type=str,action='store',dest='IDS__imasdb',help="",default=None)
    parser.add_argument('--IDS__target_IDS_shot',type=int,action='store',dest='IDS__target_IDS_shot',help="",default=1)
    parser.add_argument('--IDS__target_IDS_run',type=int,action='store',dest='IDS__target_IDS_run',help="",default=1)
    parser.add_argument('--IDS__NBI_shot',type=int,action='store',dest='IDS__NBI_shot',help="",default=130011)
    parser.add_argument('--IDS__NBI_run',type=int,action='store',dest='IDS__NBI_run',help="",default=1)
    parser.add_argument('--IDS__NBI_imasdb',type=str,action='store',dest='IDS__NBI_imasdb',help="",default='ITER')
    parser.add_argument('--IDS__NBI_username',type=str,action='store',dest='IDS__NBI_username',help="",default='public')

    args=parser.parse_args()

    #provide some extra parsing steps to dict-like and array-like input arguments
    args.LOCUST_run__settings_prec_mod=run_scripts.utils.command_line_arg_parse_dict(args.LOCUST_run__settings_prec_mod)
    args.LOCUST_run__flags=run_scripts.utils.command_line_arg_parse_dict(args.LOCUST_run__flags)
    args.MARS_read__settings=run_scripts.utils.command_line_arg_parse_dict(args.MARS_read__settings)
    args.MARS_read__flags=run_scripts.utils.command_line_arg_parse_dict(args.MARS_read__flags)
    args.NEMO_run__xml_settings=run_scripts.utils.command_line_arg_parse_dict(args.NEMO_run__xml_settings)
    args.BBNBI_run__xml_settings=run_scripts.utils.command_line_arg_parse_dict(args.BBNBI_run__xml_settings)
    args.RMP_study__filepaths_3D_fields_U=run_scripts.utils.literal_eval(args.RMP_study__filepaths_3D_fields_U)
    args.RMP_study__filepaths_3D_fields_M=run_scripts.utils.literal_eval(args.RMP_study__filepaths_3D_fields_M)
    args.RMP_study__filepaths_3D_fields_L=run_scripts.utils.literal_eval(args.RMP_study__filepaths_3D_fields_L)
    args.RMP_study__workflow_commands=run_scripts.utils.literal_eval(args.RMP_study__workflow_commands)
    args.parameters__toroidal_mode_numbers=run_scripts.utils.literal_eval(args.parameters__toroidal_mode_numbers)

    RMP_workflow=RMP_study_run(**{key:arg for key,arg in args._get_kwargs()})
    RMP_workflow.run()

#################################

##################################################################

###################################################################################################