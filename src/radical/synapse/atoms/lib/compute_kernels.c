#include <stdio.h>
#include <time.h>
#include "compute_kernels.h"


void _simple_adder(long iter)
{
    //clock_t start, end;
    //double cpu_time_used;

    //start = clock();

    long i;
    for (i = 0; i < iter; i++)
    {
        {
        __asm__ __volatile__
            (
            "addl %%eax, %%eax \n\t"
            "addl %%ebx, %%ebx \n\t"
            "addl %%ecx, %%ecx \n\t"
            "addl %%edx, %%edx \n\t"
            : /* outputs */
            : /* inputs */
            : /* clobbered */ "eax", "ebx", "ecx", "edx"
            );
        }
    }

    //end = clock();
    //cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    //printf("time for _simple atom to execute: %f (s)\n", cpu_time_used);
}


void _mat_mult(long iter, float *A, float *B, float *C, long len)
{

    clock_t start, end;
    double cpu_time_used;

    start = clock();

    long i, j, k;

    for (i = 0; i < len; i++)
    {
        for (j = 0; j < len; j++)
        {
            for (k = 0; k < len; k++)
            {
                //printf("%d %d %d\n", i, j, k);
                C[i*len + j] += (A[i*len + k] * B[k*len + j]);
            }
        }
    }

    end = clock();
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    printf("time for _mat_mult atom to execute: %f (s)\n", cpu_time_used);
}
