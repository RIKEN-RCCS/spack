# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class FujitsuMpi(Package):
    """Fujitsu MPI implementation only for Fujitsu compiler."""

    homepage = "https://www.fujitsu.com/us/"

    conflicts("%arm")
    conflicts("%cce")
    conflicts("%apple-clang")
    #conflicts("%clang")
    #conflicts("%gcc")
    conflicts("%intel")
    conflicts("%nag")
    conflicts("%pgi")
    conflicts("%xl")
    conflicts("%xl_r")

    depends_on("c")
    depends_on("cxx")
    depends_on("fortran")

    provides("mpi@3.1:")

    def install(self, spec, prefix):
        raise InstallError("Fujitsu MPI is not installable; it is vendor supplied")

    @property
    def headers(self):
        hdrs = find_headers("mpi", self.prefix.include, recursive=True)
        hdrs.directories = os.path.dirname(hdrs[0])
        return hdrs or None

    @property
    def libs(self):
        query_parameters = self.spec.last_query.extra_parameters
        libraries = ["libmpi"]

        if "cxx" in query_parameters:
            libraries = ["libmpi_cxx"] + libraries

        return find_libraries(libraries, root=self.prefix, shared=True, recursive=True)

    def setup_dependent_package(self, module, dependent_spec):
        if self.spec.satisfies("%gcc"):
            self.spec.mpicc = self.prefix.bin.mpicc
            self.spec.mpicxx = self.prefix.bin.mpicxx
            self.spec.mpif77 = self.prefix.bin.mpifort
            self.spec.mpifc = self.prefix.bin.mpifort
        elif self.spec.satisfies("%fj"):
            self.spec.mpicc = self.prefix.bin.mpifcc
            self.spec.mpicxx = self.prefix.bin.mpiFCC
            self.spec.mpif77 = self.prefix.bin.mpifrt
            self.spec.mpifc = self.prefix.bin.mpifrt
        elif self.spec.satisfies("%llvm"):
            self.spec.mpicc = self.prefix.bin.mpiclang
            self.spec.mpicxx = self.prefix.bin.join("mpiclang++")
            self.spec.mpif77 = self.prefix.bin.mpiflang
            self.spec.mpifc = self.prefix.bin.mpiflang

    def setup_dependent_build_environment(
        self, env: EnvironmentModifications, dependent_spec: Spec
    ) -> None:
        # Use the spack compiler wrappers under MPI
        dependent_module = dependent_spec.package.module
        for var_name, attr_name in (
            ("OMPI_CC", "spack_cc"),
            ("OMPI_CXX", "spack_cxx"),
            ("OMPI_FC", "spack_fc"),
            ("OMPI_F77", "spack_f77"),
        ):
            if hasattr(dependent_module, attr_name):
                env.set(var_name, getattr(dependent_module, attr_name))
        if self.spec.satisfies("%gcc"):
            env.set("MPI_C_COMPILER", self.prefix.bin.mpicc)
            env.set("MPI_CXX_COMPILER", self.prefix.bin.mpicxx)
            env.set("MPI_Fortran_COMPILER", self.prefix.bin.mpifort)
        elif self.spec.satisfies("%fj"):        
            env.set("MPI_C_COMPILER", self.prefix.bin.mpifcc)
            env.set("MPI_CXX_COMPILER", self.prefix.bin.mpiFCC)
            env.set("MPI_Fortran_COMPILER", self.prefix.bin.mpifrt)
        elif self.spec.satisfies("%llvm"):
            env.set("MPI_C_COMPILER", self.prefix.bin.mpiclang)
            env.set("MPI_CXX_COMPILER", self.prefix.bin.join("mpiclang++"))
            env.set("MPI_Fortran_COMPILER", self.prefix.bin.mpiflang)

    def setup_run_environment(self, env):
        # Because MPI are both compilers and runtimes, we set up the compilers
        # as part of run environment
        if self.spec.satisfies("%gcc"):
            env.set("MPICC", self.prefix.bin.mpicc)
            env.set("MPICXX", self.prefix.bin.mpicxx)
            env.set("MPIF77", self.prefix.bin.mpifort)
            env.set("MPIF90", self.prefix.bin.mpifort)
            env.prepend_path("LD_LIBRARY_PATH", self.prefix.lib)
            env.prepend_path("LD_LIBRARY_PATH", self.prefix.lib64)
            env.set("OPAL_PREFIX", self.prefix)
        elif self.spec.satisfies("%fj"):
            env.set("MPICC", self.prefix.bin.mpifcc)
            env.set("MPICXX", self.prefix.bin.mpiFCC)
            env.set("MPIF77", self.prefix.bin.mpifrt)
            env.set("MPIF90", self.prefix.bin.mpifrt)
        elif self.spec.satisfies("%llvm"):
            env.set("MPICC", self.prefix.bin.mpiclang)
            env.set("MPICXX", self.prefix.bin.join("mpiclang++"))
            env.set("MPIF77", self.prefix.bin.mpiflang)
            env.set("MPIF90", self.prefix.bin.mpiflang)
            env.prepend_path("LD_LIBRARY_PATH", self.prefix.lib)
            env.prepend_path("LD_LIBRARY_PATH", self.prefix.lib64)
            env.set("OPAL_PREFIX", self.prefix)
            env.set("MPI_HOME", self.prefix)
