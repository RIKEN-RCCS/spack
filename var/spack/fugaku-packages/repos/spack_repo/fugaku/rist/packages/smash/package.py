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
#     spack install smash
#
# You can edit this file again by typing:
#
#     spack edit smash
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

import os
from spack_repo.builtin.build_systems.makefile import MakefilePackage
from spack.package import *

class Smash(MakefilePackage):
    """Scalable Molecular Analysis Solver for High-performance computing systems (SMASH)
    is massively parallel software for quantum chemistry calculations written in the 
    Fortran 90/95 language with MPI and OpenMP, and released under the Apache 2.0 
    open source license. Hartree-Fock and Density Functional Theory (DFT) calculations 
    can be performed on 100,000 CPU cores of K Computer with high parallel efficiency."""

    homepage = "http://smash-qc.sourceforge.net/"
#    url = "https://sourceforge.net/projects/smash-qc/files/smash-3.0.0.tgz"
#    url = "file://{0}/smash-2.2.0.tgz".format(os.getcwd())
    url = "file://{0}/smash-3.0.2.tgz".format(os.getcwd())
#    url = "file://{0}/smash-3.0.0.tgz".format(os.getcwd())

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('3.0.2', sha256='eeaaf6d3d4b787d06e20a96757eed927f39d536564f8b193c21dc07dbac623a9', url="file://{0}/smash-3.0.2.tgz".format(os.getcwd()))
    version('3.0.0', sha256='55b5ca63f910573a504dd026a34842eac09f405c24be825633eefb926923b978')
    version('2.2.0', sha256='b8122087d14ae36d4fbc72bfc32655243733e5fb8a1a92172df649e29c62214a')    
    version('1.1.0', sha256='3174342c43d9a4038e84bf84296ba9adacfd5a0b6bb71c8d7e70474ee0cf3b18')
    version('1.0.1', sha256='446a1079cf246c4aa512de2563fc2dfbe314c07a5361a652a425a59f39ce41e5')
    version('1.0',   sha256='7933ea3221675be6a0c34abf95c54c7015c10240ff33d79ed52fd10bfe087e0a')

    parallel = False

    depends_on("fortran", type="build")  # generated
    
    depends_on('mpi')

    def edit(self, spec, prefix):
        makefile_src = join_path(self.stage.source_path, 'Makefile.fujitsu')
        makefile_dst = join_path(self.stage.source_path, 'Makefile')
        copy(makefile_src, makefile_dst)
        filter_file(r'F90 = .*', 'F90 = mpifrt', makefile_dst)

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install(join_path(self.stage.source_path, "bin", "smash"), prefix.bin)
        
