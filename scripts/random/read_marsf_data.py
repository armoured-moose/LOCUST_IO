def read_marsf_data(output_data,mode_number,**properties):
    
    """
    read MARS-F data stored in ITER cluster: /work/projects/3D-fields/
    and save to output_data (dictionary type) 
    data to read from files: SCHIMESH_RECTRZ.IN, BPLASMA_MARSF*.IN, TORQUE*.IN

    args:
        ddir - folder where MARS-F data are stored, e.g. ddir="/work/projects/3D-fields/DataBase/ITER_10MA_case6/DataMarsf"
        mode_number - toroidal mode number of perturbation 
        properties['flow'] - flow model specification (string type), e.g. "Pr03_tfte12"

    notes:
        assumes ...

    """ 

    try:
        import numpy as np
    except:
        raise ImportError("ERROR: cannot import standard Python modules!\nreturning\n")
        return


    print("start reading MARS-F data from the database stored in ITER cluster")

    ns = "%1i" % mode_number
    fs = properties['flow']
    ddir = properties['inputdir']

    #read mesh data
    f = open(ddir+"/SCHIMESH_RECTRZ.IN","r")
    d = f.read()
    f.close()

    d = d.split()

    NR = int(d[0])
    NZ = int(d[1])

    d = d[4:]
    d = np.array(d)
    d = d.reshape((NR,NZ,4))

    output_data['MESH_NR']  = NR
    output_data['MESH_NZ']  = NZ
    output_data['MESH_R']   = d[:,:,0]
    output_data['MESH_Z']   = d[:,:,1]
    output_data['MESH_S']   = d[:,:,2]
    output_data['MESH_CHI'] = d[:,:,3]
    

    #read BPLASMA_MARSF data
    for C in ['U','M','L'] :
        f = open(ddir+"/BPLASMA_MARSF_n"+ns+"_c"+C+"_"+fs+".IN","r")
        d = f.read()
        f.close()

        d = d.split()

        M0 = int(d[1])
        M1 = int(d[2])
        M2 = int(d[3])
        NR = int(d[4])
        NV = int(d[5])
        NT = NR + NV
        MM = M2-M1+1

        a = d[9:9+3*NT]
        a = np.array(a)
        a = a.reshape((NT,3))
        S = a[:,0]

        N = 9+3*NT+8*M0*NT
        a = d[N:N+6*MM*NT]
        a = np.array(a)
        B = a.reshape((MM,NT,6))

        N = 9+3*NT+8*M0*NT+6*MM*NT
        a = d[N:]
        a = np.array(a)
        X = a.reshape((MM,NR+1,2))

        output_data['FIELD_M1']  = M1
        output_data['FIELD_M2']  = M2
        output_data['FIELD_NR']  = NR
        output_data['FIELD_NV']  = NV
        output_data['FIELD_S']   = S
        output_data['FIELD_B'+C] = B
        output_data['FIELD_X'+C] = X

    #read TORQUE* matrices data
    for C in ['JXB','NTV','REY'] :
        f = open(ddir+"/TORQUE"+C+"_n"+ns+"_"+fs+".IN","r")
        d = f.read()
        f.close()

        d = d.split()
    
        N = int(len(d)/19)
        a = np.array(d)
        a = a.reshape((N,19))
        S = a[:,0]
        T = a[:,1:]

        output_data['TORQ_S']  = S
        output_data['TORQ_'+C] = T

    print("finished reading MARS-F data from the database stored in ITER cluster")

