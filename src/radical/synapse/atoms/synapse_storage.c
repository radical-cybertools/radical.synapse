
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

int main (int argc, char** argv)
{
    if ( argc < 3 )
    {
        return -1;
    }

    struct rusage ru;
    char*  tgt  =        argv[1];
    off_t  n    = atol  (argv[2]) * CHUNKSIZE;
    int    fd   = open  (tgt, O_CREAT | O_TRUNC | O_WRONLY, S_IRWXU);

    if ( fd < 0 )
    {
        perror ("open failed");
        return -2;
    }

    /* clear disk cache */
  //(void) syncfs (fd); 
    (void) sync ();

    off_t tot = 0;
    char* buf = malloc (CHUNKSIZE);

    while ( tot < (n+1) )
    {
        size_t wret = write (fd, buf, CHUNKSIZE);
  
        if ( wret != CHUNKSIZE )
        {
            perror ("write failed");
            return -4;
        }
  
        tot += CHUNKSIZE;
    }
  
    /* clear disk cache */
  //(void) syncfs (fd); 
    (void) sync ();

    free  (buf);
    close (fd);
  
    (void) unlink (tgt);

    if ( 0 != getrusage (RUSAGE_SELF, &ru) )
    {
        fprintf (stderr, "no ru: %s", strerror (errno));
        return (1);
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
    fprintf (stdout, "ru.oublock       : %ld\n",     ru.ru_oublock       ); /* block output operations */
    fprintf (stdout, "ru.msgsnd        : %ld\n",     ru.ru_msgsnd        ); /* IPC messages sent */
    fprintf (stdout, "ru.msgrcv        : %ld\n",     ru.ru_msgrcv        ); /* IPC messages received */
    fprintf (stdout, "ru.nsignals      : %ld\n",     ru.ru_nsignals      ); /* signals received */
    fprintf (stdout, "ru.nvcsw         : %ld\n",     ru.ru_nvcsw         ); /* voluntary context switches */
    fprintf (stdout, "ru.nivcsw        : %ld\n",     ru.ru_nivcsw        ); /* involuntary context switches */
    return (0);
}

