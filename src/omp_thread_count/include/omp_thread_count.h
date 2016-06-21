#ifndef OMP_THREAD_COUNT_H_   /* Include guard */
#define OMP_THREAD_COUNT_H_

#include <omp.h>

// Credits: http://stackoverflow.com/a/13328691/140510
int _omp_thread_count(void) {
  int n = 0;
  #pragma omp parallel reduction(+:n)
  n += 1;
  return n;
}

#endif // OMP_THREAD_COUNT_H_
