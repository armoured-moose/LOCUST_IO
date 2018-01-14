#input_classes.py

"""
Samuel Ward
02/11/2017
----
python module for classes which hold LOCUST's input data
contains methods for reading/writing/converting/plotting/manipulating LOCUST input data
---
usage:
    see README.md for usage

notes:         
    TODO need to read up on readline() to see if there is some global counter keeps track of which file line the entire script is currently on
    i.e. whether two separate calls to readline() will read the same line or different line due to some global current line tracker. That will help explain
    the file_numbers function somewhat and whether all file lines are held by the thing that it returns when its called in the main code body
    TODO please check how get_next() works and whether it just returns one value at a time (this is what I think)

    TODO idea for a workflow could be to have a shell script which then issues commands to an interactive python session? is this possible?
---
"""


###################################################################################################
#Preamble

import sys #have global imports --> makes less modular (no "from input_classes import x") but best practice to import whole input_classes module anyway
try:
    import numpy as np
    import copy
    import re
    import time
    import itertools
    import copy
except:
    raise ImportError("ERROR: initial imported modules not found!\nreturning\n")
    sys.exit(1)
try:
    import support #import support module from this directory
except:
    raise ImportError("ERROR: support.py not found in this directory!\nreturning\n") 
    sys.exit(1)
try:
    import imas 
except:
    raise ImportError("ERROR: IMAS module not found!\nreturning\n")
    sys.exit(1)





















###################################################################################################
#Main Code









################################################################## Supporting functions

def none_check(ID,LOCUST_input_type,error_message,*args):
    """
    generic function for checking if a None value appears in *args

    notes:
        message should be something specific to the section of code which called none_check
    """
    if all(arg is not None for arg in args):
        return False
    else:
        print("WARNING: none_check returned True (LOCUST_input_type={LOCUST_input_type}, ID={ID}): {message}".format(LOCUST_input_type=LOCUST_input_type,ID=ID,message=error_message))
        return True
        
def file_numbers(ingf):#instance of generators are objects hence can use .next() method on them
    """
    generator to read numbers in a file

    notes:
        originally written by Ben Dudson

        calling get_next() on a generator produced with this function will permanently advance the iterator in this generator
        when generators reach the end, that's permanently it!
    """
    toklist = []
    while True: #runs forever until break statement (until what is read is not a line) below will cause a return - which permanently stops a generator
        line = ingf.readline() #read in line from INGF
        if not line: break #break if readline() doesnt return a line i.e. end of file
        line = line.replace("NaN","-0.00000e0") #replaces NaNs with 0s
        pattern = r'[+-]?\d*[\.]?\d+(?:[Ee][+-]?\d+)?' #regular expression to find numbers
        toklist = re.findall(pattern,line) #toklist now holds all the numbers in a file line (is essentially a single file line)
        for tok in toklist: #yield every number in that one line individually
            yield tok #so in terms of iteration, using get_next() will cause another line to be read

def get_next(obj):
    """
    generic object iterator

    notes:
        every time get_next() is called, it will advance the counter one
    """
    pyVer = sys.version_info[0]
    if pyVer == 2:
        return obj.next() #NOTE how exactly does .next() work? will it accept tok in toklist values from file_numbers() and allow file_numbers to then read in the next bunch (since yield will pause the While True loop?)
    else:
        return next(obj)




















################################################################## base class

class LOCUST_input:
    """
    base class for a generic LOCUST input object

    self.ID                     unique object identifier, good convention to fill these for error handling etc
    self.data                   holds all input data in dictionary object
    self.LOCUST_input_type      string which holds this class' input type

    notes:
    """

    LOCUST_input_type='base_input'

    def __init__(self,ID,data_format=None,input_filename=None,shot=None,run=None,properties=None): #this is common to all children (not overloaded), must have ID

        self.ID=ID #always set the ID, even if we don't invoke read_data i.e. a blank object is initialised
        if not none_check(self.ID,self.LOCUST_input_type,'read_data requires data_format, blank input initialised \n',data_format):
            self.read_data(data_format,input_filename,shot,run,properties)

    def read_data(self,data_format=None,input_filename=None,shot=None,run=None,properties=None): #bad practice to change overridden method signatures, so retain all method arguments             
        self.data=None #read_data definition is designed to be overloaded in children classes 
























################################################################## Equilibrium functions

def read_equilibrium_GEQDSK(input_filepath): 
    """ 
    generic function for reading a G-EQDSK-formatted equilibrium file

    notes:
        originally written by Ben Dudson and edited by Nick Walkden
        see README.md for data key

    """

    input_data = {}
    flags = {'loaded' : False } #NOTE might not need this variable now

    file = open(input_filepath) #open file
    
    line = file.readline() #first line should be case, id number and dimensions
    if not line:
        raise IOError("ERROR: read_equilibrium_GEQDSK() cannot read from "+input_filepath)
    
    #extract case, id number and dimensions  
    conts = line.split()    #split by white space (no argument in .split())
    input_data['nh'] = int(conts[-1]) #same as nyefit or height dimension
    input_data['nw'] = int(conts[-2]) #same as nxefit or width dimension
    input_data['idum'] = int(conts[-3])
    flags['case'] = conts[0:-4]

    #now use generator to read numbers from remaining lines in file
    token = file_numbers(file) #token now holds all lines in the file, containing all values. each get_next() call will grab the next number in a line (since get_next() returns the next value in the yield loop? check this plz)
    
    float_keys = [
    'rdim','zdim','rcentr','rleft','zmid',
    'rmaxis','zmaxis','simag','sibry','bcentr',
    'current','simag','xdum','rmaxis','xdum',
    'zmaxis','xdum','sibry','xdum','xdum']
    
    #read in all 0D floats
    for key in float_keys:                              
        input_data[key] = float(get_next(token)) #get_next(token) always yields just a single value
    
    def read_1d(n): 
        """
        """
        input_data = np.zeros([n]) #initialise blank lists
        for i in np.arange(n): #instead of using linspace or something makes a temporary numpy array of dimension n to iterate through
            input_data[i] = float(get_next(token))
        return input_data

    def read_2d(nx,ny):
        """
        """
        input_data = np.zeros([nx,ny])
        for i in np.arange(nx): #same technique here, iterate through one dimension and call read_1d along the other dimension
            input_data[i,:] = read_1d(ny)
        return input_data

    #read in the arrays
    input_data['fpol'] = read_1d(input_data['nw']) #remember input_data['nw'] holds width, input_data['nh'] holds height
    input_data['pres'] = read_1d(input_data['nw'])
    input_data['ffprime'] = read_1d(input_data['nw'])
    input_data['pprime'] = read_1d(input_data['nw'])
    input_data['psirz'] = read_2d(input_data['nw'],input_data['nh'])
    input_data['qpsi'] = read_1d(input_data['nw'])

    #now deal with boundaries
    input_data['nbbbs'] = int(get_next(token))
    input_data['limitr'] = int(get_next(token))

    def read_bndy(nb,nl): #number of boundaries and limiters
        if nb > 0: #read in boundaries
            rb = np.zeros(nb)
            zb = np.zeros(nb)
            for i in np.arange(nb):
                rb[i] = float(get_next(token)) #read in R,Z pairs
                zb[i] = float(get_next(token))
        else:
            rb = [0]
            zb = [0]
    
        if nl > 0: #read in limiters
            rl = np.zeros(nl)
            zl = np.zeros(nl)
            for i in np.arange(nl):
                rl[i] = float(get_next(token))
                zl[i] = float(get_next(token))
        else:
            rl = [0]
            zl = [0]

        return rb,zb,rl,zl

    input_data['rbbbs'],input_data['zbbbs'],input_data['rlim'],input_data['zlim'] = read_bndy(input_data['nbbbs'],input_data['limitr'])
    flags['loaded'] = True
    
    return input_data



