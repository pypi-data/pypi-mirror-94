//#if !defined(__MINGW32__) || !defined(__MINGW64__) || !defined(__GNUC__)
//#error Must compile with MINGW
//#endif
#define PY_SSIZE_T_CLEAN

#include <Python.h>

#define __DOC__ ("\rLow level Module for colored terminal with ansi,\n" \
                 "\rWriten in C++ by Arman Ahmadi(at 'armanagha6@gmail.com')")
#define __NAME__ _colored

#define COMBINE(item, suffix) item##_##suffix
#define _COMBINE(child, parent) COMBINE(child, parent)
#define WITH_BASE(item) _COMBINE(item, __NAME__)

#define __force_inline __attribute__((always_inline))

#if defined(__WIN32) || defined(__WINNT)

#include <windows.h>

__attribute__((constructor))
static void __MAKE_CONSOLE_COLORED() {
    const HANDLE hConsoleHandle = GetStdHandle(-11);
    DWORD dwConsoleMode = 0;
    GetConsoleMode(hConsoleHandle, &dwConsoleMode);
    dwConsoleMode |= 4;
    SetConsoleMode(hConsoleHandle, dwConsoleMode);
}

#endif

enum LAYERS {
    Background = 48,
    Foreground = 38
};

__force_inline static inline void _beginColored(LAYERS layer) {
    printf("[%d;2;", layer);
}

__force_inline static inline void _setMod(short mode) {
    printf("[%dm", mode);
}

__force_inline static inline void _resetAll() {
    _setMod(0);
}

__force_inline static inline PyObject *ColoredBackground(PyObject *Py_UNUSED(ignoreSelf)) {
    _beginColored(Background);
    Py_RETURN_NONE;
}

__force_inline static inline PyObject *ColoredForeground(PyObject *Py_UNUSED(ignoreSelf)) {
    _beginColored(Foreground);
    Py_RETURN_NONE;
}

__force_inline static inline PyObject *ResetAll(PyObject *Py_UNUSED(ignoreSelf)) {
    _resetAll();
    Py_RETURN_NONE;
}

__force_inline  static inline PyObject *SetColor(PyObject *Py_UNUSED(ignoredSelf), PyObject *color) {
    PyObject
            *colorRGB;
    if (!PyArg_ParseTuple(color, "O!", &PyList_Type, &colorRGB)) return NULL;
    if (PyList_Size(colorRGB) != 3) {
        PyErr_SetString(PyExc_TypeError, "color must contain (R -> red, G -> Green, B -> blue)");
        return NULL;
    }
    unsigned char cColorsRGB[3];
    for (int i(0); i < 3; ++i) {
        PyObject
                *o = PyList_GetItem(colorRGB, i);
        unsigned char
                c;
        if (!PyLong_Check(o) || (c = PyLong_AsLong(o)) > 255 || c < 0) {
            PyErr_Format(PyExc_TypeError,
                         "invalid color(got \"%s\")!, mus be int and lower than 256 and equal bigger than 0",
                         PyUnicode_AsUTF8(PyUnicode_FromObject(o)));
            return NULL;
        }
        cColorsRGB[i] = c;
    }
    printf("%d;%d;%dm", // fg
           cColorsRGB[0], cColorsRGB[1], cColorsRGB[2]);
    Py_DECREF(colorRGB);
    Py_RETURN_NONE;
}

__force_inline static inline PyObject *Output(PyObject *Py_UNUSED(ignoredSelf), PyObject *_text) {
    char *text;
    if (!PyArg_ParseTuple(_text, "s", &text)) return NULL;
    printf("%s", text);
    fflush(stdout);
    Py_RETURN_NONE;
}

__force_inline static inline PyObject *SetMode(PyObject *Py_UNUSED(ignoredSelf), PyObject *_mode) {
    int mode;
    if (!PyArg_ParseTuple(_mode, "i", &mode)) return NULL;
    _setMod(mode);
    fflush(stdout);
    Py_RETURN_NONE;
}

static struct PyMethodDef METHODS[] = {
        {"begin_background", (PyCFunction) ColoredBackground, METH_NOARGS, "begin writing colored on background"},
        {"begin_foreground", (PyCFunction) ColoredForeground, METH_NOARGS, "begin writing colored on background"},
        {"reset", (PyCFunction) ResetAll, METH_NOARGS, "end printing colored"},
        {"set_color", (PyCFunction) SetColor, METH_VARARGS, "set color for current scope(bg or fg)"},
        {"set_mode", (PyCFunction) SetMode, METH_VARARGS, "set mode"},
        {"output", (PyCFunction) Output, METH_VARARGS, "print text with flush"}, \

        {nullptr}
};

static struct PyModuleDef
        COLORED = {PyModuleDef_HEAD_INIT,
                   "colored",
                   __DOC__,
                   0,
                   METHODS
};

PyMODINIT_FUNC WITH_BASE(PyInit)(void) {
    PyObject *m;

    m = PyModule_Create(&COLORED);
    if (m == NULL)
        goto fail;

    return m;
    fail:
    return NULL;
}
