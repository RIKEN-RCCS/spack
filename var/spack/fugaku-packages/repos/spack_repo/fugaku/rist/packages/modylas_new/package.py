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
#     spack install modylas-new
#
# You can edit this file again by typing:
#
#     spack edit modylas-new
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

# from spack import *
import os

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *


class ModylasNew(CMakePackage):
    """
     The "MOlecular DYnamics Software for LArge Systems" (MODYLAS) is a general-purpose, molecular dynamics simulation program suited to the simulation of very large physical, chemical, and biological systems. MODYLAS supports most starndard molecular dynamics calculation algorithms. In particular, for the calculations of the long-range Coulombic interaction, a combination of the fast multipole method (FMM) and the Ewald method for multipoles appropriate for the periodic boundary condition can be used. For temperature and pressure control, the Nosé-Hoover chain and Andersen method, respectively, can be used, to generate NVT, and NPT ensembles. For the numeric integration to solve the Newton's equations of motion, the program uses the rRESPA, a multiple time-step algorithm. The distance constraints between atoms are treated by the SHAKE, RATTLE, and ROLL algorithms. The program can handle all-atom force fields such as the CHARMM22 with CMAP, CHARMM36 with CMAP. In the near futre, the AMBER, and OPLSAA will be supported. Further, the program will also support free-energy calculation algorithms based on the thermodynamic integration method.
    The program also equips several newly developed methods to execute highly parallelized molecular dynamics calculations. The program ensures excellent scalability by the use of algorithms that practically eliminate data copying for communications and arithmetic operations, algorithms with minimal communication latency, and a parallel bucket-relay communication algorithm for the upper-level multipole moments in the FMM. Moreover, the use of blocked arithmetic operations can avoid the need to reload data from memory to cache, ensuring very low cache-miss rates. A benchmark test on MODYLAS using 65,536 nodes of the K-computer showed that the overall calculation time per step including communications is 5 ms for a 10 million atom system. This means that the simulation of a 10 million atom system can progress by 35 ns per day. MODYLAS thus enables us to study large-scale real systems such as viruses, liposomes, protein aggregates, micelles, and polymers.
    """

    homepage = "https://www.modylas.org"
    url      = "file://{0}/MODYLAS_1.1.0.tar.gz".format(os.getcwd())

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    # FIXME: Add proper versions here.
    # version('1.1.0', sha256="d7c1f87d35bc74e32780b3e58a0866a9cbcda14f0a6196a3cf82c8062ad4bc9a")
    version('1.1.0', sha256="2b4fe31fadbc698c8a07e9aa21e1150a205ee776ac1894a17d1b721c3a153e7a")

    depends_on('fortran', type="build")

    variant("ff", default="charmm", 
                  description="Force field", 
                  values=("charmm", "gaff", "oplsaa"), 
                  multi=False,
    )
    
    # FIXME: Add dependencies if required.
    depends_on('cmake@3:', type="build")
    depends_on("mpi")

    parallel = False

    root_cmakelists_dir = "source"

    def cmake_args(self):
#        args = [
#            '-DCMAKE_Fortran_COMPILER=mpifrt',
#            '-DCMAKE_Fortran_FLAGS=-DCOMM_CUBE -DMPIPARA -DFJMPIDIR -DSYNC-COMM -DHALFDIRE -DONEPROC_AXIS -Kfast,simd=2,openmp,parallel,ocl,optmsg=2 -X9 -Qp,s,t',
#        ]
        # if "ff=charmm" in self.spec:
        #     args = [
        #         '-DCMAKE_Fortran_COMPILER=mpifrt',
        #         '-DCMAKE_Fortran_FLAGS=-Kfast,simd=2,openmp,parallel,ocl,optmsg=2 -X9 -Cpp',
        #     ]
        # elif "ff=gaff" in self.spec:
        #     args = [
        #         '-DCMAKE_Fortran_COMPILER=mpifrt',
        #         '-DCMAKE_Fortran_FLAGS=-Kfast,simd=2,openmp,parallel,ocl,optmsg=2 -X9 -Cpp -DOPLSAMBER -DGAFF',
        #     ]
        # else:
        #     args = [
        #         '-DCMAKE_Fortran_COMPILER=mpifrt',
        #         '-DCMAKE_Fortran_FLAGS=-Kfast,simd=2,openmp,parallel,ocl,optmsg=2 -X9 -Cpp -DOPLSAMBER',
        #     ]


        if self.spec.satisfies("%fj"):
            fortran_compiler = "mpifrt"
            # fortran_flags = " -Kfast,simd=2,openmp,parallel,ocl,optmsg=2 -X9 -Cpp"
            fortran_flags = " -Kfast,simd=2,openmp,parallel,ocl -X9 -Cpp"

            if self.spec.satisfies("ff=gaff"):
                fortran_flags += " -DOPLSAMBER -DGAFF"

            elif self.spec.satisfies("ff=oplsaa"):
                fortran_flags += " -DOPLSAMBER"

        ### for %gcc
        else:
            fortran_compiler = "mpif90"
            fortran_flags = " -O3 -ftree-vectorize -cpp"

            if self.spec.satisfies("ff=gaff"):
                fortran_flags += " -DOPLSAMBER -DGAFF"

            elif self.spec.satisfies("ff=oplsaa"):
                fortran_flags += " -DOPLSAMBER"
    
        args = [
            self.define("CMAKE_Fortran_COMPILER", fortran_compiler),
            self.define("CMAKE_Fortran_FLAGS", fortran_flags),
        ]

        return args

    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        pass

