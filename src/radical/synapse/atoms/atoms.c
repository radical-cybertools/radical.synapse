
/* -----------------------------------------------------------------------------
 */
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION

#include "Python.h"
#include <stdlib.h>
#include <assert.h>
#include <stdbool.h>
#include <limits.h>


/* -----------------------------------------------------------------------------
 */
/* Available functions */
static PyObject *atom_compute_asm  (PyObject * self, PyObject * args);
static PyObject *atom_compute_test (PyObject * self, PyObject * args);
static PyObject *atom_compute      (PyObject * self, PyObject * args);
static PyObject *atom_time         (PyObject * self, PyObject * args);
static PyObject *atom_memory       (PyObject * self, PyObject * args);
static PyObject *atom_storage      (PyObject * self, PyObject * args);
static PyObject *atom_network      (PyObject * self, PyObject * args);


/* -----------------------------------------------------------------------------
 */
static PyMethodDef module_methods[] = {
    {"atom_compute_asm",  atom_compute_asm , METH_VARARGS, NULL},
    {"atom_compute_test", atom_compute_test, METH_VARARGS, NULL},
    {"atom_compute",      atom_compute     , METH_VARARGS, NULL},
    {"atom_time",         atom_time        , METH_VARARGS, NULL},
    {"atom_memory",       atom_memory      , METH_VARARGS, NULL},
    {"atom_storage",      atom_storage     , METH_VARARGS, NULL},
    {"atom_network",      atom_network     , METH_VARARGS, NULL},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef moduledef = {
       PyModuleDef_HEAD_INIT,
       "_atoms",
       "Provide C-Atoms for radical.synapse",
       -1,
       module_methods,
       NULL,
       NULL,
       NULL,
       NULL
};


/* -----------------------------------------------------------------------------
 */
PyObject *
PyInit__atoms(void){

    PyObject *module = PyModule_Create(&moduledef);

    if (module == NULL)
        return NULL;

    PyModule_AddStringConstant(module, "__author__", "Andre Merzky <andre@merzky.net>");
    PyModule_AddStringConstant(module, "__version__", "1.0.0");

    return module;
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
atom_compute_test (PyObject * self, PyObject * args)
{
    long flops = 0;
    long time  = 0;

    if ( ! PyArg_ParseTuple (args, "ll", &flops, &time) )
        return NULL;

    _atom_compute_test (flops, time);
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

