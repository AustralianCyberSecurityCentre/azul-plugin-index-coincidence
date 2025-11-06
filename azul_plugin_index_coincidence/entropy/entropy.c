#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <math.h>

#define MIN_BLOCK_SIZE 256

struct entropy_block_info {
    unsigned int size;
    unsigned int count;
};

double entropy(const char *b, unsigned int sz)
{
    double answer;
    double pr;
    double result;
    unsigned int i;
    unsigned int cts[256];

    memset(cts, 0, sizeof(cts));

    for (i = 0; i < sz; i++) {
        cts[b[i] & 0xFF]++;
    }

    answer = 0.0;
    for (i = 0; i < 256; i++) {
        if (cts[i]) {
            pr = cts[i] / (double)sz;
	    __asm__ ("fyl2x" : "=t" (result) : "0" (pr), "u" (pr) : "st(1)");
            answer += result;
        }
    }

    if (answer == 0.0) {
        return 0.0;
    }
    return -answer;
}

static PyObject *entropies(const char *b, struct entropy_block_info *ebi)
{
    PyObject *ents;
    PyObject *py_ent;
    unsigned int i;
    double ent;

    // initialise the python list
    ents = PyList_New(ebi->count);
    if (!ents) {
        return NULL;
    }

    // calculate the entropy for each block in the buf
    for (i = 0; i < ebi->count; i++) {
        ent = entropy(&b[i * ebi->size], ebi->size);

        // build a float and put into the list
        py_ent = PyFloat_FromDouble(ent);
        if (!py_ent) {
            Py_DECREF(ents);
            return NULL;
        }
        PyList_SetItem(ents, i, py_ent);
    }

    // returning the python list of entropies
    return ents;
}

void get_ebi_byblocksize(unsigned int size, unsigned int block_size,
                         struct entropy_block_info *ebi)
{
    ebi->size = block_size < MIN_BLOCK_SIZE ? MIN_BLOCK_SIZE : block_size;
    ebi->count = size / ebi->size;
}

void get_ebi_bycount(unsigned int size, unsigned int count,
                     struct entropy_block_info *ebi)
{
    if (count == 0) {
        get_ebi_byblocksize(size, 0, ebi);
    } else {
        get_ebi_byblocksize(size, size / count, ebi);
    }
}

static PyObject *py_entropy(PyObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"buf", NULL};

    const char *b;
    Py_ssize_t n;
    double ent;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "s#", kwlist, &b, &n)) {
        return NULL;
    }

    // calculate the entropy
    ent = entropy(b, (unsigned int)n);

    // return the result
    return Py_BuildValue("d", ent);
}

static PyObject *py_block_entropies(PyObject *self, PyObject *args,
                                    PyObject *kwds)
{
    static char *kwlist[] = {"buf", "block_size", NULL};

    struct entropy_block_info ebi;
    PyObject *ents;
    const char *b;
    Py_ssize_t n;
    unsigned int block_size;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "s#I", kwlist,
                                     &b, &n, &block_size)) {
        return NULL;
    }

    if (n < MIN_BLOCK_SIZE) {
        ebi.size = 0;
        ebi.count = 0;
        ents = PyList_New(0);
    } else {
        // calculate the entropies
        get_ebi_byblocksize(n, block_size, &ebi);
        ents = entropies(b, &ebi);
    }

    // return the result
    return Py_BuildValue("[OII]", ents, ebi.size, ebi.count);
}

static PyObject *py_count_entropies(PyObject *self, PyObject *args,
                                    PyObject *kwds)
{
    static char *kwlist[] = {"buf", "count", NULL};

    struct entropy_block_info ebi;
    PyObject *ents;
    const char *b;
    Py_ssize_t n;
    unsigned int count;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "s#I", kwlist,
                                     &b, &n, &count)) {
        return NULL;
    }

    if (n < MIN_BLOCK_SIZE) {
        ebi.size = 0;
        ebi.count = 0;
        ents = PyList_New(0);
    } else {
        // calculate the entropies
        get_ebi_bycount(n, count, &ebi);
        ents = entropies(b, &ebi);
    }

    // return the result
    return Py_BuildValue("[OII]", ents, ebi.size, ebi.count);
}

PyDoc_STRVAR(module_doc,
    "Entropy\n"
    "\n"
    "Calculates the entropy for a given buffer of data\n");

PyDoc_STRVAR(entropy_doc,
    "entropy(buf)\n"
    "\n"
    "Calculates the shannon entropy of given bytes.");

PyDoc_STRVAR(block_entropies_doc,
    "block_entropies(buf, block_size)\n"
    "\n"
    "Return a list of entropies for this buffer, with block_size length.");
PyDoc_STRVAR(count_entropies_doc,
    "count_entropies(buf, count)\n"
    "\n"
    "Return a list of length block_count of entropies for this buffer.");

static PyMethodDef entropy_methods[] = {
    {"entropy", (PyCFunction)py_entropy,
     METH_VARARGS | METH_KEYWORDS, entropy_doc},
    {"block_entropies", (PyCFunction)py_block_entropies,
     METH_VARARGS | METH_KEYWORDS, block_entropies_doc},
    {"count_entropies", (PyCFunction)py_count_entropies,
     METH_VARARGS | METH_KEYWORDS, count_entropies_doc},
    {NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "_entropy",
    module_doc,
    0,
    entropy_methods,
    NULL,
    NULL,
    NULL,
    NULL
};

PyMODINIT_FUNC PyInit__entropy(void)
{
    return PyModule_Create(&moduledef);
}
#else
PyMODINIT_FUNC init_entropy(void)
{
    Py_InitModule3("_entropy", entropy_methods, module_doc);
}
#endif
