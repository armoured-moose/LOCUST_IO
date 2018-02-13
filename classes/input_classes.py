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
 
 
np.set_printoptions(precision=5,threshold=5) #set printing style of numpy arrays
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
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
     
def dict_set(data,**kwargs):
    """
    generalised function (based upon safe_set) to set values in dictionary 'data' after checking source data exists 

    usage:
        dict_set(data,some_key=some_source,some_other_key=[1,2,3,4]) to set multiple values simultaneously
        dict_set(data,**{'some_key':100,'some_other_key':200}) equally
    """
    keys=kwargs.keys()
    values=kwargs.values()
    
    for key,value in zip(keys,values): #loop through kwargs
        if key is not None and value is not None: 
            data[key]=value

def safe_set(target,source):
    """
    generalised function to set a target value to source if it exists
    
    """
    if source is not None:
        target=source

 
 
 
 






















 
 
 
 
 
 
################################################################## Base class
 
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
        if not none_check(self.ID,self.LOCUST_input_type,"read_data requires data_format, blank input initialised \n",data_format):
            self.read_data(data_format,input_filename,shot,run,properties)
 
    def __getitem__(self,key):
        """
        access member data via []        
        """
        return self.data[key]
 
    def __setitem__(self,key,value):
        """
        access member data via []
        """
        self.data[key]=value

    def read_data(self,data_format=None,input_filename=None,shot=None,run=None,properties=None): #bad practice to change overridden method signatures, so retain all method arguments             
        """
        read data to be overloaded in all children classes
        """

        self.data=None 
 
    def look(self):
        """
        print class information and data
        """

        print("\n-----------------------")
        print("ID - {ID}".format(ID=self.ID))  
        print("Input Type - {LOCUST_input_type}".format(LOCUST_input_type=self.LOCUST_input_type))

        if hasattr(self,'properties'): 
            print("Properties - {properties}".format(properties=self.properties))

        if hasattr(self,'data_format'):
            print("Data Format - {data_format}".format(data_format=self.data_format))
        
        if hasattr(self,'input_filename'):
            print("Input Filename - {input_filename}".format(input_filename=self.input_filename))
        
        if hasattr(self,'shot'):
            print("Shot - {shot}".format(shot=self.shot))
        
        if hasattr(self,'run'):
            print("Run - {run}".format(run=self.run))
        
        print("|")
        print("|")

        if hasattr(self,'data') and self.data:
            for key in self.data:
                if not self.data[key].size==0: #do not print if the data is empty
                    print("{key} - {value}".format(key=key,value=self.data[key]))

        print("-----------------------\n")
 
    def copy(self,target,*keys):
        """
        copy two input objects
 
        notes:
            if target.data is None or contains Nones then this function does nothing
            if no key supplied then copy all data over
            if key supplied then copy/append dictionary data accordingly
  
        usage:
            my_input.copy(some_other_input) to copy all data
            my_input.copy(some_other_input,'some_key','some_other_key') to copy specific fields
            my_input.copy(some_other_input, *some_list_of_args) equally
        """
        if none_check(self.ID,self.LOCUST_input_type,"cannot copy() - target.data is blank\n",target.data): #return warning if any target data contains empty variables
            pass

        elif not keys: #if empty, keys will be false i.e. no key supplied --> copy everything 
            self.data=copy.deepcopy(target.data) #using = with whole dictionary results in copying by reference, so need deepcopy() here
            if hasattr(target,'properties'): #copy properties field
                self.properties=target.properties

        elif not none_check(self.ID,self.LOCUST_input_type,"cannot copy() - found key containing None\n",*keys): 
            self.set(**{key:target[key] for key in keys}) #call set function and generate the dictionary of **kwargs with list comprehension
            if hasattr(target,'properties'): #copy properties field
                self.properties=target.properties
     
    def set(self,**kwargs):
        """
        set input object data 
 
        notes:
            specific to LOCUST_IO classes due to none_check call - see safe_set() for more general function

        usage:
            my_input.set(some_key=5,some_other_key=[1,2,3,4]) to set multiple values simultaneously
            my_input.set(**{'some_key':100,'some_other_key':200}) equally
        """
        keys=kwargs.keys()
        values=kwargs.values()
        allkeysvalues=keys+values #NOTE can avoid having to do this in python version 3.5
        if none_check(self.ID,self.LOCUST_input_type,"cannot set() - empty key/value pair found\n",*allkeysvalues):
            pass
        else:
            for key,value in zip(keys,values): #loop through kwargs
                self[key]=value
 
    def compare(self,target,verbose=False):
        """
        compare two input objects

        notes:
            returns true if all data held by target is also held by self (self can have excess)
            verbose option prints summary of compare results
        """

        data_missing_self=[]
        data_missing_target=[]
        data_different=[]

        for key in target.data: #record fields we do not have that target does
            if not key in self.data:
                data_missing_self.append(key) 
            
            elif self[key].size!=target[key].size: #both contain data but data is different
                data_different.append(key)
            elif not np.allclose(self[key],target[key]): #must check size first before doing np.allclose()
                data_different.append(key)

        for key in self.data: #record fields we have that target does not
            if not key in target.data:
                data_missing_target.append(key) 

        if verbose is True: #if wanting to print summary
            if data_missing_self:
                print("self is missing:")
                print('\n'.join(str(key) for key in data_missing_self)) 
            if data_missing_target:
                print("target is missing:")
                print('\n'.join(str(key) for key in data_missing_target)) 
            if data_different: 
                print("shared different data:")
                print('\n'.join(str(key) for key in data_different))

        if not data_different and not data_missing_self: #if shared data is the same and self all target data 
            return True #self is same as target
        else:
            return False

    def run_check(self,verbose=False):
        """
        checks whether object is ready to run in LOCUST

        notes:
            only checks if correct data is held by object
        """

        missing_data=[]

        if not self.data:
            if verbose is True:
                print("no data:")
            return False

        if self.LOCUST_input_type=='equilibrium':
            for key in support.required_equilibrium:
                if key not in self.data:
                    missing_data.append(key)

        elif self.LOCUST_input_type=='beam_deposition':
            for key in support.required_beam_deposition:            
                if key not in self.data:
                    missing_data.append(key)

        elif self.LOCUST_input_type=='temperature':
            for key in support.required_temperature:
                if key not in self.data:
                    missing_data.append(key)

        elif self.LOCUST_input_type=='number_density':
            for key in support.required_number_density:
                if key not in self.data:
                    missing_data.append(key)
 
        if missing_data: #object is not ready
            if verbose is True: #if wanting to print summary
                print("missing data:")
                print('\n'.join(str(key) for key in missing_data))
            return False
        else:
            return True 
 
 
 
 
 





































 
 
