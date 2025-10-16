# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack_repo.builtin.packages.fftw.package import FftwBase

from spack.package import *

class RistFftw(FftwBase):
    """FFTW is a C subroutine library for computing the discrete Fourier
    transform (DFT) in one or more dimensions, of arbitrary input
    size, and of both real and complex data (as well as of even/odd
    data, i.e. the discrete cosine/sine transforms or DCT/DST). We
    believe that FFTW, which is free software, should become the FFT
    library of choice for most applications."""

    _name = "rist-fftw"
    homepage = "https://www.fftw.org"
    url = "https://www.fftw.org/fftw-3.3.4.tar.gz"
    list_url = "https://www.fftw.org/download.html"

    license("GPL-2.0-or-later")

    version("3.3.10", sha256="56c932549852cddcfafdab3820b0200c7742675be92179e59e6215b340e26467")
    version("3.3.9", sha256="bf2c7ce40b04ae811af714deb512510cc2c17b9ab9d6ddcf49fe4487eea7af3d")
    version('3.3.9-273-g51f7529b', sha256='9d0162977ab039a7b34b575a0ac13eccc09641e223bb8c7e10a660b8f92e707e')
    version('3.3.9-272-g63d6bd70', sha256='19b1708260497c54660b074a17397e48f74d9dbc83ead7cb8e58d9f68bd6cfb9')
    version('3.3.9-271-g47423b75', sha256='3d3f25719283c6bb32e672e565ad137f1b6a53d1dbc3594659afb87159f97b8e')
    version('3.3.9-270-gd7bb52ed', sha256='d7c7c36d85e23b648a5fcb1b62bdadf4ac8d77e013bd6a8b1738fc49923684a7')
    version("3.3.8", sha256="6113262f6e92c5bd474f2875fa1b01054c4ad5040f6b0da7c03c98821d9ae303")
    version("3.3.7", sha256="3b609b7feba5230e8f6dd8d245ddbefac324c5a6ae4186947670d9ac2cd25573")
    version("3.3.6-pl2", sha256="a5de35c5c824a78a058ca54278c706cdf3d4abba1c56b63531c2cb05f5d57da2")
    version("3.3.5", sha256="8ecfe1b04732ec3f5b7d279fdb8efcad536d555f9d1e8fabd027037d45ea8bcf")
    version("3.3.4", sha256="8f0cde90929bc05587c3368d2f15cd0530a60b8a9912a8e2979a72dbe5af0982")
    version("2.1.5", sha256="f8057fae1c7df8b99116783ef3e94a6a44518d49c72e2e630c24b689c6022630")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant(
        "pfft_patches",
        default=False,
        description="Add extra transpose functions for PFFT compatibility",
    )

    depends_on("automake", type="build", when="+pfft_patches")
    depends_on("autoconf", type="build", when="+pfft_patches")
    depends_on("libtool", type="build", when="+pfft_patches")

    provides("fftw-api@2", when="@2.1.5")
    provides("fftw-api@3", when="@3:")

    patch("pfft-3.3.9.patch", when="@3.3.9:+pfft_patches", level=0)
    patch(
        "https://github.com/FFTW/fftw3/commit/f69fef7aa546d4477a2a3fd7f13fa8b2f6c54af7.patch?full_index=1",
        sha256="872cff9a7d346e91a108ffd3540bfcebeb8cf86c7f40f6b31fd07a80267cbf53",
        when="@3.3.7:",
    )
    patch("pfft-3.3.5.patch", when="@3.3.5:3.3.8+pfft_patches", level=0)
    patch("pfft-3.3.4.patch", when="@3.3.4+pfft_patches", level=0)
    patch("intel-configure.patch", when="@3:3.3.8%intel", level=0)
