
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


#define CHUNKSIZE  (1024 * 1024)  /* 2^20 */
#define RUSAGE     0

int main (int argc, char** argv)
{
    /* size */
    if ( argc < 2 )
    {
        return -1;
    }

    /* *********************************
     * 1 loop iter allocates 1 MByte
     */
    n = n / CHUNKSIZE

    size_t n = atol   (argv[1]) * CHUNKSIZE;
    char*  c = malloc (n * sizeof(char));

    /* make sure the memory actually got allocated */
    unsigned long int i = 0;
    for ( i = 0; i < n; i++ ) {
        c[i] = '\0';
        c[i]++;
    }

    free (c);

    if ( PROFILE )
    {
        struct rusage ru;

        if ( 0 != getrusage (RUSAGE_SELF, &ru) )
        {
            fprintf (stderr, "no ru: %s", strerror (errno));
            return (1);
        }

        fprintf (stdout, "ru.Utime         : %ld.%ld\n", ru.ru_utime.tv_sec,
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