################################################################## Equilibrium functions
 
def read_equilibrium_GEQDSK(input_filepath): 
    """ 
    generic function for reading a G-EQDSK-formatted equilibrium file
 
    notes:
        originally written by Ben Dudson and edited by Nick Walkden
        
 
    """
 
    input_data = {}

    with open(input_filepath,'r') as file: #open file
     
        line = file.readline() #first line should be case, id number and dimensions
        if not line:
            raise IOError("ERROR: read_equilibrium_GEQDSK() cannot read from "+input_filepath)
         
        #extract case, id number and dimensions  
        conts = line.split()    #split by white space (no argument in .split())
        input_data['nh'] = np.asarray(int(conts[-1])) #same as nyefit or height dimension
        input_data['nw'] = np.asarray(int(conts[-2])) #same as nxefit or width dimension
        input_data['idum'] = np.asarray(int(conts[-3]))
        flags = {}
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
            input_data[key] = np.asarray(float(get_next(token))) #get_next(token) always yields just a single value, convert this to numpy array
     
        def read_1d(n): 
            """
            """
            input_data = np.zeros(n) #initialise blank lists
            for i in np.arange(n): #instead of using linspace or something makes a temporary numpy array of dimension n to iterate through
                input_data[i] = float(get_next(token))
            return input_data
     
        def read_2d(nx,ny):
            """
            notes:
                edited this function as it was not consistent with GEQDSK storage format
            """
            input_data = np.zeros((nx,ny))
            for j in np.arange(ny): #same technique here, iterate through one dimension and call read_1d along the other dimension
                input_data[:,j] = read_1d(nx)
            return input_data

        #read in the arrays
        input_data['fpol'] = read_1d(input_data['nw']) #remember input_data['nw'] holds width, input_data['nh'] holds height
        input_data['pres'] = read_1d(input_data['nw'])
        input_data['ffprime'] = read_1d(input_data['nw'])
        input_data['pprime'] = read_1d(input_data['nw'])
        input_data['psirz'] = read_2d(input_data['nw'],input_data['nh'])
        input_data['qpsi'] = read_1d(input_data['nw'])
     
        #now deal with boundaries
        input_data['nbbbs'] = np.asarray(int(get_next(token)))
        input_data['limitr'] = np.asarray(int(get_next(token)))
     
        def read_bndy(nb,nl): #number of boundaries and limiters
            if nb > 0: #read in boundaries
                rb = np.zeros(nb)
                zb = np.zeros(nb)
                for i in np.arange(nb):
                    rb[i] = float(get_next(token)) #read in R,Z pairs
                    zb[i] = float(get_next(token))
            else:
                rb = np.asarray(0,ndlim=0)
                zb = np.asarray(0,ndlim=0)
         
            if nl > 0: #read in limiters
                rl = np.zeros(nl)
                zl = np.zeros(nl)
                for i in np.arange(nl):
                    rl[i] = float(get_next(token))
                    zl[i] = float(get_next(token))
            else:
                rl = np.asarray(0,ndlim=0)
                zl = np.asarray(0,ndlim=0)
     
            return rb,zb,rl,zl
     
        input_data['rbbbs'],input_data['zbbbs'],input_data['rlim'],input_data['zlim'] = read_bndy(input_data['nbbbs'],input_data['limitr'])
        
        #extra derived data
        input_data['R_1D']=np.linspace(input_data['rleft'],input_data['rleft']+input_data['rdim'],num=input_data['nw'])     
        input_data['Z_1D']=np.linspace(input_data['zmid']-0.5*input_data['zdim'],input_data['zmid']+0.5*input_data['zdim'],num=input_data['nh']) 
        input_data['psi_1D']=np.linspace(input_data['simag'],input_data['sibry'],input_data['ffprime'].size) #use any of fpol, pres, ffprime, pprime, qpsi for final linspace field - they're all the same length
    
    return input_data
     
