# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os

class PyPhonopy(PythonPackage):
    """Phonopy is an open source package for phonon
    calculations at harmonic and quasi-harmonic levels."""
    homepage = "https://atztogo.github.io/phonopy/index.html"
#    url      = "https://github.com/phonopy/phonopy/archive/refs/tags/v2.12.0.tar.gz"
    url      = "file://{0}/v2.12.0.tar.gz".format(os.getcwd())
#    git = "https://github.com/phonopy/phonopy.git"

    version('2.12.0', sha256='a48d1f750e72da3c43c9a205572966b250f890311be2310c27f527056ba84648')
    version('1.10.0', sha256='6b7c540bbbb033203c45b8472696db02a3a55913a0e5eb23de4dc9a3bee473f7')

    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))

    depends_on('py-numpy@1.11:', type=('build', 'run'), when='@2.12.0')
    depends_on('py-matplotlib@2.0:', type=('build', 'run'), when='@2.12.0')
    depends_on('py-h5py', type=('build', 'run'), when='@2.12.0')
    depends_on('py-spglib', type='run', when='@2.12.0')
    depends_on('py-scipy@1.5.4:', type=('build', 'run'), when='@2.12.0')    
#    depends_on('py-cp2k-input-tools', type=('build', 'run'), when='@2.12.0')
    