def dump_equilibrium_GEQDSK(output_data,output_filepath):
    """
    generic function for writing G-EQDSK-formatted data to file

    notes:
        originally written by Ben Dudson and edited by Nick Walkden
        does not write out idum

        see README.md for data key
    """

    cnt = itertools.cycle([0,1,2,3,4]) #counter

    def write_number(file,number,counter):
        if number < 0:
            seperator = "-"
            number = np.abs(number)
        else:
            seperator = " "
        if get_next(counter) == 4:
            last = "\n"
        else:
            last = ""
        
        string = '%.10E'%number
        #mant,exp = string.split('E')
        file.write(seperator+string+last)

    def write_1d(file,array,counter):
        for num in array:
            write_number(file,num,counter)

    def write_2d(file,array,counter):
        nx = array.shape[0]
        for i in np.arange(nx):
            write_1d(file,array[i],counter)
    
    def write_bndry(file,R,Z,counter):
        for i in np.arange(len(list(R))):
            write_number(file,R[i],counter)
            write_number(file,Z[i],counter)
        file.write("\n")
    
    with open(output_filepath,'w') as file:
        line = " LOCUST_IO "+time.strftime("%d/%m/%Y")+" # 0 0 "+str(output_data['nw'])+" "+str(output_data['nh'])+"\n"
        file.write(line)

        float_keys = [
        'rdim','zdim','rcentr','rleft','zmid',
        'rmaxis','zmaxis','simag','sibry','bcentr',
        'current','simag','xdum','rmaxis','xdum',
        'zmaxis','xdum','sibry','xdum','xdum']
        for key in float_keys:
            write_number(file,output_data[key],cnt)

        write_1d(file,output_data['fpol'],cnt)
        write_1d(file,output_data['pres'],cnt)
        write_1d(file,output_data['ffprime'],cnt)
        write_1d(file,output_data['pprime'],cnt)
        write_2d(file,output_data['psirz'],cnt)    
        write_1d(file,output_data['qpsi'],cnt) 
        
        file.write("\n"+str(len(list(output_data['rbbbs'])))+"\t"+str(len(list(output_data['rlim'])))+"\n")
        write_bndry(file,output_data['rbbbs'],output_data['zbbbs'],cnt)
        write_bndry(file,output_data['rlim'],output_data['zlim'],cnt)


def read_equilibrium_IDS(shot,run): 
    """
    reads relevant LOCUST equilibrium data from an equilibrium IDS and returns as a dictionary

    notes:
        idum not read
        see README.md for data key
    """

    input_IDS=imas.ids(shot,run) #initialise new blank IDS
    input_IDS.open()
    input_IDS.equilibrium.get() #open the file and get all the data from it

    input_data = {} #initialise blank dictionary to hold the data

    #pull out easy things - 0D data, profiles etc which map straight over
    input_data['rcentr']=input_IDS.equilibrium.vacuum_toroidal_field.r0 
    #input_data['bcentr']=input_IDS.equilibrium.vacuum_toroidal_field.b0 #XXX this doesn't currently work - supposed to be 1D?
    input_data['rmaxis']=input_IDS.equilibrium.time_slice[0].global_quantities.magnetic_axis.r
    input_data['zmaxis']=input_IDS.equilibrium.time_slice[0].global_quantities.magnetic_axis.z
    input_data['simag']=input_IDS.equilibrium.time_slice[0].global_quantities.psi_axis
    input_data['sibry']=input_IDS.equilibrium.time_slice[0].global_quantities.psi_boundary
    input_data['current']=input_IDS.equilibrium.time_slice[0].global_quantities.ip
    input_data['psirz']=input_IDS.equilibrium.time_slice[0].profiles_2d[0].psi
    
    input_data['rlim']=input_IDS.equilibrium.time_slice[0].boundary.outline.r #boundaries
    input_data['zlim']=input_IDS.equilibrium.time_slice[0].boundary.outline.z
    input_data['rbbbs']=input_IDS.equilibrium.time_slice[0].boundary.lcfs.r #NOTE this is apparently obsolete - need to figure out where to write to 
    input_data['zbbbs']=input_IDS.equilibrium.time_slice[0].boundary.lcfs.z

    input_data['fpol'] =input_IDS.equilibrium.time_slice[0].profiles_1d.f #flux grid data
    input_data['pres'] =input_IDS.equilibrium.time_slice[0].profiles_1d.pressure
    input_data['ffprime']=input_IDS.equilibrium.time_slice[0].profiles_1d.f_df_dpsi
    input_data['pprime'] =input_IDS.equilibrium.time_slice[0].profiles_1d.dpressure_dpsi
    input_data['qpsi'] =input_IDS.equilibrium.time_slice[0].profiles_1d.q

    #values derived from grids and profiles
    psi_1D=input_IDS.equilibrium.time_slice[0].profiles_1d.psi 
    simag=min(psi_1D)
    sibry=max(psi_1D)

    input_data['limitr']=len(input_IDS.equilibrium.time_slice[0].boundary.outline.z)
    input_data['nbbbs']=len(input_IDS.equilibrium.time_slice[0].boundary.lcfs.z)

    R_1D=input_IDS.equilibrium.time_slice[0].profiles_2d[0].grid.dim1 #dim1=R values/dim2=Z values
    Z_1D=input_IDS.equilibrium.time_slice[0].profiles_2d[0].grid.dim2

    input_data['nw']=len(R_1D)
    input_data['nh']=len(Z_1D)
    input_data['rleft']=min(R_1D)
    input_data['rdim']=abs(max(R_1D)-min(R_1D))
    input_data['zdim']=abs(max(Z_1D)-min(Z_1D))
    input_data['zmid']=0.5*(max(Z_1D)+min(Z_1D))

    input_IDS.close()

    return input_data