def dump_equilibrium_GEQDSK(output_data,output_filepath):
    """
    generic function for writing G-EQDSK-formatted data to file
 
    notes:
        originally written by Ben Dudson and edited by Nick Walkden
        does not write out idum
 
        
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
        ny = array.shape[1]
        for j in np.arange(ny):
            write_1d(file,array[:,j],counter)
     
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
         
        file.write("\n"+str(len(list(output_data['rbbbs'])))+"\t"+str(len(list(output_data['rlim'])))+"\n") #write out the nbbbs and limitr
        write_bndry(file,output_data['rbbbs'],output_data['zbbbs'],cnt)
        write_bndry(file,output_data['rlim'],output_data['zlim'],cnt)
 
def read_equilibrium_IDS(shot,run): 
    """
    reads relevant LOCUST equilibrium data from an equilibrium IDS and returns as a dictionary
 
    notes:
        idum not read
        
    """
 
    input_IDS=imas.ids(shot,run) #initialise new blank IDS
    input_IDS.open()
    input_IDS.equilibrium.get() #open the file and get all the data from it
 
    input_data = {} #initialise blank dictionary to hold the data
 
    #easy bits
    #0D data
    input_data['rcentr']=np.asarray(input_IDS.equilibrium.vacuum_toroidal_field.r0)
    input_data['bcentr']=np.asarray(input_IDS.equilibrium.vacuum_toroidal_field.b0)
    input_data['rmaxis']=np.asarray(input_IDS.equilibrium.time_slice[0].global_quantities.magnetic_axis.r)
    input_data['zmaxis']=np.asarray(input_IDS.equilibrium.time_slice[0].global_quantities.magnetic_axis.z)
    input_data['simag']=np.asarray(input_IDS.equilibrium.time_slice[0].global_quantities.psi_axis)
    input_data['sibry']=np.asarray(input_IDS.equilibrium.time_slice[0].global_quantities.psi_boundary)
    input_data['current']=np.asarray(input_IDS.equilibrium.time_slice[0].global_quantities.ip)
 
    #1D data
    input_data['fpol']=np.asarray(input_IDS.equilibrium.time_slice[0].profiles_1d.f) #flux grid data
    input_data['pres']=np.asarray(input_IDS.equilibrium.time_slice[0].profiles_1d.pressure)
    input_data['ffprime']=np.asarray(input_IDS.equilibrium.time_slice[0].profiles_1d.f_df_dpsi)
    input_data['pprime']=np.asarray(input_IDS.equilibrium.time_slice[0].profiles_1d.dpressure_dpsi)
    input_data['qpsi']=np.asarray(input_IDS.equilibrium.time_slice[0].profiles_1d.q)
    input_data['rlim']=np.asarray(input_IDS.equilibrium.time_slice[0].boundary.lcfs.r) #boundaries, lcfs is obsolete in latest IMAS
    input_data['zlim']=np.asarray(input_IDS.equilibrium.time_slice[0].boundary.lcfs.z)
    input_data['rbbbs']=np.asarray(input_IDS.equilibrium.time_slice[0].boundary.outline.r) 
    input_data['zbbbs']=np.asarray(input_IDS.equilibrium.time_slice[0].boundary.outline.z)

    #2D data    
    input_data['psirz']=np.asarray(input_IDS.equilibrium.time_slice[0].profiles_2d[0].psi)
 
    #harder bits
    #values derived from grids and profiles
    psi_1D=input_IDS.equilibrium.time_slice[0].profiles_1d.psi  #where simag=min(psi_1D) and sibry=max(psi_1D)
    R_1D=input_IDS.equilibrium.time_slice[0].profiles_2d[0].grid.dim1 #dim1=R values/dim2=Z values
    Z_1D=input_IDS.equilibrium.time_slice[0].profiles_2d[0].grid.dim2
    input_data['psi_1D']=np.asarray(psi_1D)
    input_data['R_1D']=np.asarray(R_1D)
    input_data['Z_1D']=np.asarray(Z_1D)

    #0D data
    input_data['limitr']=np.asarray(len(input_IDS.equilibrium.time_slice[0].boundary.outline.z))
    input_data['nbbbs']=np.asarray(len(input_IDS.equilibrium.time_slice[0].boundary.lcfs.z))
    input_data['nw']=np.asarray(len(R_1D))
    input_data['nh']=np.asarray(len(Z_1D))
    input_data['rleft']=np.asarray(min(R_1D))
    input_data['rdim']=np.asarray(abs(max(R_1D)-min(R_1D)))
    input_data['zdim']=np.asarray(abs(max(Z_1D)-min(Z_1D)))
    input_data['zmid']=np.asarray(0.5*(max(Z_1D)+min(Z_1D)))
 
    input_IDS.close()
 
    return input_data
 
def dump_equilibrium_IDS(ID,output_data,shot,run):
    """
    writes relevant LOCUST equilibrium data to an equilibrium IDS
 
    notes:
        currently only for rectangular equilibria 
        currently overwrites pre-existing IDSs
        idum not dumped
 
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
    output_IDS.equilibrium.time=np.array(0.0,ndmin=1) #set the global time (required by vacuum_toroidal_field.b0)
 
    #write out the easy stuff - global quantities, some 1D profiles and the boundaries
    output_IDS.equilibrium.vacuum_toroidal_field.r0=output_data['rcentr'] 
    output_IDS.equilibrium.vacuum_toroidal_field.b0=np.array(output_data['bcentr'],ndmin=1) #this needs to be 1D and match the dimensions of output_IDS.equilibrium.time (above)
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
     
    #write out the uniform flux grid output_data
    output_IDS.equilibrium.time_slice[0].profiles_1d.psi=output_data['psi_1D']
    output_IDS.equilibrium.time_slice[0].profiles_1d.f=output_data['fpol'] 
    output_IDS.equilibrium.time_slice[0].profiles_1d.pressure=output_data['pres'] 
    output_IDS.equilibrium.time_slice[0].profiles_1d.f_df_dpsi=output_data['ffprime'] 
    output_IDS.equilibrium.time_slice[0].profiles_1d.dpressure_dpsi=output_data['pprime'] 
    output_IDS.equilibrium.time_slice[0].profiles_1d.q=output_data['qpsi'] 
 
    #now define the R,Z simulation grid
    output_IDS.equilibrium.time_slice[0].profiles_2d.resize(1) #add an element onto the profiles_2d struct_array to define this grid
    output_IDS.equilibrium.time_slice[0].profiles_2d[0].grid_type.name='rectangular grid' #add some identifiers for this particular grid
    output_IDS.equilibrium.time_slice[0].profiles_2d[0].grid_type.description=''
    output_IDS.equilibrium.time_slice[0].profiles_2d[0].grid_type.index=1 #1 for rectangular (R,Z), 0 for inverse (psi,theta)
  
    #write out R,Z grid coordinate arrays
    output_IDS.equilibrium.time_slice[0].profiles_2d[0].grid.dim1=output_data['R_1D'] #dim1=R values/dim2=Z values
    output_IDS.equilibrium.time_slice[0].profiles_2d[0].grid.dim2=output_data['Z_1D']
    R_2D,Z_2D=np.meshgrid(output_data['R_1D'],output_data['Z_1D']) #generate 2D arrays of R,Z values
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
        self.data_format            data format of original data e.g. GEQDSK
        self.input_filename         name of file in input_files folder
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
  
    def read_data(self,data_format=None,input_filename=None,shot=None,run=None,properties=None): #always supply all possible arguments for reading in data, irrespective of read in type
        """
        read equilibrium from file 
 
        notes:
        """
 
        if none_check(self.ID,self.LOCUST_input_type,"cannot read_data - data_format required\n",data_format): #must always have data_format if reading in data
            pass
 
        elif data_format=='GEQDSK': #here are the blocks for various file types, they all follow the same pattern
            if not none_check(self.ID,self.LOCUST_input_type,"cannot read_data from GEQDSK - input_filename required\n",input_filename): #check we have all info for reading GEQDSKs
                self.data_format=data_format #add to the member data
                self.input_filename=input_filename
                self.input_filepath=support.dir_input_files+input_filename
                self.properties=properties
                self.data=read_equilibrium_GEQDSK(self.input_filepath) #read the file
            
        elif data_format=='IDS':
            if not none_check(self.ID,self.LOCUST_input_type,"cannot read_data from equilibrium IDS - shot and run data required\n",shot,run):
                self.data_format=data_format
                self.shot=shot
                self.run=run
                self.properties=properties
                self.data=read_equilibrium_IDS(self.shot,self.run)
 
        else:
            print("cannot read_data - please specify a compatible data_format (GEQDSK/IDS)\n")
 
    def dump_data(self,data_format=None,output_filename=None,shot=None,run=None):
        """
        write equilibrium to file
 
        notes: 
        """
 
        if none_check(self.ID,self.LOCUST_input_type,"dump_data requires self.data and data_format\n",self.data,data_format):
            pass
         
        elif data_format=='GEQDSK':
            if not none_check(self.ID,self.LOCUST_input_type,"cannot dump_data to GEQDSK - output_filename required\n",output_filename):
                output_filepath=support.dir_input_files+output_filename
                dump_equilibrium_GEQDSK(self.data,output_filepath)
         
        elif data_format=='IDS':
            if not none_check(self.ID,self.LOCUST_input_type,"cannot dump_data to equilibrium IDS - shot and run required\n",shot,run):
                dump_equilibrium_IDS(self.ID,self.data,shot,run)
 
        else:
            print("cannot dump_data - please specify a compatible data_format (GEQDSK/IDS)\n")

 
 
 

 
 
 
 
 
 
 
 
 
 
 
 
 
 
