# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install phase0
#
# You can edit this file again by typing:
#
#     spack edit phase0
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *
import os
import glob


class Phase0(MakefilePackage):
    """
    PHASE-SYSTEM is a set of program packages for performing 
    simulations of nanosize materials. It consists of PHASE for 
    first-principles electronic structure calculations, UVSOR for 
    dielectric function calculations, ASCOT for quantum transport 
    property calculations, CIAO for all-electron calculations of an atom 
    and the generation of pseudopotentials, and PHASE Viewer, which is 
    a graphical user interface (GUI) for the PHASE package. 
    Note that PHASE-STSTEM, the one program package PHASE, and an executable 
    'phase' are different entities.
    """

    homepage = "https://azuma.nims.go.jp/"
    url      = "file://{0}/phase0_2023.01.tar.gz".format(os.getcwd())

    version('2023.01', sha256="c758d00ca71cbbd093a6f8d1d76dd02a0356e92fb9ea13d9b384a4897bf99ca9")
    version('2021.02', sha256="a7ae75aa236f3b3a9b485aa10b9dce0c23cdf3719719d1e1ee0027be9420e4eb")
    version('2021.01', sha256="70a3ad6614bb3f99510179bebbed9dcdc4a61578ce6d9b50a30108da4e8726dd")
    version('2019.02', sha256="e6b15ba8048b3c90d85487d4abfa5ae30658cdfe3bc7edb7615ca7735601c8f9")    

    variant("type", default="2d", description="parallel type",
            values=("2d", "3d"), multi=False)

    patch("2023.01_m_ES_nonlocal.F90.patch", when="@2023.01")
    patch("2023.01_b_XC_Potential.F90.patch", when="@2023.01")

    depends_on('mpi')
    depends_on('fftw-api@3')

    parallel = False


    def edit(self, spec, prefix):
        if "@2019.02" in spec:
            ver_str = "2019.02"
        elif "@2021.01" in spec:
            ver_str = "2021.01"
        elif "@2021.02" in spec:
            ver_str = "2021.02"
        elif "@2023.01" in spec:
            ver_str = "2023.01"
        #
        if "type=3d" in spec:
            makefile_src = join_path(os.path.dirname(self.module.__file__), 'Makefile.3d.'+ver_str)
            makefile     = join_path(self.stage.source_path, "src_phase_3d", 'Makefile')
        else:
            makefile_src = join_path(os.path.dirname(self.module.__file__), 'Makefile.2d.'+ver_str)
            makefile      = join_path(self.stage.source_path, "src_phase", 'Makefile')
        copy(makefile_src, makefile)

        if spec.satisfies("@2023.01"):
            os.rename("src_phase/ekmain.f90", "src_phase/ekmain.F90")

            

    @property
    def build_directory(self):
        if "type=3d" in self.spec:
            return "src_phase_3d"
        else:
            return "src_phase"


    @property
    def build_targets(self):
        if self.spec.satisfies("@2023.01"):
            targets = ["install",
                       "CC=mpifcc -Nnoclang",
        ]
        else:
            targets = [
                "install",
                "F90=mpifrt",
                "CC=mpifcc -Nnoclang",
                "CPP=",
                "AR=ar -vq",
                "LINK=mpifrt -Kfast,parallel,openmp,NOSVE",
                "CFLAGS=-Kfast,parallel,openmp -DINTEL",
                "ESM=yes",
                "CPPESM=-DENABLE_ESM_PACK",
                "LESM=-lesm",
            ]

            if "type=3d" in self.spec:
                targets.append("F90FLAGS=-Kfast,parallel,openmp,NOSVE -C 0")
                targets.append("F77FLAGS=-Kfast,parallel,openmp,NOSVE -C 0")
                targets.append("F90FLAGS_FIXED=-extend_source -Fl -fixed")
                targets.append("F90FLAGS_FREE=-extend_source -Fl")
                targets.append("CPPFLAGS=-DLinux -DFFTW3 -D_MPIFFT_ -D_USE_DATE_AND_TIME_ -D_POT_SMOOTHING_ -DTRANSPOSE -DGGA_ATOMIC_WITH_NEW_GNCPP -DREMOVE_PC_FROM_FORCE -D_USE_LAPACK_ -D_USE_SCALAPACK_ -D_POSITRON_ -D_FAST_WAY_ -DUSE_NONBLK_COMM -Dforsafe -D_HEAP_SORT_ -DFFT_ALLTOALL -DPOST3D -DUSE_NONBLK_COMM ${CPPESM}")
                targets.append("LIBS=-L./ -L"+self.spec['fftw-api'].prefix.lib+" ${LESM} -SCALAPACK -SSL2BLAMP -lfftw3 -lfftw3_omp -lfftw3_mpi")
            else:
                targets.append("F90FLAGS=-Kfast,parallel,openmp,NOSVE")
                targets.append("F77FLAGS=-Kfast,parallel,openmp,NOSVE")
                targets.append("F90FLAGS_FIXED=")
                targets.append("F90FLAGS_FREE=")
                targets.append("CPPFLAGS=-DLinux -DFFTW3 -D_POT_SMOOTHING_ -DTRANSPOSE -DGGA_ATOMIC_WITH_NEW_GNCPP -DREMOVE_PC_FROM_FORCE -D_USE_LAPACK_ -D_POSITRON_ -D_FAST_WAY_ -D_USE_DATE_AND_TIME_ -DUSE_NONBLK_COMM -DRMM_NONLOCAL_NEW ${CPPESM}")
                targets.append("LIBS=-L./ -L"+self.spec['fftw-api'].prefix.lib+" ${LESM} -SSL2 -lfftw3")

                targets.append("LFLAGS=")
                targets.append("MKLHOME=")
                targets.append("INCLUDE=-I"+self.spec['fftw-api'].prefix.include)
#        targets.append("LIBS=-L./ ${LESM} -SSL2 -lfftw3")

        return targets


    def install(self, spec, prefix):
#        make('install')
        if not "type=3d" in self.spec:
            os.remove(join_path(self.stage.source_path, "bin", "tdlrmain"))
        install_tree(join_path(self.stage.source_path, "bin"), prefix.bin)