def dump_equilibrium_IDS(ID,output_data,shot,run):
    """
    writes relevant LOCUST equilibrium data to an equilibrium IDS

    notes:
        currently only for rectangular equilibria 
        currently overwrites pre-existing IDSs
        idum not dumped

        see README.md for output_data key
    """

    output_IDS=imas.ids(shot,run) 
    output_IDS.create() #this will overwrite any existing IDS for this shot/run

    #write out code properties
    output_IDS.equilibrium.ids_properties.comment=ID #write out identification
    output_IDS.equilibrium.code.name="LOCUST_IO"
    output_IDS.equilibrium.code.version=support.LOCUST_IO_version
    output_IDS.equilibrium.ids_properties.homoegeneous_time=0   #must set homogeneous_time variable

    #add a time_slice and set the time of this slice
    output_IDS.equilibrium.time_slice.resize(1) #just add one time_slice i.e. static equilibrium
    output_IDS.equilibrium.time_slice[0].time=0.0

    #write out the easy stuff - global quantities, some 1D profiles and the boundaries
    output_IDS.equilibrium.vacuum_toroidal_field.r0=output_data['rcentr'] 
    #output_IDS.equilibrium.vacuum_toroidal_field.b0=output_data['bcentr'] #XXX this doesn't currently work - supposed to be 1D? #XXX TRYING THIS NEXT - output_IDS.equilibrium.time=np.array([0.0,1.0,2.0]) set b to same dimension
    output_IDS.equilibrium.time_slice[0].global_quantities.magnetic_axis.r=output_data['rmaxis']   
    output_IDS.equilibrium.time_slice[0].global_quantities.magnetic_axis.z=output_data['zmaxis']    
    output_IDS.equilibrium.time_slice[0].global_quantities.psi_axis=output_data['simag']  
    output_IDS.equilibrium.time_slice[0].global_quantities.psi_boundary=output_data['sibry']    
    output_IDS.equilibrium.time_slice[0].global_quantities.ip=output_data['current']

    output_IDS.equilibrium.time_slice[0].boundary.type=0 #boundary type (0 for limiter, 1 for diverted)
    output_IDS.equilibrium.time_slice[0].boundary.outline.r=output_data['rlim'] 
    output_IDS.equilibrium.time_slice[0].boundary.outline.z=output_data['zlim']
    output_IDS.equilibrium.time_slice[0].boundary.lcfs.r=output_data['rbbbs'] #NOTE this is apparently obsolete - need to figure out where to write to 
    output_IDS.equilibrium.time_slice[0].boundary.lcfs.z=output_data['zbbbs']

    #now to define the grids, start with the uniform flux grid
    psi_1D=np.linspace(output_data['simag'],output_data['sibry'],len(output_data['ffprime'])) #use any of fpol, pres, ffprime, pprime, qpsi for final linspace field - they're all the same length

    #write out the uniform flux grid output_data
    output_IDS.equilibrium.time_slice[0].profiles_1d.psi=psi_1D
    output_IDS.equilibrium.time_slice[0].profiles_1d.f=output_data['fpol'] 
    output_IDS.equilibrium.time_slice[0].profiles_1d.pressure=output_data['pres'] 
    output_IDS.equilibrium.time_slice[0].profiles_1d.f_df_dpsi=output_data['ffprime'] 
    output_IDS.equilibrium.time_slice[0].profiles_1d.dpressure_dpsi=output_data['pprime'] 
    output_IDS.equilibrium.time_slice[0].profiles_1d.q=output_data['qpsi'] 

    #now define the R,Z simulation grid
    output_IDS.equilibrium.time_slice[0].profiles_2d.resize(1) #add an element onto the profiles_2d struct_array to define this grid
    output_IDS.equilibrium.time_slice[0].profiles_2d[0].grid_type.name='rectangular grid' #add some identifiers for this particular grid
    output_IDS.equilibrium.time_slice[0].profiles_2d[0].grid_type.description='grid handled with GEQDSK/LOCUST_IO' 
    output_IDS.equilibrium.time_slice[0].profiles_2d[0].grid_type.index=1 #1 for rectangular (R,z), 0 for inverse (psi,theta)

    #generate the R,Z grid coordinate arrays
    R_1D=np.linspace(output_data['rleft'],output_data['rleft']+output_data['rdim'],num=output_data['nw']) #generate 1D arrays of the R,z values  TODO do this upon writing in instaed of here     
    Z_1D=np.linspace(output_data['zmid']-0.5*output_data['zdim'],output_data['zmid']+0.5*output_data['zdim'],num=output_data['nh']) 
    R_2D,Z_2D=np.meshgrid(R_1D,Z_1D) #generate 2D arrays of R,Z values

    #write out R,Z grid coordinate arrays
    output_IDS.equilibrium.time_slice[0].profiles_2d[0].grid.dim1=R_1D #dim1=R values/dim2=Z values
    output_IDS.equilibrium.time_slice[0].profiles_2d[0].grid.dim2=Z_1D
    output_IDS.equilibrium.time_slice[0].profiles_2d[0].r=R_2D
    output_IDS.equilibrium.time_slice[0].profiles_2d[0].z=Z_2D
    
    #write out 2D profiles
    output_IDS.equilibrium.time_slice[0].profiles_2d[0].psi=output_data['psirz'] 
    
    #'put' all the output_data into the file and close
    output_IDS.equilibrium.put()
    output_IDS.close()


