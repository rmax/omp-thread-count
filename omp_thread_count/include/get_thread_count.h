#ifndef GET_THREAD_COUNT_H_   /* Include guard */
#define GET_THREAD_COUNT_H_

#include <omp.h>

int get_thread_count(void);

int get_thread_count(void) {
  int n = 0;
  #pragma omp parallel reduction(+:n)
  n += 1;
  return n;
}

#endif // GET_THREAD_COUNT_H_
