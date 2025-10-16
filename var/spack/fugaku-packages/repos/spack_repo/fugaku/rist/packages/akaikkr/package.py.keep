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
from spack import *


class Akaikkr(MakefilePackage):
    """
    AkaiKKR (MACHIKANEYAMA) is a program package used for first-principles calculation of electronic structures of metals,
 semiconductors and compounds, in the framework of the local density approximation or generalized gradient approximation (
LDA/GGA) of the density functional theory.

    It exploits s function method. High speed, high accuracy and compactness are among its unique features. It is an all-electron method. It does not suffer from any serious truncation errors such as those of the plane-wave cutoff. Moreover AkaiKKR is combined with CPA (coherent potential approximation). Thus it is suitable not only for normal ordered crystals but also for disordered systems such as impurity systems, random substitutional alloys and mixed crystals. Since the method directly calculates the s function of the system, it can also provide a good starting point for first-principles linear response theory, many-body theory, and so on.

    The package has been continuously developed since late 70th and is still being developed by various authors. Each program in the package is written in FORTRAN 77. The package is completely self-contained and does not need any additional libraries. It runs equally well on a small note PC and a large supercomputer. Any platforms such as UNIX, Linux, Mac OS and Windows wherein the Fortran compiler is installed can be used.
    """

    homepage = "http://kkr.issp.u-tokyo.ac.jp/"
#    url = "file://{0}/cpa2002v010.tgz".format(os.getcwd())
#    url = "./cpa2002v010.tgz"
    url = "./cpa2021v001.tgz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

#    version('2021v001', sha256='a1a17d20d79d2474314610dce8d6739925f595857fb51cb53adf4a9b011f62d3', url="file://{0}/cpa2021.tgz".format(os.getcwd()))
    version('2021v001', sha256='a1a17d20d79d2474314610dce8d6739925f595857fb51cb53adf4a9b011f62d3')
    version('2002v010', sha256='e7de95110090f875634d71c5ff7f28d1ab4167231f16b97e3d0601dce75535bf')

    parallel = False

    patch("setomp.f.patch", when="@2002v010")
    patch("numcor.f.patch", when="@2002v010")
    patch("spmain.f.patch", when="@2002v010")

    build_targets = ["fort=frt"]
#    def build_targets(self):
#        return ["fort=frt"]

    def edit(self, spec, prefix):
        makefile=FileFilter('makefile')
        makefile.filter('omp = -fopenmp', 'omp = -Kopenmp')

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("specx", prefix.bin)

