
int _atom_compute_asm (long        flops, 
                       long        time);
int _atom_compute     (long        flops);
int _atom_time        (double      time);
int _atom_memory      (long        size);
int _atom_storage     (const char* src, 
                       long        rsize, 
                       const char* tgt, 
                       long        wsize,
                       long        buf);
int _atom_network     (const char* type, 
                       const char* mode, 
                       const char* host, 
                       int         port, 
                       long        size);


//-----------------------------------------------

static void _simple_adder     (long           iter);
static void _mat_mult         (long           iter,
                               volatile float *A,
                               volatile float *B,
                               volatile float *C,
                               volatile long  len) __attribute__((optimize("O0")));