################################################################## Equilibrium class

class Equilibrium(LOCUST_input):
    """
    class describing the equilibrium input for LOCUST

    inherited from LOCUST_input:
        self.ID                     unique object identifier, good convention to fill these for error handling etc
        self.data                   holds all input data in dictionary object
        self.LOCUST_input_type      string which holds this class' input type, this case = 'equilibrium'
    class data
        self.input_filename         name of file in input_files folder
        self.data_format            data format of original data e.g. GEQDSK
        self.input_filepath         full path of file in input_files folder  
        self.shot                   shot number
        self.run                    run number
        self.properties             data to hold additional class-specific information e.g. ion species in Temperature
        key, value                  key for data dictionary to specify data entry holding value
        target                      external object to copy from
        output_filename             name of file to write to
        output_filepath             full path to output file in output_files folder

    notes:

    """

    LOCUST_input_type='equilibrium'

    def __getitem__(self,key):
        """
        function so can access member data via []        
        """
        return self.data[key]

    def __setitem__(self,key,value):
        """
        function so can access member data via []
        """
        self.data[key]=value

    def read_data(self,data_format=None,input_filename=None,shot=None,run=None,properties=None): #always supply all possible arguments for reading in data, irrespective of read in type
        """
        read equilibrium from file 

        notes:
        """

        if none_check(self.ID,self.LOCUST_input_type,'cannot read_data - data_format required\n',data_format): #must always have data_format if reading in data
            pass

        elif data_format=='GEQDSK': #here are the blocks for various file types, they all follow the same pattern
            if not none_check(self.ID,self.LOCUST_input_type,'cannot read_data from GEQDSK - input_filename required\n',input_filename): #check we have all info for reading GEQDSKs
                self.data_format=data_format #add to the member data
                self.input_filename=input_filename
                self.input_filepath=support.dir_input_files+input_filename
                self.properties=properties
                self.data=read_equilibrium_GEQDSK(self.input_filepath) #read the file
           
        elif data_format=='IDS':
            if not none_check(self.ID,self.LOCUST_input_type,'cannot read_data from equilibrium IDS - shot and run data required\n',shot,run):
                self.data_format=data_format
                self.shot=shot
                self.run=run
                self.properties=properties
                self.data=read_equilibrium_IDS(self.shot,self.run)

        else:
            print("cannot read_data - please specify a compatible data_format\n")


    def dump_data(self,data_format=None,output_filename=None,shot=None,run=None):
        """
        write equilibrium to file

        notes: 
        """

        if none_check(self.ID,self.LOCUST_input_type,'dump_data requires self.data and data_format\n',self.data,data_format):
            pass
        
        elif data_format=='GEQDSK':
            if not none_check(self.ID,self.LOCUST_input_type,'cannot dump_data to GEQDSK - output_filename required\n',output_filename):
                output_filepath=support.dir_output_files+output_filename
                dump_equilibrium_GEQDSK(self.data,output_filepath)
        
        elif data_format=='IDS':
            if not none_check(self.ID,self.LOCUST_input_type,'cannot dump_data to equilibrium IDS - shot and run required\n',shot,run):
                dump_equilibrium_IDS(self.ID,self.data,shot,run)

        else:
            print("cannot dump_data - please specify a compatible data_format\n")

    def copy(self,target,*keys):
        """
        copy two equilibrium objects 

        notes:
            if target.data is None or contains Nones then this function does nothing
            if no key supplied then copy all data over
            if key supplied then copy/append dictionary data accordingly

            TODO need some way of editing data_format and input_filename/shot/run after a copy

        usage:
            my_equilibrium.copy(some_other_equilibrium) to copy all data
            my_equilibrium.copy(some_other_equilibrium,'nh','nw','some_other_arg') to copy specific fields
            my_equilibrium.copy(some_other_equilibrium, *some_list_of_args) equally
        """

        if none_check(self.ID,self.LOCUST_input_type,'cannot copy() - target.data is blank\n',target.data): #return warning if any target data contains empty variables
            pass
        elif not keys: #if empty, keys will be false i.e. no key supplied --> copy everything 
            self.data=copy.deepcopy(target.data) #using = with whole dictionary results in copying by reference, so need deepcopy() here
        elif not none_check(self.ID,self.LOCUST_input_type,'cannot copy() - found key containing None\n',*keys): 
            self.set(**{key:target[key] for key in keys}) #call set function and generate the dictionary of **kwargs with list comprehension
    
    def set(self,**kwargs):
        """
        set equilibrium object data 

        usage:
            my_equilibrium.set(nw=5,fpol=[1,2,3,4]) to set multiple values simultaneously
            my_equilibrium.set(**{'nh':100,'nw':200}) equally
        """
        keys=kwargs.keys()
        values=kwargs.values()
        allkeysvalues=keys+values #NOTE can avoid having to do this in python version 3.5
        if none_check(self.ID,self.LOCUST_input_type,'cannot set() - empty key/value pair found\n',*allkeysvalues):
            pass
        else:
            for key,value in zip(keys,values): #loop through kwargs
                self[key]=value





































################################################################## Beam_Deposition functions

