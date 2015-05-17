
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

#define CHUNKSIZE 1024
#define PROFILE   0


size_t get_blocksize(void)
{

  struct stat fi;
  stat ("/", &fi);
  return fi.st_blksize;
}


int _atom_storage (const char* src, long rsize, const char* tgt, long wsize)
{
    int rfd = 0;
    int wfd = 0;

    if (src && rsize)
    {
        rfd = open (src, O_RDONLY);
        if ( rfd < 0 )
        {
            fprintf (stderr, "cannot read from %s\n", src);
            perror ("open for read failed");
            return -2;
        }
    }

    if (tgt && wsize)
    {
        wfd = open (tgt, O_CREAT | O_TRUNC | O_WRONLY, S_IRWXU);
        if ( wfd < 0 )
        {
            fprintf (stderr, "cannot write to %s\n", tgt);
            perror ("open for write failed");
            return -2;
        }
    }


    /* clear disk cache */
 // (void) syncfs (rfd); 
    (void) sync ();

    off_t rtot = 0;
    off_t wtot = 0;
    char* rbuf = malloc (CHUNKSIZE);
    char* wbuf = malloc (CHUNKSIZE);

    while ( rtot < rsize || wtot < wsize )
    {
        size_t rret = 0;
        size_t rlen = rsize - rtot;

        size_t wret = 0;
        size_t wlen = wsize - wtot;

        if ( rlen > 0 )
        { 
            rret = read  (rfd, rbuf, CHUNKSIZE); 
         // fprintf (stderr, "read (%d %ld %ld) = %ld\n", rfd, rbuf, CHUNKSIZE, rret);

            if ( rret != CHUNKSIZE )
            {
                perror ("io read failed");
                return -4;
            }

            rtot += rret;
        }

        if ( wlen > 0 )
        { 
            wret = write  (wfd, wbuf, CHUNKSIZE); 
         // fprintf (stderr, "write (%d %ld %ld) = %ld\n", wfd, wbuf, CHUNKSIZE, wret);

            if ( wret != CHUNKSIZE )
            {
                perror ("io write failed");
                return -4;
            }

            wtot += wret;
        }
    }
  
    /* clear disk cache */
 // (void) syncfs (rfd); 
 // (void) syncfs (wfd); 
    (void) sync ();

    free  (rbuf);
    free  (wbuf);
    close (rfd);
    close (wfd);
  
 // (void) unlink (tgt);

    if ( PROFILE )
    {
        struct rusage ru;

        if ( 0 != getrusage (RUSAGE_SELF, &ru) )
        {
            fprintf (stderr, "no ru: %s", strerror (errno));
            return (1);
        }

        size_t bs = get_blocksize();

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
        fprintf (stdout, "ru.inbytes       : %ld\n",     ru.ru_inblock*bs    ); 
        fprintf (stdout, "ru.inbytes_app   : %ld\n",     rtot                ); 
        fprintf (stdout, "ru.outblock      : %ld\n",     ru.ru_oublock       ); /* block output operations */
        fprintf (stdout, "ru.outbytes      : %ld\n",     ru.ru_oublock*bs    ); 
        fprintf (stdout, "ru.outbytes_app  : %ld\n",     wtot                ); 
        fprintf (stdout, "ru.msgsnd        : %ld\n",     ru.ru_msgsnd        ); /* IPC messages sent */
        fprintf (stdout, "ru.msgrcv        : %ld\n",     ru.ru_msgrcv        ); /* IPC messages received */
        fprintf (stdout, "ru.nsignals      : %ld\n",     ru.ru_nsignals      ); /* signals received */
        fprintf (stdout, "ru.nvcsw         : %ld\n",     ru.ru_nvcsw         ); /* voluntary context switches */
        fprintf (stdout, "ru.nivcsw        : %ld\n",     ru.ru_nivcsw        ); /* involuntary context switches */
    }

    return (0);
}


