
int _atom_compute_asm (long        flops);
int _atom_compute     (long        flops);
int _atom_time        (double      time);
int _atom_memory      (long        size);
int _atom_storage     (const char* src, 
                       long        rsize, 
                       const char* tgt, 
                       long        wsize);
int _atom_network     (const char* type, 
                       const char* mode, 
                       const char* host, 
                       int         port, 
                       long        size);

