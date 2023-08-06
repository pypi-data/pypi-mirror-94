# distutils: language=c++

import cython
cimport numpy as np
import numpy as np


# make the c type

#cdef extern from "ssa_translation_c_w.h":
    #void translationSSA(double *kelong, double *t_array, int Nt, double kbind, double kcompl, int *SSA_result, int N, int FRAP, int Inhibitor, double inhibit_time, int seed, double *SSA_ribtimes, int *nribs,int ribtimesize, int fNt, int* frap_result, int cNt, int* col_result, double* col_t, int* col_x, int colNp, int* x0, int r_footprint, int rib_max )

cdef extern from "ssa_translation_c_w_lowmem.h":
    void translationSSA_lowmem(double *kelong, double *t_array, int Nt, double kbind, double kcompl, int* SSA_intensity, int N, int FRAP, int Inhibitor, double inhibit_time, int seed, double *SSA_ribtimes, int *nribs,int ribtimesize, int fNt, int* frap_result, int cNt, int* col_result, double* col_t, int* col_x, int colNp, int* x0, int r_footprint, int* SSA_probe,int Ncolor, int* flags, double kon, double koff,double* k_probe,int* probe_loc,int* n_probes, int rib_max)

cdef extern from "ssa_translation_c_w_full.h":
    void translationSSA_full(int *riblocations, double *kelong, double *t_array, int Nt, double kbind, double kcompl, int* SSA_intensity, int N, int FRAP, int Inhibitor, double inhibit_time, int seed, double *SSA_ribtimes, int *nribs,int ribtimesize, int fNt, int* frap_result, int cNt, int* col_result, double* col_t, int* col_x, int colNp, int* x0, int r_footprint, int* SSA_probe,int Ncolor, int* flags, double kon, double koff,double* k_probe,int* probe_loc,int* n_probes, int rib_max)

cdef extern from "ssa_translation_generic_lowmem_c_w.h":
    void translationSSA_generic_lowmem(double* kelong, double* t_array, int* SSA_result, int N, int Nt, double* inhibitors, int seed, int fNt, int* frap_result, double* k_add, int n_enters,int n_pauses,int n_stops, int n_jumps,int* SSA_probe, int Ncolor, int Nlocs, int watched_ribs );

cdef extern from "ssa_translation_generic_c_w.h":
    void translationSSA_generic(double *kelong, double *t_array, int *SSA_result, int N,int Nt, double* inhibitors, int seed, double *SSA_ribtimes, int *nribs,int ribtimesize, int fNt, int* frap_result, int cNt, int* col_result, double* k_add, int n_enters,int n_pauses,int n_stops, int n_jumps  )

cdef extern from "ssa_trna_c_w.h":
    void translationSSA_trna(int *k_index, double *k_trna, double k_diffusion, double *t_array, int Nt, double kbind, double kcompl, int *SSA_result,int *trna_result, int N, int FRAP, int Inhibitor, double inhibit_time, int seed, double *SSA_ribtimes, int *nribs,int ribtimesize, int fNt, int* frap_result, int cNt, int* col_result, double* col_t, int* col_x, int colNp, int* x0, double kelong)

cdef extern from "ssa_trna_lowmem_c_w.h":
    void translationSSA_trna_lowmem(int *k_index, double *k_trna, double k_diffusion, double *t_array, int Nt, double kbind, double kcompl, double kelong, int *SSA_result,int *trna_result, int N, int FRAP, int Inhibitor, double inhibit_time, int seed, int fNt, int *frap_result, int *x0,int r_footprint, int *SSA_probe, int Ncolor)


@cython.boundscheck(False)
@cython.wraparound(False)


# cdef class PySSA:
    
#     cdef int c_leaky
#     cdef int c_bursting
#     cdef int c_lowmem
#     cdef int c_stats
    
#     cdef int footprint
#     cdef int rib_max
    
    
#     def __cinit__(self):
#         self.c_leaky = 0
#         self.c_bursting = 0
#         self.c_stats = 0
#         self.c_lowmem = 1
#         self.footprint = 9
#         self.rib_max = 200
        

#     def set_flags(self,leaky, bursting, stats, lowmem):
#         self.c_leaky = leaky
#         self.c_bursting = bursting
#         self.c_stats = stats
#         self.c_lowmem = lowmem
        
#     def set_footprints(self,r_footprint,rib_max):
#         self.footprint = r_footprint
#         self.rib_max = rib_max

