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
#     spack install hphi
#
# You can edit this file again by typing:
#
#     spack edit hphi
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *
import os

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *

class Hphi(CMakePackage):
    """
    A numerical solver package for a wide range of quantum lattice models 
    including Hubbard-type itinerant electron hamiltonians, quantum spin models, 
    and Kondo-type hamiltonians for itinerant electrons coupled with quantum spins. 
    The Lanczos algorithm for finding ground states and newly developed Lanczos-based 
    algorithm for finite-temperature properties of these models are implemented for 
    parallel computing (hybrid parallelization with OpenMP and MPI). 
    A broad spectrum of users including experimental researchers is cordially welcome.
    """

    homepage = "http://issp-center-dev.github.io/HPhi/index_en.html"
    url      = "https://github.com/issp-center-dev/HPhi/releases/download/v3.5.1/HPhi-3.5.1.tar.gz"

    version('3.5.1', sha256='f4fa8b2d1a9688865be9e237f78fed2e72dfd5b65fc1ae3095d4c29e70cac320')
    version('3.4.0', sha256='bed245add87fe499e60427c6dbd17b0a2ccab68eba0dea04bb84a1fb61d30298')
#    version('3.4.0', sha256='bed245add87fe499e60427c6dbd17b0a2ccab68eba0dea04bb84a1fb61d30298', url="file://{0}/HPhi-3.4.0_offline.tar.gz".format(os.getcwd())) 
#    version('3.4.0', sha256='96274448fefe72fe0bf7bfff1fcb7515e2aefb6b7b9962783a0e4a13edcb8f8d')
    version('3.3.1', sha256='35f9e95c6bbaaf16c1c39b0ec61fc8fcbec68654b45143bc00c5a6643593ba96')
    version('3.3.0', sha256='c3e734b337bbfa9d1b3d3f3648ed725e1141a20036b1b8592f674b69f82594c2')
    version('3.2.0', sha256='6244bc76ecbbf468bc38628c98158b21ba1e3ebc54554399c3c11f55248b0212')
    version('3.1.2', sha256='f934ed7932a4d92951319567e84b9aacfd4fc04febcc4a7f46ae6f2514dfb18c')
    version('3.1.1', sha256='30b385313d3bdf7e8533b6cf1c7d7c59308cb0c86cfe20cadf42c9ece16aef13')
    version('3.1.0', sha256='0a38b0d70c7628e3e4f64ced225b27b87a32f502b6c895bd8b7923d9910fdd1e')
    version('3.0.0', sha256='b850b18b55cc7f75bdc83b5340aee23abd6ee93461d14f3e2e3c42995dbd335f')
    version('2.0.4', sha256='252decaf9c7938d4dd30737c481539b9aebc0e1f47dcc5ef112f5e3c74de1925')
    version('2.0.3', sha256='e8ee4848455ad23353c997e9864ea36855dfac601350318bec637c34535c2441')

    depends_on('mpi')
    depends_on("cmake@2.8.0:", type="build")

    depends_on("c", type="build")
    depends_on("fortran", type="build")

    variant("build_type", default="Release", values=("Debug", "Release"))

    patch("lanczos_spingc_hcor.sh.patch", sha256="d292cf20d26faddc53822247dc1d7508f4f959ae84e035c1f81e1428265b85b1", when='@3.4.0')
    patch("lobcg_spingc_hcor.sh.patch", sha256="565d56158929e3ceb4755252d15820974eceea46f05ef82955e3ff9ec6038627", when='@3.4.0')
    patch("testTECalc.py.patch", sha256="82a0245a451f945d0fddf42f7e5ba6e69853630a7ba8fc6601d7c71db3be589d", when='@3.4.0')
    

    parallel = False

    def cmake_args(self):
        if "@3.5.1" in self.spec:
            args = [
                self.define("USE_SCALAPACK", True),
                self.define("CMAKE_C_COMPILER", "mpifcc"),
                #self.define("CMAKE_C_FLAGS_RELEASE", "-Kfast,openmp -SCALAPACK -SSL2BLAMP -DMPI -DSCALAPACK -Nlst=t"),
                self.define("CMAKE_C_FLAGS_RELEASE", "-Nclang -O3 -ffj-fast-matmul -ffp-contract=fast -ffj-fp-relaxed -ffj-ilfunc -fbuiltin -fomit-frame-pointer -finline-functions -march=armv8.3-a+nosve -SCALAPACK -DMPI -DSCALAPACK"),
                self.define("OpenMP_C_FLAGS", "-fopenmp"),
                self.define("CMAKE_Fortran_COMPILER", "mpifrt"),
#                self.define("CMAKE_Fortran_FLAGS_RELEASE", "-DFUJITSU -DNDEBUG -Kfast,parallel"),
#                self.define("CMAKE_Fortran_FLAGS_RELEASE", "-fPIC -Kfast,parallel,NOSVE -SCALAPACK -SSL2BLAMP -DFUJITSU -DMPI -DSCALAPACK -Nlst=t"),
#                self.define("CMAKE_Fortran_FLAGS_RELEASE", "-DFUJITSU -DNDEBUG -Kfast,parallel,NOSVE -Nlst=t"),
                self.define("CMAKE_Fortran_FLAGS_RELEASE", "-fPIC -Kfast,NOSVE -SCALAPACK -SSL2BLAMP -DFUJITSU -DMPI -DSCALAPACK -Nlst=t"),
                self.define("OpenMP_Fortran_FLAGS", "-Kopenmp"),
#                self.define("BUILD_SHARED_LIBS", False),
#                self.define("BLAS_LIBRARIES", "-SSL2BLAMP"),
#                self.define("LAPACK_LIBRARIES", "-SSL2BLAMP"),
#                self.define("SCALAPACK_LIBRARIES", "-lmpi_mpifh -lfjscalapacksve -lfjlapacksve"),
#                self.define("SCALAPACK_LIBRARIES", "-lmpi_mpifh -lfjscalapack -lfjlapack"),
            ]
        else:
            args = [
                self.define("USE_SCALAPACK", True),
                self.define("CMAKE_C_COMPILER", "mpifcc"),
                self.define("CMAKE_C_FLAGS_RELEASE", "-DNDEBUG -Nclang -O3 -ffj-fast-matmul -ffp-contract=fast -ffj-fp-relaxed -ffj-ilfunc -fbuiltin -fomit-frame-pointer -finline-functions"),
                self.define("OpenMP_C_FLAGS", "-fopenmp"),
                self.define("CMAKE_Fortran_COMPILER", "mpifrt"),
                self.define("CMAKE_Fortran_FLAGS_RELEASE", "-DFUJITSU -DNDEBUG -Kfast,parallel"),
                self.define("OpenMP_Fortran_FLAGS", "-Kopenmp"),
                self.define("BUILD_SHARED_LIBS", False),
                self.define("BLAS_LIBRARIES", "-SSL2BLAMP"),
                self.define("LAPACK_LIBRARIES", "-SSL2BLAMP"),
                self.define("SCALAPACK_LIBRARIES", "-lmpi_mpifh -lfjscalapacksve -lfjlapacksve"),
            ]
        return args
