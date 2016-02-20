
/* -----------------------------------------------------------------------------
 */
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


/* -----------------------------------------------------------------------------
 */
static PyMethodDef module_methods[] = {
    {"atom_compute_asm",  atom_compute_asm, METH_VARARGS, NULL},
    {"atom_compute",      atom_compute    , METH_VARARGS, NULL},
    {"atom_time",         atom_time       , METH_VARARGS, NULL},
    {"atom_memory",       atom_memory     , METH_VARARGS, NULL},
    {"atom_storage",      atom_storage    , METH_VARARGS, NULL},
    {"atom_network",      atom_network    , METH_VARARGS, NULL},
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
    long flops = 1;

    if ( ! PyArg_ParseTuple (args, "l", &flops) )
        return NULL;

    _atom_compute_asm (flops);
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

    if ( ! PyArg_ParseTuple (args, "slsl", &src, &rsize, &tgt, &wsize) )
        return NULL;

    _atom_storage (src, rsize, tgt, wsize);
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

