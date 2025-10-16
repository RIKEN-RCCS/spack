# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import os

class FfvhcAce(Package):
    """FFVHC-ACE is xxxxxxxxxxxxxxxxxxxxxxxxxxx. """

    url      = "file://{0}/FFVHC-ACE_20221110_toRIST.tar.gz".format(os.getcwd())

    version('1.0.0', sha256='e7609159d4d90b74601aa7426e083082c44e752be99f48a596dc6542a294840c', url="file://{0}/FFVHC-ACE_20221110_toRIST.tar.gz".format(os.getcwd()))

    depends_on('cmake@3.20.2', type='build')
    #depends_on('cmake@3:', type='build')

    def install(self, spec, prefix):
        with working_dir('Source/libs_ffv', create=False):
            if os.path.exists('CMakeCache.txt'): os.remove('CMakeCache.txt')
            filter_file(r'mpifccpx', 'mpifcc', 'install_lib.sh')
            filter_file(r'mpiFCCpx', 'mpiFCC', 'install_lib.sh')
            filter_file(r'mpifrtpx', 'mpifrt', 'install_lib.sh')
            filter_file(r'-D CMAKE_TOOLCHAIN_FILE=../cmake/Toolchain_fx100.cmake', '', 'install_lib.sh')
            filter_file(r'-Nrt_tune_io', '-Nrt_tune_io -Nnoclang', 'install_lib.sh')
            filter_file(r'openmp,visimpact', 'openmp,visimpact -Nnoclang', 'install_lib.sh')
            install_sh_lib = Executable('./install_lib.sh -s FX100 -f %s/libs/ -d' % self.stage.source_path)
            install_sh_lib()

        with working_dir('Source/src', create=False):
            if os.path.exists('CMakeCache.txt'): os.remove('CMakeCache.txt')
            filter_file(r'mpifccpx', 'mpifcc', 'cmake_run')
            filter_file(r'mpiFCCpx', 'mpiFCC', 'cmake_run')
            filter_file(r'mpifrtpx', 'mpifrt', 'cmake_run')
            filter_file(r'mpifrtpx', 'mpifrt', 'CMakeLists.txt')
            filter_file(r'Kfast,ocl,parallel,openmp', 'Kfast,ocl,parallel,openmp -Nnoclang', 'CMakeLists.txt')
            filter_file(r'Kopenmp,parallel', 'Kopenmp,parallel -Nnoclang', 'CMakeLists.txt')
            filter_file(r'Solver.h', 'Solver.h.in', 'FFV/makeModuleF90.py')
            os.system('awk \'{if(match($0,"MODULEF90")==0){sub("//.*$", "");} sub("\\r", "",$NF); print $0;}\' FFV/Solver.h > FFV/Solver.h.in')
            copy('FFV/modulef90.cpp.in', 'FFV/modulef90.cpp.in.org')
            os.system('awk \'{if(match($0,"begin")==0&&match($0,"end")==0){sub("//.*$", "");} sub("\\r", "",$NF); print $0;}\' FFV/modulef90.cpp.in.org > FFV/modulef90.cpp.in')
            install_sh = Executable('./cmake_run -s FX100 -f %s/libs/' % self.stage.source_path)
            install_sh()

            mkdirp(prefix.bin)
            install('FFV/ffv-hc-ace-NS', prefix.bin)
