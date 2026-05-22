# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

class OmniCompiler(AutotoolsPackage):
    homepage = "https://omni-compiler.org"
    url      = "https://omni-compiler.org/download/stable/omnicompiler-1.3.3.tar.bz2"

    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('1.3.3', sha256='75a932c9d1d11f2e6b87983dd81c01e31cec3c40c65f259a0f8c51c6e0ba761f')

    depends_on('c', type='build')
    depends_on('cxx', type='build')
    depends_on('fortran', type='build')

    depends_on('openjdk')
    depends_on('libxml2')
#    depends_on('perl')
    depends_on('byacc')
    depends_on('flex')
    variant('mpi', default='internal', description='MPI library to use', values=('internal', 'openmpi', 'mpich'), multi=False)
    variant('system', default='defalut', description='System to use', values=('defalut', 'fugaku'), multi=False)
    depends_on('openmpi', when='mpi=openmpi')
    depends_on('mpich',   when='mpi=mpich')
    
    def configure_args(self):
        config_args = []
        if self.spec.satisfies('system=fugaku'):
            config_args.append('--target=Fugaku-linux-gnu')
        return config_args
            
    def install(self, spec, prefix):
        make('install')
