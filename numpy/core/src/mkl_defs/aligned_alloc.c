#include "mkl.h"
#include <stdlib.h>
#include <stddef.h>
#ifndef Py_PYTHON_H
#   include "Python.h"
#endif
#include "numpy/npy_common.h"

#define ALIGNMENT 64
#define __THRESHOLD 524288
#define __UNIT_STRIDE 1
#define __NULL_STRIDE 0
#define __8BYTES_ALIGNMENT_OFFSET(ptr) (((size_t) (ptr)) & 0x7)
#define MKL_INT_MAX ((size_t) (~((MKL_UINT) 0) >> 1))

#if defined(_MSC_VER)
#define posix_memalign(p, a, s) (((*(p)) = _aligned_malloc((s), (a))), *(p) ?0 :errno)
#endif
static int is_tbb_enabled(void) {
    static int TBB_ENABLED = -1;
    if (TBB_ENABLED == -1) {
            char* mkl_threading = getenv("MKL_THREADING_LAYER");
            TBB_ENABLED = (!mkl_threading || strncmp(mkl_threading, "TBB", 3) != 0 || strncmp(mkl_threading, "tbb", 3) != 0 ) ? 0 : 1;
    }
    return TBB_ENABLED;
}

static NPY_INLINE void call_dcopy_chunked(size_t size, double* src, double* dest) {
   while (size > MKL_INT_MAX) {
       cblas_dcopy(MKL_INT_MAX, src , __NULL_STRIDE, dest, __UNIT_STRIDE);
       size -= MKL_INT_MAX;
       dest += MKL_INT_MAX;
   }
   if (size > 0) {
       if (size >= __THRESHOLD) {
            cblas_dcopy(size, src , __NULL_STRIDE, dest, __UNIT_STRIDE);
       } else {
            memset(dest, 0, size * sizeof(double));
       }
   }
}

void * _aligned_alloc(size_t size) {
    /* Only available for Linux and OSX (has been explicitly disabled on Windows : see aligned_alloc.h)
     * With Windows, we would run into composability issues with modules like h5py which allocate
     * memory using libc functions in another library, like hdf5 for instance
     */
    size = (size > 0) ? size : 1;
    void* data = NULL;
    int ret_code = posix_memalign(&data, ALIGNMENT, size);
    if (ret_code == 0) {
        return data;
    }
    return NULL;
}


#ifdef WITH_ALIGNED_CALLOC
void * _aligned_calloc(size_t nelem, size_t elsize)
{
    size_t size = nelem * elsize;
    void *data = _aligned_alloc(size);
    char *memory = NULL;

    if (data != NULL) {
        memory = (char*) data;
        if((size > __THRESHOLD) && !is_tbb_enabled()) {
            size_t offset = __8BYTES_ALIGNMENT_OFFSET(8 - __8BYTES_ALIGNMENT_OFFSET(memory));
            size_t rem_size, ch_size, n_ch = (size - offset) / sizeof(double);
            double init = 0;
            if (offset) {
                memset(memory, 0, offset);
            }

            call_dcopy_chunked(n_ch, &init, (double*) (memory+offset));

            ch_size = offset + n_ch * sizeof(double);
            rem_size = size - ch_size;
            if(rem_size > 0) {
                memset(memory + ch_size, 0, rem_size);
            }
        } else {
                memset(memory, 0, size);
        }
    }
    return data;
}
#endif

#if PY_VERSION_HEX >= 0x03040000
static int is_tracemalloc_enabled(void) {
    static int TRACEMALLOC_PRESENT = -1;
    if (TRACEMALLOC_PRESENT == -1) {
        TRACEMALLOC_PRESENT = (getenv("PYTHONTRACEMALLOC")) ? 1 : 0;
    }
    return TRACEMALLOC_PRESENT;
}
#endif

void* call_aligned_malloc(size_t size) {
#if PY_VERSION_HEX >= 0x03040000
    if(is_tracemalloc_enabled()){
        return PyMem_RawMalloc(size);
    } else
#endif
    {
        return _aligned_alloc(size);
    }
}

void* call_aligned_realloc(void* input, size_t size) {
#if PY_VERSION_HEX >= 0x03040000
    if(is_tracemalloc_enabled()){
        return PyMem_RawRealloc(input, size);
    } else
#endif
    {
        if (input) {
          return realloc(input, size ? size : 1);
        }
        return _aligned_alloc(size);
    }
}

void* call_aligned_calloc(size_t num, size_t size) {
#if PY_VERSION_HEX >= 0x03040000
    if(is_tracemalloc_enabled()){
        return PyMem_RawCalloc(num, size);
    } else
#endif
    {
#ifdef WITH_ALIGNED_CALLOC
        return _aligned_calloc(num, size);
#else
        return calloc(num, size);
#endif
    }
}

void call_free(void* ptr) {
#if PY_VERSION_HEX >= 0x03040000
    if(is_tracemalloc_enabled()){
        PyMem_RawFree(ptr);
    } else
#endif
    {
        free(ptr);
    }
}
