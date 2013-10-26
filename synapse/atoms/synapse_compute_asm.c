
#include <stdlib.h>
#include <stdio.h>

#define CHUNKSIZE  (1024 * 256)  /* 10^6 */

float mat_mult (float* a1, float* a2, int n);

int main (int argc, char** argv)
{
  /* size */
  if ( argc < 2 )
  {
    return -1;
  }

  size_t n = atol (argv[1]);
  float f[CHUNKSIZE];

  unsigned int i = 0;
  for ( i = 0; i < CHUNKSIZE; i++ ) 
  { 
    f[i] = i * 0.01;
  }

  for ( i = 0; i < n * 13; i++ ) 
  {
      mat_mult (f, f, CHUNKSIZE);
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

