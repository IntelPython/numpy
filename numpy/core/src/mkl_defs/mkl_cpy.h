#ifdef __has_include
#   if __has_include("mkl.h") && !defined(MKL_CPY_H)
#       define MKL_CPY_H
#       include <stddef.h>
        void call_mkl_mv(void*, const void*, size_t, const char*, const char*, const int); 
        void call_mkl_cpy(void*, const void*, size_t, const char*, const char*, const int);
#       define memcpy(src, dst, size) call_mkl_cpy(src, dst, size, __FILE__, __func__, __LINE__)
#       define memmove(src, dst, size) call_mkl_mv(src, dst, size, __FILE__, __func__, __LINE__)
#   endif
#endif
