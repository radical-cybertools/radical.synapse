
#include <stdio.h>
#include <stdlib.h>

#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>


#define CHUNKSIZE  (1024 * 1024)  /* 2^20 */

int main (int argc, char** argv)
{
    /* size */
    if ( argc < 2 )
    {
        return -1;
    }
  
    size_t n = atol   (argv[1]) * CHUNKSIZE;
    char*  c = malloc (n * sizeof(char));

    int fd   = open ("/tmp/t", O_CREAT);
    fprintf (stderr, "mem: %ld\n", n);
    char tmp[100];
    sprintf (tmp, "mem: %ld\n", n);
    write (fd, tmp, strlen(tmp));
    close (fd);
  
    /* make sure the memory actually got allocated */
    unsigned long int i = 0;
    for ( i = 0; i < n; i++ ) {
        c[i] = '\0';
        c[i]++;
    }
  
    free (c);
  
    return 0;
}

