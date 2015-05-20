
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <sys/stat.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/resource.h>

/* NOTE: tune this number to tune loop towards 1 MFlop */
#define CHUNKSIZE  (1024 * 1024)  /* 2^20 */
#define PROFILE     0

float mat_mult (float* a1, float* a2, int n);

int _atom_compute_asm (long flops)
{
    size_t  n = flops / (1024 * 1024);
    float * f = calloc (CHUNKSIZE, sizeof(float));

    /* This is an overhead for each sample :( */
    unsigned int i = 0;
    for ( i = 0; i < CHUNKSIZE; i++ ) 
    { 
        f[i] = i * 0.01;
    }

    /* *********************************
     * 1 loop gives 1 MFLOP
     */
    for ( i = 0; i < n; i++ ) 
    {
        mat_mult (f, f, CHUNKSIZE);
    }
    /* ********************************* */

    free (f);

    if (PROFILE)
    {
        struct rusage ru;

        if ( 0 != getrusage (RUSAGE_SELF, &ru) )
        {
            fprintf (stderr, "no ru: %s", strerror (errno));
            return  (1);
        }

        fprintf (stdout, "ru.utime         : %ld.%ld\n", ru.ru_utime.tv_sec,
                                                         ru.ru_utime.tv_usec ); /* user CPU time used */
        fprintf (stdout, "ru.stime         : %ld.%ld\n", ru.ru_stime,
                                                         ru.ru_stime.tv_usec ); /* system CPU time used */
        fprintf (stdout, "ru.maxrss        : %ld\n",     ru.ru_maxrss*1024   ); /* maximum resident set size */
        fprintf (stdout, "ru.ixrss         : %ld\n",     ru.ru_ixrss         ); /* integral shared memory size */
        fprintf (stdout, "ru.idrss         : %ld\n",     ru.ru_idrss         ); /* integral unshared data size */
        fprintf (stdout, "ru.isrss         : %ld\n",     ru.ru_isrss         ); /* integral unshared stack size */
        fprintf (stdout, "ru.minflt        : %ld\n",     ru.ru_minflt        ); /* page reclaims (soft page faults) */
        fprintf (stdout, "ru.majflt        : %ld\n",     ru.ru_majflt        ); /* page faults (hard page faults) */
        fprintf (stdout, "ru.nswap         : %ld\n",     ru.ru_nswap         ); /* swaps */
        fprintf (stdout, "ru.inblock       : %ld\n",     ru.ru_inblock       ); /* block input operations */
        fprintf (stdout, "ru.outblock      : %ld\n",     ru.ru_oublock       ); /* block output operations */
        fprintf (stdout, "ru.msgsnd        : %ld\n",     ru.ru_msgsnd        ); /* IPC messages sent */
        fprintf (stdout, "ru.msgrcv        : %ld\n",     ru.ru_msgrcv        ); /* IPC messages received */
        fprintf (stdout, "ru.nsignals      : %ld\n",     ru.ru_nsignals      ); /* signals received */
        fprintf (stdout, "ru.nvcsw         : %ld\n",     ru.ru_nvcsw         ); /* voluntary context switches */
        fprintf (stdout, "ru.nivcsw        : %ld\n",     ru.ru_nivcsw        ); /* involuntary context switches */
    }

    return 0;
}


float mat_mult (float* a1, float* a2, int n)
{
    /* 
     * kudos: 
     * http://www.drdobbs.com/optimizing-cc-with-inline-assembly-progr 
     */

    float ans[4] __attribute__ ((aligned(16)));
    register int i;

    if (n >= 8)
    {
        __asm__ __volatile__ (
            "xorps            %%xmm0, %%xmm0"
            : /* outputs   */
            : /* inputs    */
            : /* clobbered */ "xmm0" );
        for ( i = 0; i < ( n >> 3 ); ++i )
        {
            __asm__ __volatile__ (
                "movups           (%0),   %%xmm1\n\t"
                "movups           16(%0), %%xmm2\n\t"
                "movups           (%1),   %%xmm3\n\t"
                "movups           16(%1), %%xmm4\n\t"
                "add              $32,%0\n\t"
                "add              $32,%1\n\t"
                "mulps            %%xmm3, %%xmm1\n\t"
                "mulps            %%xmm4, %%xmm2\n\t"
                "addps            %%xmm2, %%xmm1\n\t"
                "addps            %%xmm1, %%xmm0"
                : /* outputs   */ "+r" ( a1 ), "+r" ( a2 )
                : /* inputs    */
                : /* clobbered */ "xmm0", "xmm1", "xmm2", "xmm3", "xmm4" );

            ans[0] *= ans[1];
        }
        __asm__ __volatile__ (
            "movaps           %%xmm0, %0"
            : /* outputs   */ "=m" ( ans )
            : /* inputs    */
            : /* clobbered */ "xmm0", "memory" );

        n -= i << 3;
        ans[0] += ans[1] + ans[2] + ans[3];
    }
    else
    {
        ans[0] = 0.0;
    }

    for ( i = 0; i < n; ++i )
    {
        ans[0] += a1[i] * a2[i];
    }

    return (ans[0]);
}

