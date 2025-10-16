# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fds(MakefilePackage):
    """
    Fire Dynamics Simulator (FDS) is a large-eddy simulation (LES) code for low-speed flows,
    with an emphasis on smoke and heat transport from fires.
    FDS and Smokeview are free and open-source software tools provided by the National Institute
    of Standards and Technology (NIST) of the United States Department of Commerce. Pursuant
    to Title 17, Section 105 of the United States Code, this software is not subject to copyright
    protection and is in the public domain. View the full disclaimer for NIST-developed software.
    """

    maintainers("kjrstory")
    homepage = "https://pages.nist.gov/fds-smv"
    url = "https://github.com/firemodels/fds/archive/refs/tags/FDS-6.8.0.tar.gz"
    git = "https://github.com/firemodels/fds.git"

    version("6.9.1", commit="889da6ae08d08dae680f7c0d8de66a3ad1c65375")
    version("6.8.0", commit="886e0096535519b7358a3c4393c91da3caee5072")    
    version("6.7.9", commit="ec52dee4274fcf994d358c8b0f883eec8f67e041")
    version("6.7.8", commit="fbf3e11eee06c89b85fcc936e592bcf27bb9827f")
    version("6.7.7", commit="fe0d4ef38f955b2a298ac9124ea3d8f085704edd")

    depends_on("mpi")
    depends_on("blas")

    requires(
        "%gcc",
        "%intel",
        "%oneapi",
        "%fj",
        policy="one_of",
        msg="FDS builds only with GNU, Intel or Fujitsu Fortran",
    )

    requires(
        "^intel-mpi^intel-mkl",
        when="%intel platform=linux",
        msg="Intel MPI and Intel MKL can only be used with Intel Fortran on Linux platform",
    )

    requires(
        "^intel-oneapi-mpi^intel-oneapi-mkl",
        when="%oneapi platform=linux",
        msg="Intel oneAPI MPI and MKL can only be used with oneAPI Fortran on Linux platform",
    )
    
    requires(
        "^openmpi%intel",
        when="platform=darwin",
        msg="OpenMPI can only be used with Intel Fortran on macOS",
    )

    # Added compile and link options for aarch64 to make files
    patch("modmakefile_arm_6.7.7.patch", when="@:6.7.7 target=aarch64:")
    patch("modmakefile_arm_6.7.9.patch", when="@6.7.8:6.8.0 target=aarch64:")
    
    # Modifications for Fujitsu compilers that do not support Fortran2018 format
    patch("fixf18_6.7.7_fj.patch", when="@:6.7.7%fj")
    patch("fixf18_6.7.9_fj.patch", when="@6.7.8:6.7.9%fj")
    patch("fixf18_6.8.0_fj.patch", when="@6.8.0%fj")

    # Modifications for gcc and fujitsu-mpi link error
    patch("fix_ompi_comm_op_eq_not_found_6.7.7.patch", when="@:6.7.7 %gcc ^fujitsu-mpi")
    patch("fix_ompi_comm_op_eq_not_found_6.7.9.patch", when="@6.7.8:6.8.0 %gcc ^fujitsu-mpi")

    # Apply patch made by FOCUS
    patch("focus-patch.fds6.9.1", when="@6.9.1%fj")
    
    build_directory = "Build"

    def edit(self, spec, prefix):
        if spec.satisfies("^mkl"):
            env["MKL_ROOT"] = self.spec["mkl"].prefix
        if spec.compiler.name == "oneapi":
            env["INTEL_IFORT"] = "ifx"
        makefile = FileFilter("Build/makefile")
        makefile.filter(r"\.\./Scripts", "./Scripts")
        makefile.filter(r"\.\.\\Scripts", ".\\Scripts")
        if spec.satisfies("target=aarch64: %gcc"):
            makefile.filter(r"LFLAGSMKL = ","LFLAGSMKL = {}"
           .format(spec["blas"].libs))

    @property
    def build_targets(self):
        spec = self.spec
        mpi_mapping = {"intel-oneapi-mpi": "impi", "intel-mpi": "impi"}
        mpi_mapping["openmpi"] = "ompi" if spec.satisfies("@6.7.8:") else "mpi"
        mpi_mapping["fujitsu-mpi"] = "fjmpi" if spec.satisfies("@6.7.8:") else "mpi"
        compiler_mapping = {"gcc": "gnu", "oneapi": "intel", "intel": "intel",
                            "fj": "fujitsu"}
        platform_mapping = {"linux": "linux", "darwin": "osx"}

        mpi_prefix = "mpi"
        if spec["mpi"].name in mpi_mapping.keys():
            mpi_prefix = mpi_mapping[spec["mpi"].name]
        compiler_prefix = compiler_mapping[spec.compiler.name]
        platform_prefix = platform_mapping[spec.architecture.platform]

        target = "{}_{}_{}".format(mpi_prefix, compiler_prefix, platform_prefix)
        if spec.satisfies("@:6.7.7"):
            arch_prefix = "arm" if spec.satisfies("target=aarch64: ") else "64"
            target += "_{}".format(arch_prefix)

        return [target]

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with working_dir(self.build_directory):
            install("*.mod", prefix.bin)
            install("*.o", prefix.bin)
            install("fds_" + self.build_targets[0], prefix.bin + "/fds")