def run_SSA_generic(np.ndarray[int, ndim=1, mode="c"] result not None, np.ndarray[double, ndim=1, mode="c"] ribtimes not None, np.ndarray[int, ndim=1, mode="c"] coltimes not None,np.ndarray[double, ndim=1, mode="c"] kelong not None, np.ndarray[int, ndim=1, mode="c"] frap_result not None, np.ndarray[double, ndim=1, mode="c"] t_array not None, np.ndarray[double, ndim=1, mode="c"] inhibitors not None, int seed, np.ndarray[int, ndim=1, mode="c"] nribs not None,np.ndarray[double, ndim=1, mode="c"] k_add not None, int n_enters,int n_pauses, int n_stops, int n_jumps ):
    """
    I need to write this. 
    """
    cdef int Nt
    cdef int N
    

    # subtract 2. 
    N = len(kelong)/3
   
    Nt = t_array.shape[0]
    ribtimesize = ribtimes.shape[0]
    coltimesize = coltimes.shape[0]
    fNt = t_array.shape[0]
    cNt = t_array.shape[0]
    #inhibitors = [0,0,0]
    
    translationSSA_generic (&kelong[0], &t_array[0], &result[0], N, Nt, &inhibitors[0], seed, &ribtimes[0],&nribs[0], ribtimesize,fNt,&frap_result[0],coltimesize,&coltimes[0],  &k_add[0], n_enters, n_pauses,  n_stops, n_jumps)

    return None


def run_SSA_generic_lowmem(np.ndarray[int, ndim=2, mode="c"] result not None, np.ndarray[double, ndim=1, mode="c"] kelong not None, np.ndarray[int, ndim=1, mode="c"] frap_result not None, np.ndarray[double, ndim=1, mode="c"] t_array not None, np.ndarray[double, ndim=1, mode="c"] inhibitors not None, int seed, np.ndarray[double, ndim=1, mode="c"] k_add not None, int n_enters,int n_pauses, int n_stops, int n_jumps, np.ndarray[int, ndim=2, mode="c"] probevec not None, int Ncolor, int watched_ribs ):
    """
    I need to write this. 
    """
    cdef int Nt
    cdef int N
    
    
    # subtract 2. 
    N = len(kelong+2)/3
    Nlocs = len(kelong)
    Nt = t_array.shape[0]

    fNt = t_array.shape[0]

    #inhibitors = [0,0,0]
 
    translationSSA_generic_lowmem (&kelong[0], &t_array[0], &result[0,0], N, Nt, &inhibitors[0], seed,fNt,&frap_result[0],  &k_add[0], n_enters, n_pauses,  n_stops, n_jumps, &probevec[0,0], Ncolor,Nlocs, watched_ribs)

    return None



def run_SSA(np.ndarray[int, ndim=2, mode="c"] intensity not None, np.ndarray[double, ndim=1, mode="c"] ribtimes not None, np.ndarray[int, ndim=1, mode="c"] coltimes not None, np.ndarray[int, ndim=1, mode="c"] col_x not None, np.ndarray[double, ndim=1, mode="c"] col_t not None ,np.ndarray[double, ndim=1, mode="c"] kelong not None, np.ndarray[int, ndim=1, mode="c"] frap_result not None, np.ndarray[double, ndim=1, mode="c"] t_array not None, double kbind, double kcompl, int FRAP, int Inhibitor, double inhibit_time, int seed, np.ndarray[int, ndim=1, mode="c"] nribs not None,  np.ndarray[int, ndim=1, mode="c"] x0 not None,int r_footprint, np.ndarray[int, ndim=2, mode="c"] probevec not None, int Ncolor, double kon, double koff, np.ndarray[double, ndim=1, mode="c"] k_probe not None,np.ndarray[int, ndim=2, mode="c"] probeloc not None, np.ndarray[int, ndim=1, mode="c"] flags not None, int N_rib ):
    """
    I need to write this. 
    """       
    
    cdef int N
    cdef int Nt
    
    cdef np.ndarray[int, ndim=1, mode="c"] n_probes = np.zeros([Ncolor],dtype=np.int32)
    # subtract 2. 
    N = len(kelong)
    Nt = t_array.shape[0]
    ribtimesize = ribtimes.shape[0]
    coltimesize = coltimes.shape[0]
    fNt = t_array.shape[0]
    cNt = t_array.shape[0]
    colNp = col_x.shape[0]
    rib_max = N_rib
 
    
    for i in range(0,Ncolor):
      
        n_probes[i] = len(np.where(probeloc[i] == 1)[0]) 
    
    
    pind = np.array(np.where(probeloc== 1)).T.astype(np.int32)
    
    cdef np.ndarray[int, ndim=2, mode="c"] probeloc_indexes = np.zeros(list(pind.shape),dtype=np.int32)
 
    for i in range(0,pind.shape[0]):
        for j in range(0,pind.shape[1]):
            probeloc_indexes[i,j] = pind[i,j]
    
    translationSSA_lowmem (&kelong[0], &t_array[0], Nt, kbind, kcompl, &intensity[0,0], N, FRAP, Inhibitor, inhibit_time,seed,&ribtimes[0],&nribs[0], ribtimesize,fNt,&frap_result[0],coltimesize,&coltimes[0], &col_t[0],&col_x[0],colNp, &x0[0], r_footprint, &probevec[0,0],Ncolor, &flags[0], kon, koff, &k_probe[0], &probeloc_indexes[0,0],&n_probes[0], rib_max)

    return None

