#if !defined(ALIGNED_ALLOC_H) && !defined(_MSC_VER)
#   define ALIGNED_ALLOC_H
#   include <stddef.h>
    inline void* call_aligned_malloc(size_t);
    inline void* call_aligned_realloc(void*, size_t);
    inline void* call_aligned_calloc(size_t, size_t);
    inline void call_free(void*);
#   define PyArray_malloc call_aligned_malloc 
#   define PyArray_free call_free
#   define PyArray_realloc call_aligned_realloc 
#endif