def read_beam_depo_ASCII(input_filepath):
    """
    reads neutral beam deposition profile stored in ASCII format - r z phi v_r v_z v_phi
    """


    with open(input_filepath) as file:
        
        lines=file.readlines() #return lines as list
        if not lines: #check to see if the file opened
            raise IOError("ERROR: read_beam_depo_ASCII() cannot read from "+input_filepath)
    
    del(lines[0]) #first two lines are junk
    del(lines[0])

    input_data = {} #initialise the dictionary to hold the data
    input_data['r']=[] #initialise the arrays 
    input_data['z']=[]
    input_data['phi']=[]
    input_data['v_r']=[]
    input_data['v_z']=[]
    input_data['v_phi']=[]

    for line in lines:

        split_line=line.split()
        input_data['r'].append(float(split_line[0]))
        input_data['z'].append(float(split_line[1]))
        input_data['phi'].append(float(split_line[2]))
        input_data['v_r'].append(float(split_line[3]))
        input_data['v_z'].append(float(split_line[4]))
        input_data['v_phi'].append(float(split_line[5]))

    input_data['r']=np.asarray(input_data['r']) #convert to arrays
    input_data['z']=np.asarray(input_data['z'])
    input_data['phi']=np.asarray(input_data['phi'])
    input_data['v_r']=np.asarray(input_data['v_r'])
    input_data['v_z']=np.asarray(input_data['v_z'])
    input_data['v_phi']=np.asarray(input_data['v_phi'])    

    return input_data

def dump_beam_depo_ASCII(output_data,output_filepath):
    """
    writes neutral beam deposition profile to ASCII format - r z phi v_r v_z v_phi
    
    notes:
        writes out two headerlines
    """

    with open(output_filepath,'w') as file: #open file

        file.write('1.0\n') #re-insert junk lines
        file.write('1.0\n')

        for this_particle in range(len(output_data['r'])): #iterate through all particles i.e. length of our dictionary's arrays

            r_out=output_data['r'][this_particle] #briefly set to a temporary variable to improve readability
            z_out=output_data['z'][this_particle]
            phi_out=output_data['phi'][this_particle]
            v_r_out=output_data['v_r'][this_particle]
            v_z_out=output_data['v_z'][this_particle]
            v_phi_out=output_data['v_phi'][this_particle]

            file.write("{r} {z} {phi} {v_r} {v_z} {v_phi}\n".format(r=r_out,z=z_out,phi=phi_out,v_r=v_r_out,v_z=v_z_out,v_phi=v_phi_out))


def read_beam_depo_IDS(shot,run):
    """
    reads relevant LOCUST neutral beam data from a distribution_sources IDS and returns as a dictionary

    notes:
        see README.md for data key
    """

    input_IDS=imas.ids(shot,run) #initialise new blank IDS
    input_IDS.open()
    input_IDS.distribution_sources.get() #open the file and get all the data from it

    #extract the 2D positions array
    positions=input_IDS.distribution_sources.source[0].markers[0].positions #assume everything is stored in the first source, and first marker type

    input_data = {} #initialise blank dictionary to hold the data
    input_data['r']=positions[:,0]
    input_data['z']=positions[:,1]
    input_data['phi']=positions[:,2]
    input_data['v_r']=positions[:,3]
    input_data['v_z']=positions[:,4]
    input_data['v_phi']=positions[:,5]

    input_IDS.close()

    return input_data

def dump_beam_depo_IDS(ID,output_data,shot,run):
    """
    writes relevant LOCUST neutral beam data to a distribution_sources IDS

    """

    output_IDS=imas.ids(shot,run) 
    output_IDS.create() #this will overwrite any existing IDS for this shot/run

    #write out code properties
    output_IDS.distribution_sources.ids_properties.comment=ID #write out identification
    output_IDS.distribution_sources.code.name="LOCUST_IO"
    output_IDS.distribution_sources.code.version=support.LOCUST_IO_version
    output_IDS.distribution_sources.ids_properties.homoegeneous_time=0   #must set homogeneous_time variable
    
    #add a type of source and add a time_slice for this source
    output_IDS.distribution_sources.source.resize(1) #adds a type of source here
    output_IDS.distribution_sources.source[0].markers.resize(1) #adds a time_slice here    
    output_IDS.distribution_sources.source[0].markers[0].time=0.0 #set the time of this time_slice

    #add definition of our coordinate basis - r,z,phi,v_r,v_z,v_phi in this case
    output_IDS.distribution_sources.source[0].markers[0].coordinate_identifier.resize(1)
    output_IDS.distribution_sources.source[0].markers[0].coordinate_identifier[0].name='r, z, phi' #add some description here
    output_IDS.distribution_sources.source[0].markers[0].coordinate_identifier[0].index=0 #set arbitrarily here
    output_IDS.distribution_sources.source[0].markers[0].coordinate_identifier[0].description='r, z, phi, v_r, v_z, v_phi coordinate system'
    
    #start storing particle data
    output_IDS.distribution_sources.source[0].markers[0].weights=np.ones(len(output_data['r'])) #define the weights, i.e. number of particles per marker 
    positions=np.array([output_data['r'],output_data['z'],output_data['phi'],output_data['v_r'],output_data['v_z'],output_data['v_phi']]) #create 2D array of positions
    output_IDS.distribution_sources.source[0].markers[0].positions=np.transpose(positions) #swap the indices due to data dictionary convention

    #'put' all the output_data into the file and close
    output_IDS.distribution_sources.put()
    output_IDS.close()

################################################################## Beam_Deposition class