################################################################## Beam_Deposition functions
 
def read_beam_depo_ASCII(input_filepath):
    """
    reads neutral beam deposition profile stored in ASCII format - r phi z v_r v_phi v_z
    """
 
 
    with open(input_filepath,'r') as file:
         
        lines=file.readlines() #return lines as list
        if not lines: #check to see if the file opened
            raise IOError("ERROR: read_beam_depo_ASCII() cannot read from "+input_filepath)
     
    del(lines[0]) #first two lines are junk
    del(lines[0])
 
    input_data = {} #initialise the dictionary to hold the data
    input_data['r']=[] #initialise the arrays 
    input_data['phi']=[]
    input_data['z']=[]
    input_data['v_r']=[]
    input_data['v_phi']=[]
    input_data['v_z']=[]
 
    for line in lines:
 
        split_line=line.split()
        input_data['r'].append(float(split_line[0]))
        input_data['phi'].append(float(split_line[1]))
        input_data['z'].append(float(split_line[2]))
        input_data['v_r'].append(float(split_line[3]))
        input_data['v_phi'].append(float(split_line[4]))
        input_data['v_z'].append(float(split_line[5]))
 
    input_data['r']=np.asarray(input_data['r']) #convert to arrays
    input_data['phi']=np.asarray(input_data['phi'])
    input_data['z']=np.asarray(input_data['z'])
    input_data['v_r']=np.asarray(input_data['v_r'])
    input_data['v_phi']=np.asarray(input_data['v_phi'])
    input_data['v_z']=np.asarray(input_data['v_z'])
 
    return input_data
 
