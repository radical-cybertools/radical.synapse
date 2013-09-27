
#include <errno.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>

int main (int argc, char** argv)
{
  if ( argc < 3 )
  {
    return -1;
  }

  /* storage target */
  char*  tgt  =        argv[1];
  off_t  n    = atol  (argv[2]) * 1024 * 1024;  /* 2^20 (MByte) */

  int    fd   = open  (tgt, O_CREAT | O_TRUNC | O_WRONLY, S_IRWXU);
  if ( fd < 0 )
  {
    perror ("open failed");
    return -2;
  }

  off_t off = 1024;
  off_t cnt = 0;

  while ( off < (n+1) )
  {
    off_t  sret = lseek (fd, off-2, SEEK_SET);

    if ( sret != off-2 )
    {
      perror ("lseek failed");
      return -3;
    }

    size_t wret = write (fd, "x\n", 2);

    if ( wret != 2 )
    {
      perror ("write failed");
      return -4;
    }


    off += 1024;
    cnt += 1;

    /*
    if ( 0 == (cnt % 1024) )
    {
      fprintf (stdout, ".");
      fflush  (stdout);
    }
    */
  }

  /*
  fprintf (stdout, "\n");
  */

  close (fd);

  return (0);

}

