# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class Alamode(CMakePackage):
    #eigen3_url="https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.tar.bz2"
    #spglib_url="https://github.com/spglib/spglib/archive/refs/tags/v1.16.2.tar.gz"

    homepage = "https://alamode.readthedocs.io/"
    #url      = "https://github.com/ttadano/alamode/archive/refs/tags/v.1.3.0.tar.gz"
    url      = "https://github.com/ttadano/alamode/archive/refs/tags/v.1.4.2.tar.gz"
    #url      = "/vol0004/apps/oss/spack-v0.19/var/spack/repos/local/packages/alamode/alamode-v.1.4.2.tar.gz"
    git      = "https://github.com/ttadano/alamode.git"

    #version("develop", branch="develop")
    #version("master", branch="master")
    version("1.5.0", commit="0a60844c48702639e2a9e2b2783f4d6d387ca1ae")

    version('1.4.2', sha256='18fb80a183c2a9b68488aeeccd6efa95e8c21d4cb21b08319a557389d55c067a')
    version('1.3.0', sha256='23ecc9f870dc28bf2d6efabb5a98b0d476f37231e8d5d9abdd9c87b11ac93d65')

    resource(
        name="eigen3",
        url="https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.tar.bz2",
        sha256="b4c198460eba6f28d34894e3a5710998818515104d6e74e5cc331ce31e46e626",
        destination="eigen3",
    )

    variant('build_type', default='RELEASE',
            description='CMake build type',
            values=('DEBUG', 'RELEASE'))

    depends_on('mpi')
    depends_on('blas')
    depends_on('lapack')
    depends_on('scalapack')
    depends_on('boost')
    depends_on('fftw')
    #depends_on('eigen3')
    depends_on('spglib')


    def cmake_args(self):
        define = CMakePackage.define
        spec = self.spec
        print("self.stage.source_path")
        print(self.stage.source_path)
        cmake_args = [
            '-DUSE_MKL_FFT=no',
            #'-DSPGLIB_ROOT=${SPGLIB_ROOT}',
            '-DEIGEN3_INCLUDE=%s/eigen3/eigen-3.4.0' % self.stage.source_path,
            '-DCMAKE_CXX_FLAGS="-O2"',
            '-DSCALAPACK_LIBRARIES=%s'    % spec['scalapack'].libs
        ]
        return cmake_args

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        src = join_path(self.build_directory, 'alm')
        b = 'alm'
        install(join_path(src, b), join_path(prefix.bin, b))
        src = join_path(self.build_directory, 'anphon' )
        b = 'anphon'
        install(join_path(src, b), join_path(prefix.bin, b))
        src = join_path(self.build_directory, 'tools')
        binaries = ['analyze_phonons', 'dfc2','fc_virtual','parse_fcsxml','qe2alm']
        for b in binaries:
            install(join_path(src, b), join_path(prefix.bin, b))