def dump_beam_depo_ASCII(output_data,output_filepath):
    """
    writes neutral beam deposition profile to ASCII format - r z phi v_r v_z v_phi
     
    notes:
        writes out two headerlines
    """
 
    with open(output_filepath,'w') as file: #open file
 
        file.write("1.0\n") #re-insert junk lines
        file.write("1.0\n")
 
        for this_particle in range(output_data['r'].size): #iterate through all particles i.e. length of our dictionary's arrays
 
            r_out=output_data['r'][this_particle] #briefly set to a temporary variable to improve readability
            phi_out=output_data['phi'][this_particle]
            z_out=output_data['z'][this_particle]
            v_r_out=output_data['v_r'][this_particle]
            v_phi_out=output_data['v_phi'][this_particle]
            v_z_out=output_data['v_z'][this_particle]
 
            file.write("{r} {phi} {z} {v_r} {v_phi} {v_z}\n".format(r=r_out,phi=phi_out,z=z_out,v_r=v_r_out,v_phi=v_phi_out,v_z=v_z_out))
 
 
def read_beam_depo_IDS(shot,run):
    """
    reads relevant LOCUST neutral beam data from a distribution_sources IDS and returns as a dictionary
 
    notes:
        
    """
 
    input_IDS=imas.ids(shot,run) #initialise new blank IDS
    input_IDS.open()
    input_IDS.distribution_sources.get() #open the file and get all the data from it
 
    #extract the 2D positions array
    positions=input_IDS.distribution_sources.source[0].markers[0].positions #assume everything is stored in the first source, and first marker type
 
    input_data = {} #initialise blank dictionary to hold the data
    input_data['r']=np.asarray(positions[:,0])
    input_data['phi']=np.asarray(positions[:,1])
    input_data['z']=np.asarray(positions[:,2])
    input_data['v_r']=np.asarray(positions[:,3])
    input_data['v_phi']=np.asarray(positions[:,4])
    input_data['v_z']=np.asarray(positions[:,5])
 
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
    output_IDS.distribution_sources.source[0].markers[0].coordinate_identifier[0].name="r, phi, z" #add some description here
    output_IDS.distribution_sources.source[0].markers[0].coordinate_identifier[0].index=0 #set arbitrarily here
    output_IDS.distribution_sources.source[0].markers[0].coordinate_identifier[0].description="r, phi, z, v_r, v_phi, v_z coordinate system"
     
    #start storing particle data
    output_IDS.distribution_sources.source[0].markers[0].weights=np.ones(output_data['r'].size) #define the weights, i.e. number of particles per marker 
    positions=np.array([output_data['r'],output_data['phi'],output_data['z'],output_data['v_r'],output_data['v_phi'],output_data['v_z']]) #create 2D array of positions
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
        self.data_format            data format of original data e.g. ASCII
        self.input_filename         name of file in input_files folder
        self.input_filepath         full path of file in input_files folder  
        self.shot                   shot number
        self.run                    run number
        self.properties             data to hold additional class-specific information e.g. ion species in Temperature
        key, value                  key for data dictionary to specify data entry holding value
        target                      external object to copy from
        output_filename             name of file to write to
        output_filepath             full path to output file in output_files folder
 
    notes:
        data is stored such that the coordinate 'r' for all particles is stored in my_beam_deposition['r']
        therefore the phase space position of particle p is:
            (my_beam_deposition['r'][p], my_beam_deposition['phi'][p], my_beam_deposition['z'][p], my_beam_deposition['v_r'][p], my_beam_deposition['v_phi'][p], my_beam_deposition['v_z'][p])
    """
 
    LOCUST_input_type='beam_deposition'
 
    def read_data(self,data_format=None,input_filename=None,shot=None,run=None,properties=None): 
        """
        read beam_deposition from file 
 
        notes:
        """
 
        if none_check(self.ID,self.LOCUST_input_type,"cannot read_data - data_format required\n",data_format): #must always have data_format if reading in data
            pass
 
        elif data_format=='ASCII': #here are the blocks for various file types, they all follow the same pattern
            if not none_check(self.ID,self.LOCUST_input_type,"cannot read_data from ASCII - input_filename required\n",input_filename): #must check we have all info required for reading GEQDSKs
 
                self.data_format=data_format #add to the member data
                self.input_filename=input_filename
                self.input_filepath=support.dir_input_files+input_filename
                self.properties=properties
                self.data=read_beam_depo_ASCII(self.input_filepath) #read the file
         
        elif data_format=='IDS':
            if not none_check(self.ID,self.LOCUST_input_type,"cannot read_data from distribution_sources IDS - shot and run data required\n",shot,run):
 
                self.data_format=data_format
                self.shot=shot
                self.run=run
                self.properties=properties
                self.data=read_beam_depo_IDS(self.shot,self.run)
 
        else:
            print("cannot read_data - please specify a compatible data_format (ASCII/IDS)\n")            
 
    def dump_data(self,data_format=None,output_filename=None,shot=None,run=None):
        """
        write beam_deposition to file
 
        notes: 
        """
 
        if none_check(self.ID,self.LOCUST_input_type,"cannot dump_data - self.data and data_format required\n",self.data,data_format):
            pass
         
        elif data_format=='ASCII':
            if not none_check(self.ID,self.LOCUST_input_type,"cannot dump_data to ASCII - output_filename required\n",output_filename):
                output_filepath=support.dir_input_files+output_filename
                dump_beam_depo_ASCII(self.data,output_filepath)
         
        elif data_format=='IDS':
            if not none_check(self.ID,self.LOCUST_input_type,"cannot dump_data to distribution_sources IDS - shot and run required\n",shot,run):
                dump_beam_depo_IDS(self.ID,self.data,shot,run)
 
        else:
            print("cannot dump_data - please specify a compatible data_format (ASCII/IDS)\n")
 

 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
################################################################## Temperature functions
 
def read_temperature_ASCII(input_filepath):
    """
    reads temperature profile stored in ASCII format - flux_pol T(ev)
    """
 
    with open(input_filepath,'r') as file:
         
        lines=file.readlines() #return lines as list
        if not lines: #check to see if the file opened
            raise IOError("ERROR: read_temperature_ASCII() cannot read from "+input_filepath)
     
    del(lines[0]) #first line contains the number of points
 
    input_data = {} #initialise the dictionary to hold the data
    input_data['flux_pol']=[] #initialise the arrays 
    input_data['T']=[]
 
    for line in lines:
 
        split_line=line.split()
        input_data['flux_pol'].append(float(split_line[0]))
        input_data['T'].append(float(split_line[1]))
 
    input_data['flux_pol']=np.asarray(input_data['flux_pol']) #convert to arrays
    input_data['T']=np.asarray(input_data['T'])
    
    return input_data
 
def dump_temperature_ASCII(output_data,output_filepath):
    """
    writes temperature profile to ASCII format - flux_pol T(ev)    
     
    notes:
        writes out a headerline for length of file
    """
 
    with open(output_filepath,'w') as file: #open file
 
        file.write("{}\n".format(output_data['flux_pol'].size)) #re-insert line containing length
 
        for point in range(output_data['flux_pol'].size): #iterate through all points i.e. length of our dictionary's arrays
 
            flux_pol_out=output_data['flux_pol'][point] #briefly set to a temporary variable to improve readability
            T_out=output_data['T'][point]
             
            file.write("{flux_pol} {T}\n".format(flux_pol=flux_pol_out,T=T_out))
 
def read_temperature_IDS(shot,run,properties):
    """
    reads relevant LOCUST temperature data from a core_profiles IDS and returns as a dictionary
 
    notes:
        
    """
 
    input_IDS=imas.ids(shot,run) #initialise new blank IDS
    input_IDS.open()
    input_IDS.core_profiles.get() #open the file and get all the data from it
 
    input_data = {} #initialise blank dictionary to hold the data
    
    input_data['flux_pol']=np.asarray(input_IDS.core_profiles.profiles_1d[0].grid.psi)
 
    #read in temperature depending on species
    if properties=='electrons':
        input_data['T']=np.asarray(input_IDS.core_profiles.profiles_1d[0].electrons.temperature)
    elif properties=='ions':
        input_data['T']=np.asarray(input_IDS.core_profiles.profiles_1d[0].ion[0].temperature)
    else:
        print("cannot read_temperature_IDS - Temperature.properties must be set to 'electrons' or 'ions'\n")
 
    #read optional quantities
    dict_set(input_data,flux_tor=np.asarray(input_IDS.core_profiles.profiles_1d[0].grid.rho_tor))
    dict_set(input_data,q=np.asarray(input_IDS.core_profiles.profiles_1d[0].q))

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
    output_IDS.core_profiles.profiles_1d[0].time=0.0 #set the time of the time_slice
    output_IDS.core_profiles.profiles_1d[0].grid.psi=output_data['flux_pol']

    #write out temperature depending on species
    if properties=='electrons':
        output_IDS.core_profiles.profiles_1d[0].electrons.temperature=output_data['T']
    elif properties=='ions':
        output_IDS.core_profiles.profiles_1d[0].ion.resize(1) #add an ion species 
        #TODO need to add additional species data here e.g. mass, charge
        output_IDS.core_profiles.profiles_1d[0].ion[0].temperature=output_data['T']
    else:
        print("cannot dump_temperature_IDS - Temperature.properties must be set to 'electrons' or 'ions'\n")

    #dump optional quantities
    safe_set(output_IDS.core_profiles.profiles_1d[0].grid.rho_tor,output_data['flux_tor'])
    safe_set(output_IDS.core_profiles.profiles_1d[0].q,output_data['q'])


    #'put' all the output_data into the file and close
    output_IDS.core_profiles.put()
    output_IDS.close()
 
################################################################## Temperature class
 
class Temperature(LOCUST_input):
    """
    class describing temperature profile input for LOCUST
 
    inherited from LOCUST_input:
        self.ID                     unique object identifier, good convention to fill these for error handling etc
        self.data                   holds all input data in dictionary object
        self.LOCUST_input_type      string which holds this class' input type, this case = 'temperature'
    class data
        self.data_format            data format of original data e.g. ASCII
        self.input_filename         name of file in input_files folder
        self.input_filepath         full path of file in input_files folder  
        self.shot                   shot number
        self.run                    run number
        self.properties             data to hold additional class-specific information e.g. ion species
        key, value                  key for data dictionary to specify data entry holding value
        target                      external object to copy from
        output_filename             name of file to write to
        output_filepath             full path to output file in output_files folder
 
    notes:
        data is stored such that a reading of temperature at coordinate 'coord' is:
            my_temperature['flux_tor'][coord], my_temperature['T'][coord]
    """
 
    LOCUST_input_type='temperature'
 
    def read_data(self,data_format=None,input_filename=None,shot=None,run=None,properties=None):
        """
        read temperature from file 
 
        notes:
        """
        if none_check(self.ID,self.LOCUST_input_type,"Temperature.properties not specified - set to 'electrons' or 'ions' for IDS functionality\n",properties):
            pass
 
        if none_check(self.ID,self.LOCUST_input_type,"cannot read_data - data_format required\n",data_format): #must always have data_format if reading in data
            pass
 
        elif data_format=='ASCII': #here are the blocks for various file types, they all follow the same pattern
            if not none_check(self.ID,self.LOCUST_input_type,"cannot read_data from ASCII - input_filename required\n",input_filename): #must check we have all info required for reading GEQDSKs
 
                self.data_format=data_format #add to the member data
                self.input_filename=input_filename
                self.input_filepath=support.dir_input_files+input_filename
                self.properties=properties
                self.data=read_temperature_ASCII(self.input_filepath) #read the file
         
        elif data_format=='IDS':
            if not none_check(self.ID,self.LOCUST_input_type,"cannot read_data from core_profiles IDS - shot, run and ion species property required\n",shot,run,properties):
 
                self.data_format=data_format
                self.shot=shot
                self.run=run
                self.properties=properties
                self.data=read_temperature_IDS(self.shot,self.run,self.properties)
 
        else:
            print("cannot read_data - please specify a compatible data_format (ASCII/IDS)\n")            
 
    def dump_data(self,data_format=None,output_filename=None,shot=None,run=None):
        """
        write temperature to file
 
        notes: 
        """
 
        if none_check(self.ID,self.LOCUST_input_type,"cannot dump_data - self.data and data_format required\n",self.data,data_format):
            pass
         
        elif data_format=='ASCII':
            if not none_check(self.ID,self.LOCUST_input_type,"cannot dump_data to ASCII - output_filename required\n",output_filename):
                output_filepath=support.dir_input_files+output_filename
                dump_temperature_ASCII(self.data,output_filepath)
         
        elif data_format=='IDS':
            if not none_check(self.ID,self.LOCUST_input_type,"cannot dump_data to core_profiles IDS - shot, run and ion species property required\n",shot,run,self.properties):
                dump_temperature_IDS(self.ID,self.data,shot,run,self.properties)
 
        else:
            print("cannot dump_data - please specify a compatible data_format (ASCII/IDS)\n")
 

 
 
 
 
 
 
 
 
 
 
 






 
 
 
 

 
 
 
################################################################## Number_Density functions
 
def read_number_density_ASCII(input_filepath):
    """
    reads number density profile stored in ASCII format - flux_pol n
 
    notes:
        reads in a headerline for length of file
    """
 
    with open(input_filepath,'r') as file:
         
        lines=file.readlines() #return lines as list
        if not lines: #check to see if the file opened
            raise IOError("ERROR: read_number_density_ASCII() cannot read from "+input_filepath)
     
    del(lines[0]) #first line contains the number of points
 
    input_data = {} #initialise the dictionary to hold the data
    input_data['flux_pol']=[] #initialise the arrays 
    input_data['n']=[]
 
    for line in lines:
 
        split_line=line.split()
        input_data['flux_pol'].append(float(split_line[0]))
        input_data['n'].append(float(split_line[1]))
 
    input_data['flux_pol']=np.asarray(input_data['flux_pol']) #convert to arrays
    input_data['n']=np.asarray(input_data['n'])
    
    return input_data
 
def dump_number_density_ASCII(output_data,output_filepath):
    """
    writes number density profile to ASCII format - flux_pol n 
     
    notes:
        writes out a headerline for length of file
    """
 
    with open(output_filepath,'w') as file: #open file
 
        file.write("{}\n".format(output_data['flux_pol'].size)) #re-insert line containing length
 
        for point in range(output_data['flux_pol'].size): #iterate through all points i.e. length of our dictionary's arrays
 
            flux_pol_out=output_data['flux_pol'][point] #briefly set to a temporary variable to improve readability
            n_out=output_data['n'][point]
             
            file.write("{flux_pol} {n}\n".format(flux_pol=flux_pol_out,n=n_out))
 
def read_number_density_IDS(shot,run,properties):
    """
    reads relevant LOCUST number density data from a core_profiles IDS and returns as a dictionary
 
    notes:
        
    """
 
    input_IDS=imas.ids(shot,run) #initialise new blank IDS
    input_IDS.open()
    input_IDS.core_profiles.get() #open the file and get all the data from it
 
    input_data = {} #initialise blank dictionary to hold the data
    
    input_data['flux_pol']=np.asarray(input_IDS.core_profiles.profiles_1d[0].grid.psi) 

    #read in number density depending on species
    if properties=='electrons':
        input_data['n']=np.asarray(input_IDS.core_profiles.profiles_1d[0].electrons.density)
    elif properties=='ions':
        input_data['n']=np.asarray(input_IDS.core_profiles.profiles_1d[0].ion[0].density)
    else:
        print("cannot read_number_density_IDS - Number_Density.properties must be set to 'electrons' or 'ions'\n")

    #read optional quantities
    dict_set(input_data,flux_tor=np.asarray(input_IDS.core_profiles.profiles_1d[0].grid.rho_tor))
    dict_set(input_data,q=np.asarray(input_IDS.core_profiles.profiles_1d[0].q))

    input_IDS.close()
 
    return input_data
 
def dump_number_density_IDS(ID,output_data,shot,run,properties):
    """
    writes relevant LOCUST number density data to a core_profiles IDS
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
    output_IDS.core_profiles.profiles_1d[0].time=0.0 #set the time of the time_slice
    output_IDS.core_profiles.profiles_1d[0].grid.psi=output_data['flux_pol']
 
    #write out number density depending on species
    if properties=='electrons':
        output_IDS.core_profiles.profiles_1d[0].electrons.density=output_data['n']
    elif properties=='ions':
        output_IDS.core_profiles.profiles_1d[0].ion.resize(1) #add an ion species 
        #TODO need to add additional species data here e.g. mass, charge
        output_IDS.core_profiles.profiles_1d[0].ion[0].density=output_data['n']
    else:
        print("cannot dump_number_density_IDS - Number_Density.properties must be set to 'electrons' or 'ions'\n")

    #dump optional quantities
    safe_set(output_IDS.core_profiles.profiles_1d[0].grid.rho_tor,output_data['flux_tor'])
    safe_set(output_IDS.core_profiles.profiles_1d[0].q,output_data['q'])

    #'put' all the output_data into the file and close
    output_IDS.core_profiles.put()
    output_IDS.close()
 
