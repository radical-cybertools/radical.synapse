
/* -----------------------------------------------------------------------------
 */

#include <time.h>
#include <Python.h>
#include "unistd.h"
#include "atoms.h"


/* -----------------------------------------------------------------------------
 */
static char module_docstring[] =
"Provide C-Atoms for radical.synapse";


/* -----------------------------------------------------------------------------
 */
/* Available functions */
static PyObject *atom_compute_asm (PyObject * self, PyObject * args);
static PyObject *atom_compute     (PyObject * self, PyObject * args);
static PyObject *atom_time        (PyObject * self, PyObject * args);
static PyObject *atom_memory      (PyObject * self, PyObject * args);
static PyObject *atom_storage     (PyObject * self, PyObject * args);
static PyObject *atom_network     (PyObject * self, PyObject * args);

static PyObject* atom_simple_adder  (PyObject *self, PyObject *args);
static PyObject* atom_mat_mult      (PyObject *self, PyObject *args) __attribute((optimize("-O0")));


/* -----------------------------------------------------------------------------
 */
static PyMethodDef module_methods[] = {
    {"atom_compute_asm",  atom_compute_asm  , METH_VARARGS, NULL},
    {"atom_compute",      atom_compute      , METH_VARARGS, NULL},
    {"atom_time",         atom_time         , METH_VARARGS, NULL},
    {"atom_memory",       atom_memory       , METH_VARARGS, NULL},
    {"atom_storage",      atom_storage      , METH_VARARGS, NULL},
    {"atom_network",      atom_network      , METH_VARARGS, NULL},
    {"atom_simple_adder", atom_simple_adder , METH_VARARGS, NULL},
    {"atom_mat_mult",     atom_mat_mult     , METH_VARARGS, NULL},
    {NULL, NULL, 0, NULL}
};


/* -----------------------------------------------------------------------------
 */
PyMODINIT_FUNC
init_atoms (void)
{
    PyObject *m = Py_InitModule3 ("_atoms", module_methods, module_docstring);
    if (m == NULL)
        fprintf (stderr, "Py_InitModule3 failed\n");
    return;
}


/* -----------------------------------------------------------------------------
 */
static PyObject *
atom_compute_asm (PyObject * self, PyObject * args)
{
    long flops = 0;
    long time  = 0;

    if ( ! PyArg_ParseTuple (args, "ll", &flops, &time) )
        return NULL;

    _atom_compute_asm (flops, time);
    Py_RETURN_NONE;
}


/* -----------------------------------------------------------------------------
 */
static PyObject *
atom_compute (PyObject * self, PyObject * args)
{
    long flops = 1;

    if ( ! PyArg_ParseTuple (args, "l", &flops) )
        return NULL;

    _atom_compute (flops);
    Py_RETURN_NONE;
}


/* -----------------------------------------------------------------------------
 */
static PyObject *
atom_time (PyObject * self, PyObject * args)
{
    double time = 0.0;

    if ( ! PyArg_ParseTuple (args, "d", &time) )
        return NULL;

    _atom_time(time);
    Py_RETURN_NONE;
}


/* -----------------------------------------------------------------------------
 */
static PyObject *
atom_memory (PyObject * self, PyObject * args)
{
    long size = 1;

    if ( ! PyArg_ParseTuple (args, "l", &size) )
        return NULL;

    _atom_memory (size);
    Py_RETURN_NONE;
}


/* -----------------------------------------------------------------------------
 */
static PyObject *
atom_storage (PyObject * self, PyObject * args)
{
    char * src;
    long   rsize =  1;
    char * tgt;
    long   wsize =  1;
    long   buf   =  0;

    if ( ! PyArg_ParseTuple (args, "slsll", &src, &rsize, &tgt, &wsize, &buf) )
        return NULL;

    _atom_storage (src, rsize, tgt, wsize, buf);
    Py_RETURN_NONE;
}


/* -----------------------------------------------------------------------------
 */
static PyObject *
atom_network (PyObject * self, PyObject * args)
{
    char * type = "";
    char * mode = "";
    char * host = "";
    int    port = 1;
    long   size = 1;

    if ( ! PyArg_ParseTuple (args, "sssil", &type, &mode, &host, &port, &size) )
        return NULL;

    // FIXME
    return NULL; 
    _atom_network (type, mode, host, port, size);
    Py_RETURN_NONE;
}


/* -----------------------------------------------------------------------------
 */
static PyObject* 
atom_simple_adder(PyObject *self, PyObject *args)
{
    // args provide the number of flops to implement

    // The number of flops to emulate is an input argument to 'args'
    // The kernel called emulates a fixed number of cycles. We emulate
    //  the designated number of cycles to emulate by specifying the 
    //  number of times (iter) to run the loop

    long cycles;
    long iter;

	const long cycles_per_iter = 8;

    if (!PyArg_ParseTuple(args, "l", &cycles)) { return NULL; }

    iter = flops / cycles_per_iter;
    _simple_adder(iter);

    Py_RETURN_NONE;
}


static PyObject*
atom_mat_mult(PyObject *self, PyObject *args)
{

    long cycles;
    volatile int len;

	const long cycles_per_iter = 1;

    if (!PyArg_ParseTuple(args, "li", &flops, &len)) { return NULL; }

    int iter = flops / cycles_per_iter; // And some other stuff

    int size = len*len;
    //printf("size %d\n", len);
    volatile int *A = (int*) malloc(size * sizeof(int));
    volatile int *B = (int*) malloc(size * sizeof(int));
    volatile int *C = (int*) malloc(size * sizeof(int));

    _mat_mult(iter, A, B, C, len);

    free((void*) A);
    free((void*) B);
    free((void*) C);

    Py_RETURN_NONE;
}

/* -----------------------------------------------------------------------------
 */

static void _simple_adder(long iter)
{
    clock_t start, end;
    double cpu_time_used;

    start = clock();

    long i;
    for (i = 0; i < iter; i++)
    {
        {
        __asm__ __volatile__
            (
            "addl %%eax, %%eax \n\t"
            "addl %%ebx, %%ebx \n\t"
            "addl %%ecx, %%ecx \n\t"
            "addl %%edx, %%edx \n\t"
            : /* outputs */
            : /* inputs */
            : /* clobbered */ "eax", "ebx", "ecx", "edx"
            );
        }
    }
    
    end = clock();
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    printf("time for _simple atom to execute: %f (s)\n", cpu_time_used);
}

/* -----------------------------------------------------------------------------
 */
static void _mat_mult(long iter, volatile int *A, volatile int *B, volatile int *C, volatile int len)
{

    //clock_t start, end;
    //double cpu_time_used;

    //start = clock();

    volatile int i, j, k;

    for (i = 0; i < len; i++)
    {
        for (j = 0; j < len; j++)
        {
            for (k = 0; k < len; k++)
            {
                //printf("%d %d %d\n", i, j, k);
                C[i*len + j] += (A[i*len + k] * B[k*len + j]);
            }
        }
    }

    //end = clock();
    //cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    //printf("time for _mat_mult atom to execute: %f (s)\n", cpu_time_used);
}



