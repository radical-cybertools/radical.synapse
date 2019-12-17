
#include <stdio.h>
#include <unistd.h>

long ext_lib_workload(long flops, long time)
{
    fprintf(stdout, "ext_lib sleeping for %ld seconds", flops);
    sleep(flops);
    return 0;
}


