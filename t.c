
#include <stdlib.h>

int main()
{
  long int i, I = atol (getenv ("ITER")) * 1000000;
  double   f = 1.0;

  for (i = 0; i < I; i++ )
  {
    f = f * 1.000000000001;
  }
}




