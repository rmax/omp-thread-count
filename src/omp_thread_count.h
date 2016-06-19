#ifndef OMPUTILS_H_   /* Include guard */
#define OMPUTILS_H_

#include <omp.h>

int omp_thread_count(void);

int omp_thread_count(void) {
  int n = 0;
  #pragma omp parallel reduction(+:n)
  n += 1;
  return n;
}

#endif // OMPUTILS_H_

