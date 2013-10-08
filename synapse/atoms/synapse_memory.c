
#include <stdlib.h>

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

  /* make sure the memory actually got allocated */
  unsigned long int i = 0;
  for ( i = 0; i < n; i++ ) {
    c[i] = '\0';
  }

  free (c);

  return 0;

}

