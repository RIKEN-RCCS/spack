# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class Scale(MakefilePackage):
    """SCALE (Scalable Computing for Advanced Library and Environment) is
    a basic library for weather and climate model of the earth and planets
    aimed to be widely used in various models.
    The SCALE library is developed with co-design by researchers of
    computational science and computer science."""

    homepage = "https://scale.riken.jp/"
    url = "https://scale.riken.jp/archives/scale-5.4.4.tar.gz"

    maintainers("t-yamaura")

    license("BSD-2-Clause")

    version(
        "5.5.5",
        sha256="63347f7b6638c85020649a98e4036cf98bfbbbab481e1072db880b77034d8e90",
        preferred=True,
    )
    version("5.4.5", sha256="015323c54f84c071eaeef7d983a5c22c84f66a3bbbac28c44cbad9d9e28809eb")
    version("5.3.6", sha256="3ab0d42cdb16eee568c65b880899e861e464e92088ceb525066c726f31d04848")
    version("5.2.6", sha256="e63141d05810e3f41fc89c9eb15e2319d753832adabdac8f7c8dd7acc0f5f8ed")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("mpi@2:", type=("build", "link", "run"))
    depends_on("netcdf-c")
    depends_on("netcdf-fortran")
    depends_on("parallel-netcdf")
    depends_on("lapack")

    patch("fj-own_compiler.patch", when="@:5.4.5 %fj")
    patch("fj-own_compiler-rev.patch", when="@5.5.5 %fj")
    patch("fix_fillvalue.patch", when='@5.5.5')

    parallel = False

    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        env.set("PREFIX", self.prefix)

        if 'lapack' in self.spec:
            lapack_libs = self.spec['lapack'].libs.ld_flags
            env.set("SCALE_MATHLIB_LIBS", lapack_libs)
            env.set("SCALE_ENABLE_MATHLIB", "T")

    def build(self, spec, prefix):
        scale_sys_str = ""
        if self.spec.satisfies("platform=linux %gcc"):
            scale_sys_str = "Linux64-gnu-ompi"
        elif self.spec.satisfies("platform=linux %intel"):
            scale_sys_str = "Linux64-intel-impi"
        elif self.spec.satisfies("platform=linux target=arm %gcc"):
            scale_sys_str = "LinuxARM-gnu-ompi"
        elif self.spec.satisfies("platform=linux target=a64fx %fj"):
            scale_sys_str = "FUGAKU"
        elif self.spec.satisfies("platform=linux target=s64fx %fj"):
            scale_sys_str = "FX100"
        elif self.spec.satisfies("platform=darwin %gcc"):
            scale_sys_str = "MacOSX-gnu-ompi"

        if scale_sys_str == "":
            raise InstallError("unsupported arch and compiler combination.")
        env["SCALE_SYS"] = scale_sys_str

        nc_config = which("nc-config")
        nf_config = which("nf-config")

        # set SCALE_NETCDF_INCLUDE
        nc_str = nc_config("--cflags", output=str).strip()
        nf_str = nf_config("--fflags", output=str).strip()
        env["SCALE_NETCDF_INCLUDE"] = "{} {}".format(nc_str, nf_str)

        # set SCALE_NETCDF_LIBS
        nc_libs = nc_config("--libs", output=str).strip()
        nf_libs = nf_config("--flibs", output=str).strip()
        env["SCALE_NETCDF_LIBS"] = "{} {}".format(nc_libs, nf_libs)

        make()

    def install(self, spec, prefix):
        make("install")

        install_tree("bin", prefix.bin)
        install_tree("lib", prefix.lib)
        install_tree("doc", prefix.share.docs)
        install_tree(os.path.join("scale-rm", "test"), os.path.join(prefix.share, "test"))
