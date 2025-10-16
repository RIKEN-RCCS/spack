#!/bin/sh

export OMP_NUM_THREADS=1

umask 0002
. /vol0004/apps/oss/spack-v1.0.1/share/spack/setup-env.sh

export SPACK_DISABLE_LOCAL_CONFIG=true
export SPACK_USER_CACHE_PATH=/data/rist/r00017/Spack/v1.0.1/tmp/cache

#spack -d install py-phonopy@2.27.0
#spack spec py-phonopy@2.27.0
#spack -d install py-phonopy@2.27.0 ^python@3.11.6
#spack versions python
#spack spec py-phonopy@2.27.0 ^python@3.10.13

spack clean -a
spack -d install py-phonopy@2.27.0 ^py-h5py@3.10.0 ^py-mpi4py@3.1.4 ^py-numpy@1.26.4 ^py-scipy@1.11.3