class Beam_Deposition(LOCUST_input):
    """
    class describing neutral beam deposition profile input for LOCUST

    inherited from LOCUST_input:
        self.ID                     unique object identifier, good convention to fill these for error handling etc
        self.data                   holds all input data in dictionary object
        self.LOCUST_input_type      string which holds this class' input type, this case = 'beam_deposition'
    class data
        self.input_filename         name of file in input_files folder
        self.data_format            data format of original data e.g. ASCII
        self.input_filepath         full path of file in input_files folder  
        self.shot                   shot number
        self.run                    run number
        self.properties             data to hold additional class-specific information e.g. ion species in Temperature
        key, value                  key for data dictionary to specify data entry holding value
        target                      external object to copy from
        output_filename             name of file to write to
        output_filepath             full path to output file in output_files folder

    notes:
        data is stored such that the coordinate 'r' for all particles is stored in this_beam_depo['r']
        therefore the phase space position of particle p is:
            (this_beam_depo['r'][p], this_beam_depo['z'][p], this_beam_depo['phi'][p], this_beam_depo['v_r'][p], this_beam_depo['v_z'][p], this_beam_depo['v_phi'][p])
    """

    LOCUST_input_type='beam_deposition' 

    def __getitem__(self,key):

        return self.data[key]

    def __setitem__(self,key,value):

        self.data[key]=value

    def read_data(self,data_format=None,input_filename=None,shot=None,run=None,properties=None): 
        """
        read beam_deposition from file 

        notes:
        """

        if none_check(self.ID,self.LOCUST_input_type,'cannot read_data - data_format required\n',data_format): #must always have data_format if reading in data
            pass

        elif data_format=='ASCII': #here are the blocks for various file types, they all follow the same pattern
            if not none_check(self.ID,self.LOCUST_input_type,'cannot read_data from ASCII - input_filename required\n',input_filename): #must check we have all info required for reading GEQDSKs

                self.data_format=data_format #add to the member data
                self.input_filename=input_filename
                self.input_filepath=support.dir_input_files+input_filename
                self.properties=properties
                self.data=read_beam_depo_ASCII(self.input_filepath) #read the file
        
        elif data_format=='IDS':
            if not none_check(self.ID,self.LOCUST_input_type,'cannot read_data from distribution_sources IDS - shot and run data required\n',shot,run):

                self.data_format=data_format
                self.shot=shot
                self.run=run
                self.properties=properties
                self.data=read_beam_depo_IDS(self.shot,self.run)

        else:
            print("cannot read_data - please specify a compatible data_format\n")            

    def dump_data(self,data_format=None,output_filename=None,shot=None,run=None):
        """
        write beam_deposition to file

        notes: 
        """

        if none_check(self.ID,self.LOCUST_input_type,'cannot dump_data - self.data and data_format required\n',self.data,data_format):
            pass
        
        elif data_format=='ASCII':
            if not none_check(self.ID,self.LOCUST_input_type,'cannot dump_data to ASCII - output_filename required\n',output_filename):
                output_filepath=support.dir_output_files+output_filename
                dump_beam_depo_ASCII(self.data,output_filepath)
        
        elif data_format=='IDS':
            if not none_check(self.ID,self.LOCUST_input_type,'cannot dump_data to distribution_sources IDS - shot and run required\n',shot,run):
                dump_beam_depo_IDS(self.ID,self.data,shot,run)

        else:
            print("cannot dump_data - please specify a known data_format (ASCII/IDS)\n")

    def copy(self,target,*keys):
        """
        copy two beam_deposition objects 

        notes:
            if target.data is None or contains Nones then this function does nothing
            if no key supplied then copy all data over
            if key supplied then copy/append dictionary data accordingly

            TODO need some way of editing data_format and input_filename/shot/run after a copy

        usage:
            my_beam_deposition.copy(some_other_beam_deposition) to copy all data
            my_beam_deposition.copy(some_other_beam_deposition,'some_arg','some_other_arg') to copy specific fields
            my_beam_deposition.copy(some_other_beam_deposition, *some_list_of_args) equally
        """

        if none_check(self.ID,self.LOCUST_input_type,'cannot copy() - target.data is blank\n',target.data): #return warning if any target data contains empty variables
            pass
        elif not keys: #if empty, keys will be false i.e. no key supplied --> copy everything 
            self.data=copy.deepcopy(target.data) #using = with whole dictionary results in copying by reference, so need deepcopy() here
        elif not none_check(self.ID,self.LOCUST_input_type,'cannot copy() - found key containing None\n',*keys): 
            self.set(**{key:target[key] for key in keys}) #call set function and generate the dictionary of **kwargs with list comprehension
    
    def set(self,**kwargs):
        """
        set beam_deposition object data 

        usage:
            my_beam_deposition.set(some_arg=5,some_other_arg=[1,2,3,4]) to set multiple values simultaneously
            my_beam_deposition.set(**{'some_arg':100,'some_other_arg':200}) equally
        """
        keys=kwargs.keys()
        values=kwargs.values()
        allkeysvalues=keys+values #NOTE can avoid having to do this in python version 3.5
        if none_check(self.ID,self.LOCUST_input_type,'cannot set() - empty key/value pair found\n',*allkeysvalues):
            pass
        else:
            for key,value in zip(keys,values): #loop through kwargs
                self[key]=value








































