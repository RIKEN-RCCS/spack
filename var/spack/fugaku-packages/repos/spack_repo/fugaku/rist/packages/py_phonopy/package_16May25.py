# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPhonopy(PythonPackage):
    """Phonopy is an open source package for phonon
    calculations at harmonic and quasi-harmonic levels."""
    homepage = "https://atztogo.github.io/phonopy/index.html"
    url      = "https://github.com/phonopy/phonopy/archive/refs/tags/v2.20.0.tar.gz"
#    url      = "https://github.com/phonopy/phonopy/archive/refs/tags/v2.12.0.tar.gz"
#    git = "https://github.com/phonopy/phonopy.git"

    version('2.20.0', sha256='1dd47cb6e5b427d5cb88ce0b810b91f05533f434d53d22ea69eb974d4eb0ab46')
    version('2.12.0', sha256='a48d1f750e72da3c43c9a205572966b250f890311be2310c27f527056ba84648')
    version('1.10.0', sha256='6b7c540bbbb033203c45b8472696db02a3a55913a0e5eb23de4dc9a3bee473f7')

    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))

    depends_on('py-numpy@1.11:', type=('build', 'run'), when='@2.12.0')
    depends_on('py-matplotlib@2.0:', type=('build', 'run'), when='@2.12.0')
    depends_on('py-h5py', type=('build', 'run'), when='@2.12.0:')
    depends_on('py-spglib', type='run', when='@2.12.0:')
    depends_on('py-scipy@1.5.4:', type=('build', 'run'), when='@2.12.0:')

    depends_on('python@3.8:', type=('build', 'run'), when='@2.20.0')
    depends_on('py-numpy@1.15:', type=('build', 'run'), when='@2.20.0')
    depends_on('py-matplotlib@2.2.2:', type=('build', 'run'), when='@2.20.0')
    #depends_on('py-pyyaml@6.0.1', type=('build', 'run'), when='@2.20.0')
    #depends_on('py-h5py@3.10.0~mpi', type=('build', 'run'), when='@2.20.0')
    #depends_on('py-spglib@2.2.0', type='run', when='@2.20.0')
    #depends_on('py-scipy@1.10.1', type=('build', 'run'), when='@2.20.0')
        
#    depends_on('py-cp2k-input-tools', type=('build', 'run'), when='@2.12.0')
    