def run_SSA_full(np.ndarray[int, ndim=2, mode="c"] rib_locations not None, np.ndarray[int, ndim=2, mode="c"] intensity not None, np.ndarray[double, ndim=1, mode="c"] ribtimes not None, np.ndarray[int, ndim=1, mode="c"] coltimes not None, np.ndarray[int, ndim=1, mode="c"] col_x not None, np.ndarray[double, ndim=1, mode="c"] col_t not None ,np.ndarray[double, ndim=1, mode="c"] kelong not None, np.ndarray[int, ndim=1, mode="c"] frap_result not None, np.ndarray[double, ndim=1, mode="c"] t_array not None, double kbind, double kcompl, int FRAP, int Inhibitor, double inhibit_time, int seed, np.ndarray[int, ndim=1, mode="c"] nribs not None,  np.ndarray[int, ndim=1, mode="c"] x0 not None, int r_footprint, np.ndarray[int, ndim=2, mode="c"] probevec not None, int Ncolor, double kon, double koff, np.ndarray[double, ndim=1, mode="c"] k_probe not None,np.ndarray[int, ndim=2, mode="c"] probeloc not None, np.ndarray[int, ndim=1, mode="c"] flags not None ):
    """
    I need to write this. 
    """       
    
    cdef int N
    cdef int Nt
    
    cdef np.ndarray[int, ndim=1, mode="c"] n_probes = np.zeros([Ncolor],dtype=np.int32)
    # subtract 2. 
    N = len(kelong)
    Nt = t_array.shape[0]
    ribtimesize = ribtimes.shape[0]
    coltimesize = coltimes.shape[0]
    fNt = t_array.shape[0]
    cNt = t_array.shape[0]
    colNp = col_x.shape[0]
    rib_max = rib_locations.shape[0]
  
    
    for i in range(0,Ncolor):
      
        n_probes[i] = len(np.where(probeloc[i] == 1)[0]) 
    
    
    pind = np.array(np.where(probeloc== 1)).T.astype(np.int32)
    
    cdef np.ndarray[int, ndim=2, mode="c"] probeloc_indexes = np.zeros(list(pind.shape),dtype=np.int32)
 
    for i in range(0,pind.shape[0]):
        for j in range(0,pind.shape[1]):
            probeloc_indexes[i,j] = pind[i,j]
    
    translationSSA_full (&rib_locations[0,0], &kelong[0], &t_array[0], Nt, kbind, kcompl, &intensity[0,0], N, FRAP, Inhibitor, inhibit_time,seed,&ribtimes[0],&nribs[0], ribtimesize,fNt,&frap_result[0],coltimesize,&coltimes[0], &col_t[0],&col_x[0],colNp, &x0[0], r_footprint, &probevec[0,0],Ncolor, &flags[0], kon, koff, &k_probe[0], &probeloc_indexes[0,0],&n_probes[0],rib_max)

    return None

def run_SSA_trna_lowmem(np.ndarray[int, ndim=2, mode="c"] intensity not None, np.ndarray[int, ndim=1, mode="c"] trna_result not None, np.ndarray[int, ndim=1, mode="c"] k_index not None, np.ndarray[double, ndim=1, mode="c"] k_trna not None, double k_diffusion, double kelong, np.ndarray[int, ndim=1, mode="c"] frap_result not None, np.ndarray[double, ndim=1, mode="c"] t_array not None, double kbind, double kcompl, int FRAP, int Inhibitor, double inhibit_time, int seed,  np.ndarray[int, ndim=1, mode="c"] x0 not None,  int r_footprint, np.ndarray[int, ndim=2, mode="c"] probevec not None ,int Ncolor):
    """
    I need to write this. 
    """
    cdef int Nt
    cdef int N
    
    # subtract 2. 
    N = len(k_index)
    Nt = t_array.shape[0]

    fNt = int(t_array.shape[0])

    
    
    translationSSA_trna_lowmem(&k_index[0],&k_trna[0],k_diffusion, &t_array[0], Nt, kbind, kcompl,kelong, &intensity[0,0], &trna_result[0], N, FRAP, Inhibitor, inhibit_time,seed,fNt,&frap_result[0], &x0[0], r_footprint, &probevec[0,0],Ncolor)

    return None

