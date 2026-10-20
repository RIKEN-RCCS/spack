#!/bin/bash
#PJM -L rscgrp=small
#PJM -L node=1
#PJM -L elapse=24:00:00
#PJM --llio localtmp-size=10Gi
#PJM --mpi "max-proc-per-node=1"
#PJM -x PJM_LLIO_GFSCACHE=/vol0004
#PJM -S

export OMP_NUM_THREADS=1

umask 0002
. /vol0004/apps/oss/spack-v1.0.1/share/spack/setup-env.sh

export SPACK_DISABLE_LOCAL_CONFIG=true
export SPACK_USER_CACHE_PATH=/data/rist/r00017/Spack/v1.0.1/tmp/cache

spack -d install -y --verbose --keep-stage openmx@3.9.9%fj@4.12.0 ^fujitsu-fftw@1.1.0