'''



################################################################## Temperature functions

def read_temperature_ASCII(input_filepath):
    """
    reads temperature profile stored in ASCII format - psi T(ev)
    """

    with open(input_filepath) as file:
        
        lines=file.readlines() #return lines as list
        if not lines: #check to see if the file opened
            raise IOError("ERROR: read_temperature_ASCII() cannot read from "+input_filepath)
    
    number_data_points=lines[0] #first line contains the number of points
    del(lines[0])

    input_data = {} #initialise the dictionary to hold the data
    input_data['psi']=[] #initialise the arrays 
    input_data['T']=[]

    for line in lines:

        split_line=line.split()
        input_data['psi'].append(float(split_line[0]))
        input_data['T'].append(float(split_line[1]))

    input_data['psi']=np.asarray(input_data['psi']) #convert to arrays
    input_data['T']=np.asarray(input_data['T'])
   
    return input_data

def dump_temperature_ASCII(output_data,output_filepath):
    """
    writes temperature profile to ASCII format - psi T(ev)    
    
    notes:
        writes out a headerline for length of file
    """

    with open(output_filepath,'w') as file: #open file

        file.write(len(output_data['psi'])) #re-insert line containing length
        file.write('\n')

        for point in range(len(output_data['psi'])): #iterate through all points i.e. length of our dictionary's arrays

            psi_out=output_data['psi'][point] #briefly set to a temporary variable to improve readability
            T_out=output_data['T'][point]
            
            file.write("{psi} {T}\n".format(psi=psi_out,T=T_out))


def read_temperature_IDS(shot,run,properties):
    """
    reads relevant LOCUST temperature data from a core_profiles IDS and returns as a dictionary

    notes:
        see README.md for data key
    """

    input_IDS=imas.ids(shot,run) #initialise new blank IDS
    input_IDS.open()
    input_IDS.core_profiles.get() #open the file and get all the data from it

    input_data = {} #initialise blank dictionary to hold the data
    input_data['psi']=input_IDS.core_profiles.profiles_1d[0].grid.psi

    #read in temperature depending on species
    if properties=='electrons':
        input_data['T']=input_IDS.core_profiles.profiles_1d[0].electrons.temeprature        
    elif properties=='ions':
        input_data['T']=input_IDS.core_profiles.profiles_1d[0].ion[0].temperature 
    else:
        print("cannot read_temperature_IDS - Temperature.properties must be set to 'electrons' or 'ions'\n")

    input_IDS.close()

    return input_data

def dump_temperature_IDS(ID,output_data,shot,run,properties):
    """
    writes relevant LOCUST temperature data to a core_profiles IDS
    """

    output_IDS=imas.ids(shot,run) 
    output_IDS.create() #this will overwrite any existing IDS for this shot/run

    #write out code properties
    output_IDS.core_profiles.ids_properties.comment=ID #write out identification
    output_IDS.core_profiles.code.name="LOCUST_IO"
    output_IDS.core_profiles.code.version=support.LOCUST_IO_version
    output_IDS.core_profiles.ids_properties.homoegeneous_time=0   #must set homogeneous_time variable
    
    #add a time_slice and set the time
    output_IDS.core_profiles.profiles_1d.resize(1) #add a time_slice
    output_IDS.core_profiles.profiles_1d.time=0.0 #set the time of the time_slice
    output_IDS.core_profiles.profiles_1d[0].grid.psi=output_data['psi']

    #write out temperature depending on species
    if properties=='electrons':
        output_IDS.core_profiles.profiles_1d[0].electrons.temeprature=output_data['T']        
    elif properties=='ions':
        output_IDS.core_profiles.profiles_1d[0].ion.resize(1) #add an ion species 
        #TODO need to add additional species data here e.g. mass, charge
        output_IDS.core_profiles.profiles_1d[0].ion[0].temperature=output_data['T']
    else:
        print("cannot dump_temperature_IDS - Temperature.properties must be set to 'electrons' or 'ions'\n")

    #'put' all the output_data into the file and close
    output_IDS.core_profiles.put()
    output_IDS.close()

'''

################################################################## Temperature class

class Temperature(LOCUST_input):
    """
    class describing temperature profile input for LOCUST

    inherited from LOCUST_input:
        self.ID                     unique object identifier, good convention to fill these for error handling etc
        self.data                   holds all input data in dictionary object
        self.LOCUST_input_type      string which holds this class' input type, this case = 'temperature'
    class data
        self.input_filename         name of file in input_files folder
        self.data_format            data format of original data e.g. ASCII
        self.input_filepath         full path of file in input_files folder  
        self.shot                   shot number
        self.run                    run number
        self.properties             data to hold additional class-specific information e.g. ion species in Temperature
        key, value                  key for data dictionary to specify data entry holding value
        target                      external object to copy from
        output_filename             name of file to write to
        output_filepath             full path to output file in output_files folder

    notes:
        data is stored such that a reading of temperature at psi coordinate 'coord' is:
            this_temperature['psi'][coord], this_temperature['T'][coord]
    """

    LOCUST_input_type='temperature' 

    def __getitem__(self,key):

        return self.data[key]

    def __setitem__(self,key,value):

        self.data[key]=value

    def read_data(self,data_format=None,input_filename=None,shot=None,run=None,properties=None):
        """
        read temperature from file 

        notes:
        """

        if none_check(self.ID,self.LOCUST_input_type,'cannot read_data - data_format required\n',data_format): #must always have data_format if reading in data
            pass

        elif data_format=='ASCII': #here are the blocks for various file types, they all follow the same pattern
            if not none_check(self.ID,self.LOCUST_input_type,'cannot read_data from ASCII - input_filename required\n',input_filename): #must check we have all info required for reading GEQDSKs

                self.data_format=data_format #add to the member data
                self.input_filename=input_filename
                self.input_filepath=support.dir_input_files+input_filename
                self.properties=properties
                self.data=read_temperature_ASCII(self.input_filepath) #read the file
        
        elif data_format=='IDS':
            if not none_check(self.ID,self.LOCUST_input_type,'cannot read_data from core_profiles IDS - shot, run and ion species property required\n',shot,run,properties):

                self.data_format=data_format
                self.shot=shot
                self.run=run
                self.properties=properties
                self.data=read_temperature_IDS(self.shot,self.run,self.properties)

        else:
            print("cannot read_data - please specify a compatible data_format\n")            

    def dump_data(self,data_format=None,output_filename=None,shot=None,run=None):
        """
        write temperature to file

        notes: 
        """

        if none_check(self.ID,self.LOCUST_input_type,'cannot dump_data - self.data and data_format required\n',self.data,data_format):
            pass
        
        elif data_format=='ASCII':
            if not none_check(self.ID,self.LOCUST_input_type,'cannot dump_data to ASCII - output_filename required\n',output_filename):
                output_filepath=support.dir_output_files+output_filename
                dump_temperature_ASCII(self.data,output_filepath)
        
        elif data_format=='IDS':
            if not none_check(self.ID,self.LOCUST_input_type,'cannot dump_data to core_profiles IDS - shot, run and ion species property required\n',shot,run,self.properties):
                dump_temperature_IDS(self.ID,self.data,shot,run,self.properties)

        else:
            print("cannot dump_data - please specify a known data_format (ASCII/IDS)\n")

    def copy(self,target,*keys):
        """
        copy two temperature objects 

        notes:
            if target.data is None or contains Nones then this function does nothing
            if no key supplied then copy all data over
            if key supplied then copy/append dictionary data accordingly

            TODO need some way of editing data_format and input_filename/shot/run after a copy

        usage:
            my_temperature.copy(some_other_temperature) to copy all data
            my_temperature.copy(some_other_temperature,'some_arg','some_other_arg') to copy specific fields
            my_temperature.copy(some_other_temperature, *some_list_of_args) equally
        """

        if none_check(self.ID,self.LOCUST_input_type,'cannot copy() - target.data is blank\n',target.data): #return warning if any target data contains empty variables
            pass
        elif not keys: #if empty, keys will be false i.e. no key supplied --> copy everything 
            self.data=copy.deepcopy(target.data) #using = with whole dictionary results in copying by reference, so need deepcopy() here
        elif not none_check(self.ID,self.LOCUST_input_type,'cannot copy() - found key containing None\n',*keys): 
            self.set(**{key:target[key] for key in keys}) #call set function and generate the dictionary of **kwargs with list comprehension
    
    def set(self,**kwargs):
        """
        set temperature object data 

        usage:
            my_temperature.set(some_arg=5,some_other_arg=[1,2,3,4]) to set multiple values simultaneously
            my_temperature.set(**{'some_arg':100,'some_other_arg':200}) equally
        """
        keys=kwargs.keys()
        values=kwargs.values()
        allkeysvalues=keys+values #NOTE can avoid having to do this in python version 3.5
        if none_check(self.ID,self.LOCUST_input_type,'cannot set() - empty key/value pair found\n',*allkeysvalues):
            pass
        else:
            for key,value in zip(keys,values): #loop through kwargs
                self[key]=value













