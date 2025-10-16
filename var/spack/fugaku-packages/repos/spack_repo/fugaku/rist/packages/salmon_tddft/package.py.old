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
#     spack install salmon-tddft
#
# You can edit this file again by typing:
#
#     spack edit salmon-tddft
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *
import os


class SalmonTddft(CMakePackage):
    """SALMON is an open-source computer program for ab-initio quantum-mechanical 
    calculations of electron dynamics at the nanoscale that takes place in 
    various situations of light-matter interactions. 
    It is based on time-dependent density functional theory, solving time-dependent 
    Kohn-Sham equation in real time and real space with norm-conserving pseudopotentials."""

    homepage = "https://salmon-tddft.jp/"
    url      = "http://salmon-tddft.jp/download/SALMON-v.2.0.2.tar.gz"

    version('2.1.0', sha256='18267818cdfa82ea762441e2d751abeff7b553c8ce92cabf5fb010248d2cfcbe')
    version('2.0.2', sha256='742007d3684a478199ba959ce135ad0020b70676a49f52a5e1dc25438123d50e')
    version('2.0.0', sha256='8086a32bd3986b63adfe4798e4c8077c7586d1dd023a57f1e1f7fb45ca0120a9')

    variant("build_type", default="Release", values=("Release", "Debug"))

    depends_on("cmake@3.14:", type="build")
    depends_on('mpi')

    parallel = False

    phases = ["edit", "cmake", "build", "install"]

    def edit(self, spec, prefix):
        if spec.satisfies('%fj'):
            config_file = join_path(self.stage.source_path, "platforms", "fujitsu-a64fx-ea.cmake")
            filter_file(r'-Nfjomplib', '-Nlibomp', config_file)
            filter_file(r'-SCALAPACK -SSL2BLAMP', '-SSL2BLAMP', config_file)
            filter_file(r'mpifrtpx', 'mpifrt', config_file)
            filter_file(r'mpifccpx', 'mpifcc', config_file)
            filter_file(r'-Kocl -Nlst=t -Koptmsg=2 -Ncheck_std=03s', '-Kocl -Nlst=t -Koptmsg=2 -Ncheck_std=03s -SCALAPACK', config_file)
            filter_file(r'-Kocl -Nlst=t -Koptmsg=2 -Xg -std=gnu99', '-Nclang -Kocl -Nlst=t -Koptmsg=2 -Xg -std=gnu99', config_file)
            test_cmakelist = join_path(self.stage.source_path, "testsuites", "CMakeLists.txt")
            filter_file(r'\${TEST_MPI_NPROC} \${CMAKE_BINARY_DIR}/\${TARGET_NAME}', '${TEST_MPI_NPROC} -stdin ./inputfile -of outputfile ${CMAKE_BINARY_DIR}/${TARGET_NAME}', test_cmakelist)
            create_test_cmake = join_path(self.stage.source_path, "cmakefiles", "create_test.cmake")
            filter_file(r'"\${TEST_COMMAND}" \'< ./inputfile \|& tee ./outputfile\'', '"${TEST_COMMAND}"', create_test_cmake)

    
    def cmake_args(self):
        spec = self.spec
        if spec.satisfies('%fj'):
            args = [
                "-DCMAKE_TOOLCHAIN_FILE:STRING=fujitsu-a64fx-ea",
                self.define("CMAKE_VERBOSE_MAKEFILE", False),
                self.define("USE_MPI", True),
                self.define("USE_SCALAPACK", True)
            ]
        else:
            args = []
        return args
