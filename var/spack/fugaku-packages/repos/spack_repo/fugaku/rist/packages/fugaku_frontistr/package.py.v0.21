# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *
from spack.pkg.builtin.frontistr import FrontistrBase


class FugakuFrontistr(FrontistrBase):
    """This is a fork repository of the FrontISTR tuned for A64FX."""

    _name = "fugaku-frontistr"
    homepage = "https://www.frontistr.com/"
    git = "https://gitlab.com/FrontISTR-Commons/FrontISTR.git"
    maintainers = ["kinagaki-fj", "kinagaki", "m-shunji"]

    version("master", branch="fugaku")

    variant("static", default=True, description="Build with static linkage")
    depends_on("metis ~shared", when="+static")
    depends_on("mumps ~shared", when="+static")
    depends_on("trilinos ~shared", when="+static")

    def cmake_args(self):
        define = self.define
        args = super(FugakuFrontistr, self).cmake_args()
        if self.spec.satisfies("%fj"):
            args.extend(
                [
                    define(
                        "CMAKE_C_FLAGS", "-Kcmodel=large -Nlst=t -Kocl -Kfast -Kzfill -Koptmsg=2"
                    ),
                    define(
                        "CMAKE_CXX_FLAGS", "-Kcmodel=large -Nlst=t -Kocl -Kfast -Kzfill -Koptmsg=2"
                    ),
                    define(
                        "CMAKE_Fortran_FLAGS",
                        "-Kcmodel=large -Nlst=t -Kocl -Kfast -Kzfill -Koptmsg=2",
                    ),
                    define("CMAKE_Fortran_MODDIR_FLAG", "M"),
                    define("OpenMP_C_FLAGS", "-Kopenmp"),
                    define("OpenMP_CXX_FLAGS", "-Kopenmp"),
                    define("OpenMP_Fortran_FLAGS", "-Kopenmp"),
                ]
            )
        return args