'''














#################################
class Number_Density(LOCUST_input): write to core_profiles IDS
    """
    class describing particle number density as a function of Psi input for LOCUST
    """
    class_level_attribute=attribute_here 

    def __init__(self,*args,**kwargs):
        instance data, methods etc
    def __enter__(self,*args,**kwargs):
        some_things
    def __exit__(self,*args,**kwargs):
        some_things
    def class_methods(self,*args,**kwargs):
        some_things




#################################
class Collisions(LOCUST_input):
    """
    class describing collision data input for LOCUST
    """
    class_level_attribute=attribute_here 

    def __init__(self,*args,**kwargs):
        instance data, methods etc
    def __enter__(self,*args,**kwargs):
        some_things
    def __exit__(self,*args,**kwargs):
        some_things
    def class_methods(self,*args,**kwargs):
        some_things




























#NOTE post-processing IDL script for LOCUST to be re-written in Python?


pro locust_orplot

device, decompose=0

file    = '/tmp/sward/locust.AUG/OutputFiles/ORBIT.dat'

n       = 0L
npoints = 0

SPAWN, 'tail -1 '+file, STR, /SH

m       = fix(STR[0],type=3)

openr, 1, file

readf, 1, n

DAT = fltarr(n,3,m)
DUM = fltarr(n,3)

for i=0,m-1 do begin
    readf, 1, DUM

    DAT[*,*,i]=DUM
endfor

close, 1

i = where(DAT[*,0,*] gt 0.0)

!X.range=[min(DAT[*,0,*]),max(DAT[*,0,*])]
!Y.range=[min(DAT[*,2,*]),max(DAT[*,2,*])]

plot, [0.,1.], [0.,1.], /iso, /nodata, xtitle='R [m]', ytitle='Z [m]'

for i=0,n-1 do begin
    j = where( (DAT[i,0,*] eq SHIFT(DAT[i,0,*],-1)) and                       $
               (DAT[i,1,*] eq SHIFT(DAT[i,1,*],-1)) and                       $
               (DAT[i,2,*] eq SHIFT(DAT[i,2,*],-1)) ) & j=j[0]

;-  CHECK THIS FOR ORBITS THAT WORKED....

    if( j eq -1 )then j = m-1

    print, DAT[i,0,0], DAT[i,0,j], j

    npoints = npoints + j+1
    print, i, npoints
    oplot, DAT[i,0,0:j], DAT[i,2,0:j], color=7*16-1
endfor

COL  = fltarr(npoints)
COL2 = fltarr(npoints)

openW,  1, '/tmp/sward/ORBITS.vtk'
printF, 1, '# vtk DataFile Version 2.0'
printF, 1, 'Unstructured Grid ORBIT data'
printF, 1, 'ASCII'
printF, 1, 'DATASET UNSTRUCTURED_GRID'
printF, 1, 'POINTS '+strcompress(string(npoints),/re)+' float'

for i=0,n-1 do begin

    j = where( (DAT[i,0,*] eq SHIFT(DAT[i,0,*],-1)) and                       $
               (DAT[i,1,*] eq SHIFT(DAT[i,1,*],-1)) and                       $
               (DAT[i,2,*] eq SHIFT(DAT[i,2,*],-1)) ) & j=j[0]

;- CHECK

    if( j eq -1 )then j=m-1


    for k=0,j do begin
        printF, 1, DAT[i,0,k]*cos(DAT[i,1,k]), DAT[i,0,k]*sin(DAT[i,1,k]),    $
                   DAT[i,2,k]
    endfor
endfor

printF, 1, 'CELLS '+strcompress(string(n),/re)+' '+                           $
                    strcompress(string(npoints+n),/re)
ioff = 0

for i=0,n-1 do begin

    j = where( (DAT[i,0,*] eq SHIFT(DAT[i,0,*],-1)) and                       $
               (DAT[i,1,*] eq SHIFT(DAT[i,1,*],-1)) and                       $
               (DAT[i,2,*] eq SHIFT(DAT[i,2,*],-1)) ) & j=j[0]
;- CHECK

    if( j eq -1 )then j=m-1

    printF, 1, j+1, indgen(j+1)+ioff
    COL [indgen(j+1)+ioff] = findgen(j+1) + 1
    COL2[indgen(j+1)+ioff] = DAT[i,0,0]
    ioff = ioff + j+1
endfor

printF, 1, 'CELL_TYPES '+strcompress(string(n),/re)

for i=0,n-1 do begin
    printF, 1, 4
endfor

printF, 1, 'POINT_DATA '+strcompress(string(npoints),/re)
printF, 1, 'SCALARS INDX float 2'
printF, 1, 'LOOKUP_TABLE default'

for i=0,n_elements(COL)-1 do begin
    printF, 1, COL[i], COL2[i]
endfor

close, 1

stop
end

'''

#################################

##################################################################

###################################################################################################
