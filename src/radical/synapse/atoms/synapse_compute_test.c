#include <atom_compute_extlib.h>


int _atom_compute_test (long flops, long runtime) 
{
    return ext_lib_workload(flops, runtime);
}

