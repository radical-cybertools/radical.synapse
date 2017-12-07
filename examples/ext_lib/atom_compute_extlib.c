
#include <stdio.h>
#include <unistd.h>

int ext_lib_workload(int load)
{
    fprintf(stdout, "ext_lib sleeping for %d seconds", load);
    sleep(load);
    return 0;
}

