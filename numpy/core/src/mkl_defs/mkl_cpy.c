#include "mkl.h"
#include <stddef.h>

#define __THRESHOLD 262144
#define __UNIT_STRIDE 1
#define __8BYTES_ALIGNMENT_OFFSET(ptr) (((size_t) (ptr)) & 0x7)
#define MKL_INT_MAX ((size_t) (~((MKL_UINT) 0) >> 1))
#include "numpy/npy_common.h"

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
       cblas_dcopy(MKL_INT_MAX, src , __UNIT_STRIDE, dest, __UNIT_STRIDE);
       size -= MKL_INT_MAX;
       src += MKL_INT_MAX;
       dest += MKL_INT_MAX;
   }
   if (size > 0) {
        if (size >= __THRESHOLD) {
            cblas_dcopy(size, src , __UNIT_STRIDE, dest, __UNIT_STRIDE);
        } else {
            memmove(dest, src, size * sizeof(double));
        }
   }
}

//#define __DEBUG
void call_mkl_mv(void* destination, const void* source, size_t size, const char* file_name, const char* func_name, const int line_num) {
        char* dst = (char*) destination;
        const char* src = (const char*) source;
        if((size > __THRESHOLD) && (__8BYTES_ALIGNMENT_OFFSET(src) == __8BYTES_ALIGNMENT_OFFSET(dst)) && ((dst + size < src) || (src + size < dst)) && !is_tbb_enabled()) {
            // memory segments do not intersect, use threaded MKL BLAS copying functions
            size_t offset = __8BYTES_ALIGNMENT_OFFSET(8 - __8BYTES_ALIGNMENT_OFFSET(src));
            size_t rem_size, ch_size, n_ch = (size - offset) / sizeof(double);
            if (offset) {
                memmove(dst, src, offset);
            }

#           ifdef __DEBUG
            printf("%zu bytes to mkl-mv : %s (%s:%d)\n", size, func_name, file_name, line_num);
#           endif
            call_dcopy_chunked(n_ch, (double *) (src + offset), (double*) (dst + offset));

            ch_size = offset + n_ch * sizeof(double);
            rem_size = size - ch_size;
            if(rem_size > 0) {
                memmove(dst + ch_size, src + ch_size, rem_size);
            }
        } else {
                memmove(dst, src, size);
        }
}

void call_mkl_cpy(void* destination, const void* source, size_t size, const char* file_name, const char* func_name, const int line_num) {
        char* dst = (char*) destination;
        const char* src = (const char*) source;
        if((size > __THRESHOLD) && (__8BYTES_ALIGNMENT_OFFSET(src) == __8BYTES_ALIGNMENT_OFFSET(dst)) && !is_tbb_enabled()) {
            size_t offset = __8BYTES_ALIGNMENT_OFFSET(8 - __8BYTES_ALIGNMENT_OFFSET(src));
            size_t rem_size, ch_size, n_ch = (size - offset) / sizeof(double);
            if (offset) {
                memcpy(dst, src, offset);
            }

#           ifdef __DEBUG
            printf("%zu bytes to mkl-cp : %s (%s:%d)\n", size, func_name, file_name, line_num);
#           endif
            call_dcopy_chunked(n_ch, (double *) (src + offset), (double*) (dst + offset));

            ch_size = offset + n_ch * sizeof(double);
            rem_size = size - ch_size;
            if(rem_size > 0) {
                memmove(dst + ch_size, src + ch_size, rem_size);
            }
        } else {
                memcpy(dst, src, size);
        }
}