################################################################## Number_Density class
 
class Number_Density(LOCUST_input):
    """
    class describing number density profile input for LOCUST
 
    inherited from LOCUST_input:
        self.ID                     unique object identifier, good convention to fill these for error handling etc
        self.data                   holds all input data in dictionary object
        self.LOCUST_input_type      string which holds this class' input type, this case = 'number density'
    class data
        self.data_format            data format of original data e.g. ASCII
        self.input_filename         name of file in input_files folder
        self.input_filepath         full path of file in input_files folder  
        self.shot                   shot number
        self.run                    run number
        self.properties             data to hold additional class-specific information e.g. ion species
        key, value                  key for data dictionary to specify data entry holding value
        target                      external object to copy from
        output_filename             name of file to write to
        output_filepath             full path to output file in output_files folder
 
    notes:
        data is stored such that a reading of number density at coordinate 'coord' is:
            my_number_density['flux_tor'][coord], my_number_density['n'][coord]
    """
 
    LOCUST_input_type='number_density'
 
    def read_data(self,data_format=None,input_filename=None,shot=None,run=None,properties=None):
        """
        read number density from file 
 
        notes:
        """
        if none_check(self.ID,self.LOCUST_input_type,"Number_Density.properties not specified - set to 'electrons' or 'ions' for IDS functionality\n",properties):
            pass
 
        if none_check(self.ID,self.LOCUST_input_type,"cannot read_data - data_format required\n",data_format): #must always have data_format if reading in data
            pass
 
        elif data_format=='ASCII': #here are the blocks for various file types, they all follow the same pattern
            if not none_check(self.ID,self.LOCUST_input_type,"cannot read_data from ASCII - input_filename required\n",input_filename): #must check we have all info required for reading GEQDSKs
 
                self.data_format=data_format #add to the member data
                self.input_filename=input_filename
                self.input_filepath=support.dir_input_files+input_filename
                self.properties=properties
                self.data=read_number_density_ASCII(self.input_filepath) #read the file
         
        elif data_format=='IDS':
            if not none_check(self.ID,self.LOCUST_input_type,"cannot read_data from core_profiles IDS - shot, run and ion species property required\n",shot,run,properties):
 
                self.data_format=data_format
                self.shot=shot
                self.run=run
                self.properties=properties
                self.data=read_number_density_IDS(self.shot,self.run,self.properties)
 
        else:
            print("cannot read_data - please specify a compatible data_format (ASCII/IDS)\n")            
 
    def dump_data(self,data_format=None,output_filename=None,shot=None,run=None):
        """
        write number density to file
 
        notes: 
        """
        if none_check(self.ID,self.LOCUST_input_type,"cannot dump_data - self.data and data_format required\n",self.data,data_format):
            pass
         
        elif data_format=='ASCII':
            if not none_check(self.ID,self.LOCUST_input_type,"cannot dump_data to ASCII - output_filename required\n",output_filename):
                output_filepath=support.dir_input_files+output_filename
                dump_number_density_ASCII(self.data,output_filepath)
         
        elif data_format=='IDS':
            if not none_check(self.ID,self.LOCUST_input_type,"cannot dump_data to core_profiles IDS - shot, run and ion species property required\n",shot,run,self.properties):
                dump_number_density_IDS(self.ID,self.data,shot,run,self.properties)
 
        else:
            print("cannot dump_data - please specify a compatible data_format (ASCII/IDS)\n")
 

 
 
 
 
 
 
 
#################################
 
##################################################################
 
###################################################################################################
