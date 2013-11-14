
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

#define CHUNKSIZE  (1000 * 1000)  /* 10^6 */

int main (int argc, char** argv)
{
    /* size */
    if ( argc < 2 )
    {
        return -1;
    }

    size_t n = atol (argv[1]) * CHUNKSIZE;
    double f = 1.0;

    /* consume the given number of FLOPs, and some IOPS, too */
    unsigned long int i = 0;
    for (i = 0; i < n; i++ ) {       /* 3 MIPS, 1 BRANCH */
        if (i > 0) {                 /* 1 Branch         */
            f = f * 1.000000000001;  /* 1 FLOP           */
        }
    }

    struct rusage ru;
    getrusage (RUSAGE_SELF, &ru);

    fprintf (stdout, "ru_utime         : %ld.%ld\n", ru.ru_utime.tv_sec,
             ru.ru_utime.tv_usec ); /* user CPU time used */
    fprintf (stdout, "ru_stime         : %ld.%ld\n", ru.ru_stime,
             ru.ru_stime.tv_usec ); /* system CPU time used */
    fprintf (stdout, "ru_maxrss        : %ld\n",     ru.ru_maxrss        ); /* maximum resident set size */
    fprintf (stdout, "ru_ixrss         : %ld\n",     ru.ru_ixrss         ); /* integral shared memory size */
    fprintf (stdout, "ru_idrss         : %ld\n",     ru.ru_idrss         ); /* integral unshared data size */
    fprintf (stdout, "ru_isrss         : %ld\n",     ru.ru_isrss         ); /* integral unshared stack size */
    fprintf (stdout, "ru_minflt        : %ld\n",     ru.ru_minflt        ); /* page reclaims (soft page faults) */
    fprintf (stdout, "ru_majflt        : %ld\n",     ru.ru_majflt        ); /* page faults (hard page faults) */
    fprintf (stdout, "ru_nswap         : %ld\n",     ru.ru_nswap         ); /* swaps */
    fprintf (stdout, "ru_inblock       : %ld\n",     ru.ru_inblock       ); /* block input operations */
    fprintf (stdout, "ru_oublock       : %ld\n",     ru.ru_oublock       ); /* block output operations */
    fprintf (stdout, "ru_msgsnd        : %ld\n",     ru.ru_msgsnd        ); /* IPC messages sent */
    fprintf (stdout, "ru_msgrcv        : %ld\n",     ru.ru_msgrcv        ); /* IPC messages received */
    fprintf (stdout, "ru_nsignals      : %ld\n",     ru.ru_nsignals      ); /* signals received */
    fprintf (stdout, "ru_nvcsw         : %ld\n",     ru.ru_nvcsw         ); /* voluntary context switches */
    fprintf (stdout, "ru_nivcsw        : %ld\n",     ru.ru_nivcsw        ); /* involuntary context switches */

    return 0;
}