def run_SSA_trna_full(np.ndarray[int, ndim=1, mode="c"] result not None, np.ndarray[int, ndim=1, mode="c"] trna_result not None, np.ndarray[double, ndim=1, mode="c"] ribtimes not None, np.ndarray[int, ndim=1, mode="c"] coltimes not None, np.ndarray[int, ndim=1, mode="c"] col_x not None, np.ndarray[double, ndim=1, mode="c"] col_t not None ,np.ndarray[int, ndim=1, mode="c"] k_index not None, np.ndarray[double, ndim=1, mode="c"] k_trna not None, double k_diffusion, np.ndarray[int, ndim=1, mode="c"] frap_result not None, np.ndarray[double, ndim=1, mode="c"] t_array not None, double kbind, double kcompl, int FRAP, int Inhibitor, double inhibit_time, int seed, np.ndarray[int, ndim=1, mode="c"] nribs not None,  np.ndarray[int, ndim=1, mode="c"] x0 not None, double kelong):
    """
    I need to write this. 
    """
    cdef int Nt
    cdef int N
    
    # subtract 2. 
    N = len(k_index)
    Nt = t_array.shape[0]
    ribtimesize = int(ribtimes.shape[0])
    coltimesize = int(coltimes.shape[0])
    fNt = int(t_array.shape[0])
    cNt = int(t_array.shape[0])
    colNp = int(col_x.shape[0])
    
    
    translationSSA_trna(&k_index[0],&k_trna[0],k_diffusion, &t_array[0], Nt, kbind, kcompl, &result[0], &trna_result[0], N, FRAP, Inhibitor, inhibit_time,seed,&ribtimes[0],&nribs[0], ribtimesize,fNt,&frap_result[0],coltimesize,&coltimes[0], &col_t[0],&col_x[0],colNp, &x0[0], kelong)

    return None
# def run_SSA(np.ndarray[int, ndim=1, mode="c"] result not None, np.ndarray[double, ndim=1, mode="c"] ribtimes not None, np.ndarray[int, ndim=1, mode="c"] coltimes not None, np.ndarray[int, ndim=1, mode="c"] col_x not None, np.ndarray[double, ndim=1, mode="c"] col_t not None ,np.ndarray[double, ndim=1, mode="c"] kelong not None, np.ndarray[int, ndim=1, mode="c"] frap_result not None, np.ndarray[double, ndim=1, mode="c"] t_array not None, double kbind, double kcompl, int FRAP, int Inhibitor, double inhibit_time, int seed, np.ndarray[int, ndim=1, mode="c"] nribs not None,  np.ndarray[int, ndim=1, mode="c"] x0 not None,int r_footprint, int rib_max ):
#     """
#     I need to write this. 
#     """
#     cdef int Nt
#     cdef int N
    
#     # subtract 2. 
#     N = len(kelong)
#     Nt = t_array.shape[0]
#     ribtimesize = ribtimes.shape[0]
#     coltimesize = coltimes.shape[0]
#     fNt = t_array.shape[0]
#     cNt = t_array.shape[0]
#     colNp = col_x.shape[0]
    
    
#     translationSSA (&kelong[0], &t_array[0], Nt, kbind, kcompl, &result[0], N, FRAP, Inhibitor, inhibit_time,seed,&ribtimes[0],&nribs[0], ribtimesize,fNt,&frap_result[0],coltimesize,&coltimes[0], &col_t[0],&col_x[0],colNp, &x0[0], r_footprint, rib_max)

#     return None

## Numpy must be initialized. When using numpy from C or Cython you must
## _always_ do that, or you will have segfaults
#np.import_array()
#
#
#cpdef translation_ssa():
#    cdef np.ndarray[int, ndim=1, mode='c'] a
#
#    a = np.zeros((4,), dtype=np.int32)
#    set_integer_arr_ptr(&a[0])
#    return a
