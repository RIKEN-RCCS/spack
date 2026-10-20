import os
from spack.package import *
from spack_repo.builtin.build_systems.makefile import MakefilePackage

class QuantumEspresso(Package):
    """Quantum ESPRESSO is an integrated suite of Open-Source computer codes
    for electronic-structure calculations and materials modeling at the
    nanoscale. It is based on density-functional theory, plane waves, and
    pseudopotentials.
    """

    homepage = "http://quantum-espresso.org"
    url = "https://gitlab.com/QEF/q-e/-/archive/qe-6.6/q-e-qe-6.6.tar.gz"
    git = "https://gitlab.com/QEF/q-e.git"

    maintainers("ye-luo", "bellenlau", "tgorni")

    version("7.4.1", sha256="fd78ddb13f9ec08114b8bbc6e0b96f9c828da7a164add5987b09b8cbb432fae3",
            url="file://{0}/qe-7.4.1-ReleasePack.tar.gz".format(os.getcwd()))

    version("7.3.1", sha256="e0123582f7d76e343a2c4a95ff6a170efffd2471cd78211ea10b724fec27c18c",
            url="file://{0}/qe-7.3.1-ReleasePack.tar.gz".format(os.getcwd()))

    
    depends_on("c", type="build")
    depends_on("fortran", type="build")
    depends_on("fujitsu-fftw", type=("build", "link", "run"))
    depends_on("mpi")
    depends_on("gmake", type="build")

    patch("patch-qe-7.4.1.spack", level=1, when="@7.4.1")
    patch("patch-qe-7.3.1.spack", level=1, when="@7.3.1")

    def install(self, spec, prefix):
        prefix_path = prefix.bin if spec.satisfies("@:5.4.0") else prefix
        options = ["-prefix={0}".format(prefix_path)]

        options += [
            "--enable-parallel=yes",
            "--enable-openmp",
            "--with-scalapack=yes",
            "--host=aarch64-linux-gnu",
            "DFLAGS=-D__FFTW3 -D__SCALAPACK -D__MPI -D_OPENMP -Duse_beef",
            "IFLAGS=-I$(TOPDIR)/include -I$(TOPDIR)/FoX/finclude -I$(TOPDIR)/S3DE/iotk/include",
            "CFLAGS=-Nnoclang -Kfast,parallel,openmp,SVE -Knofp_relaxed",
            "CPPFLAGS=-traditional",
            "FFLAGS=-Kfast,parallel,openmp,SVE -Knofp_relaxed -Nalloc_assign -Nlst=t -Free",
            "LDFLAGS=-Kfast,parallel,openmp,SVE -Knofp_relaxed",
            "FC=mpifrt",
            "F90=frt",
            "CC=fcc",
            "BLAS_LIBS=-SSL2MPI -SSL2 -SSL2BLAMP",
            "LAPACK_LIBS=-SSL2MPI -SSL2 -SSL2BLAMP",
            "SCALAPACK_LIBS=-SSL2MPI -SSL2 -SSL2BLAMP -SCALAPACK",
            "FFT_LIBS=-lfftw3_mpi -lfftw3_omp -lfftw3",
            "FLIB_CNTL_BARRIER_ERR=FALSE"
        ]

        configure(*options)

        make("all", "epw", parallel=False)
        make("install")
