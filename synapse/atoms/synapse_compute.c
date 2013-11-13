
#include <stdlib.h>

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

  return 0;
}

