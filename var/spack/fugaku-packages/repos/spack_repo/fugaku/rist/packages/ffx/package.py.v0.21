# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import os

class Ffx(Package):
#    """FFX"""

    homepage = ""
    url      = "file://{0}/FFX.ver.03.01.tar.gz".format(os.getcwd())

    #version('03.01', sha256='83d5839d4fc83a55d1fa213f3c2167c2563be0b51eb5dcdc9b72703fd59dec10')
    #version('03.01', sha256='e1b13dba389cb045ac621ad0bb7b443f0011a0a19dda19eb027a69b6cd8e6dee')    
    version('03.01', sha256='796c96d13bee8b94ae71793c1a0cff2d1866fc74685dc87e222589c671e60984', \
                     url="file://{0}/FFX.ver.03.01.tar.gz".format(os.getcwd()))
    #version('59.01', sha256='4087d367af7d521417e5584ec6678c249f52c7dffd81fc126752547e324afb29')
    version('59.01', sha256='4087d367af7d521417e5584ec6678c249f52c7dffd81fc126752547e324afb29', \
                     url="file://{0}/FFX.ver.59.01.20221204.tar.gz".format(os.getcwd()))

    depends_on('mpi')

    #if spec.satisfies('@03.01'):
    phases = ['edit', 'build_libs', 'build_misc', 'build_lbm3d',  'build_lbm3dmpi', 'install_ffx']
    #elif spec.satisfies('@59.01'):
    #    phases = ['build_les', 'build_libs', 'build_lbm3dmpi']

    patch("lbm3d.f.patch", when="@03.01")
    patch("lbm3d.f.mpi.patch", when="@03.01")    
    #
    #
    #
    def setup_build_environment(self, env):
        env.set('LES3DHOME', self.stage.source_path)
        
    
    def edit(self, spec, prefix):
        if spec.satisfies("@03.01"):
            chmod = which("chmod")
            #
            make = join_path("make", "OPTION")
            m = FileFilter(make)
            m.filter(r'OPT\s=.*$', 'OPT = -Dcputime')
            m.filter(r'CPP\s*=.*$', 'CPP  = /usr/bin/cpp')
            m.filter(r'POPT\s=.*$', 'POPT = -P -traditional-cpp ${OPT}')
            m.filter(r'CCOM\s=.*$', 'CCOM = mpifcc')
            m.filter(r'COPT\s=.*$', 'COPT = -Nnoclang -Kvisimpact,ocl ${OPT} -Qt')
            m.filter(r'FCOM\s=.*$', 'FCOM = mpifrt')
            m.filter(r'FOPT\s=.*$', 'FOPT = -Kvisimpact,ocl ${OPT} -Qt -Cpp')
            m.filter(r'LINK\s=.*$', 'LINK = mpiFCC')
            m.filter(r'LOPT\s=.*$', 'LOPT = -Nnoclang --linkfortran -Kvisimpact ${OPT}')
            m.filter(r'LIBDIR\s=.*$', 'LIBDIR = {0}\n'.format(spec['mpi'].headers.directories[0]))
            m.filter(r'INCDIR\s=.*$', 'INCDIR = {0}\n'.format(spec['mpi'].libs.directories[0]))
            #
            make = join_path("lib", "src", "ParMetis-3.1", "Makefile.in")
            m = FileFilter(make)
            m.filter(r'CC\s=.*S', 'CC = mpifcc')
            m.filter(r'OPTFLAGS\s=.*S', 'OPTFLAGS = -Nnoclang -Kvisimpact')
            m.filter(r'INCDIR\s=.*S', 'INCDIR =')
            #
            make = join_path("util", "lbm3d.mpi", "FILES")
            m = FileFilter(make)
            m.filter(r'-lmpifort', '')
        else:
            pass
        #
        
        

    def build_les(self, spec, prefix):
        #
        # Create les3x.mpi
        #
        if spec.satisfies("@59.01"):
            print("Creating les3x.mpi")
            with working_dir('FFB/', create=False):
                filter_file(r'rm', 'rm -f', 'clean.sh')
                filter_file(r'module load lang/tcsds-1.2.24', '', 'make.FP3.sh')
                files = (os.path.join('make','OPTION'), os.path.join('lib','src','ParMetis-3.1','Makefile.in'), \
                         os.path.join('lib','src','REVOCAP_Refiner-1.1.02','OPTIONS'), \
                         os.path.join('lib','src','REVOCAP_Refiner-1.1.02','MakefileConfig.in') )
                for f in files:
                    filter_file(r'fccpx', 'fcc', f)
                    filter_file(r'FCCpx', 'FCC', f)
                    filter_file(r'frtpx', 'frt', f)
                    #filter_file(r'visimpact,', '', f)
                    #filter_file(r'-Kvisimpact', '', f)
                    #filter_file(r'-Nlinkprof', '', f)
                    #filter_file(r'-Qt', '', f)
                    filter_file(r'COPT =', 'COPT = -Nnoclang', f)
                    filter_file(r'OPTFLAGS =', 'OPTFLAGS = -Nnoclang', f)
                    filter_file(r'CFLAGS =', 'CFLAGS = -Nnoclang', f)
                    filter_file(r'CXXFLAGS =', 'CXXFLAGS = -Nnoclang', f)
                clean_exe = Executable('./clean.sh')
                clean_exe()
                make_exe = Executable('./make.FP3.sh')
                make_exe()
        else:
            pass


    def build_libs(self, spec, prefix):
        #
        # Create libdd_mpi_lbm.a and libgf2_lbm.a
        #
        workdir = os.getcwd()
        #
        if spec.satisfies('@03.01'):
            print("Creating libraries")
            for lib in ['fort', 'dd_dmy_lbm', 'dd_mpi', 'dd_mpi_lbm', 'gf2', 'gf2_lbm']:
                with working_dir('lib/src/'+lib, create=False):
                    #clean_sh = Executable("make -f ../../../make/makefile clean")
                    ##clean_sh = Executable("make -f "+workdir+"/make/makefile clean")
                    ##clean_sh()
                    Executable("make -f "+workdir+"/make/makefile clean")
            with working_dir('lib/src/ParMetis-3.1/METISLib', create=False):
                ##clean_sh = Executable("make -f Makefile realclean")
                ##clean_sh()
                Executable("make -f Makefile realclean")
            with working_dir('lib/src', create=False):
                install_sh = Executable("./Makeall.ffx")
                install_sh()
        elif spec.satisfies('@59.01'):
            with working_dir('lib/src/dd_mpi_lbm/', create=False):
                Executable('make clean')
                Executable('make lib')
            with working_dir('lib/src/gf2_lbm/', create=False):
                Executable('make clean')
                Executable('make lib')
        else:
            pass

    def build_misc(self, spec, prefix):
        workdir = os.getcwd()
        if spec.satisfies('@03.01'):
            with working_dir('util/lbm', create=False):
                ##clean_sh = Executable('make -f '+workdir+'/make/makefile clean')
                ##clean_sh()
                Executable('make -f '+workdir+'/make/makefile clean')
            for lib in ('partrg', 'mltcub', 'mltcub4', 'mltcub5'):
                with working_dir('util/lbm/'+lib, create=False):
                    ##claen_sh = Executable('make -f '+workdir+'/make/makefile clean')
                    ##clean_sh()
                    Executable('make -f '+workdir+'/make/makefile clean')
            with working_dir('util/lbm', create=False):
                install_sh = Executable('./Makeall')
                install_sh()
        else:
            pass
        

    def build_lbm3d(self, spec, prefix):
        if spec.satisfies('@03.01'):
            print("Creating lbm3d")
            with working_dir('util/lbm3d', create=False):
                ##clean_sh = Executable('make clean')
                ##clean_sh()
                Executable('make clean')
                install_sh = Executable('make')
                install_sh()
        else:
            pass

        
    def build_lbm3dmpi(self, spec, prefix):
        #
        # Create lbm3d.mpi
        #
        print("Creating lbm3d.mpi")
        if spec.satisfies('@59.01'):
            with working_dir('SRC/lbm/ver.59.01', create=False):
                ##clean_sh = Executable('make clean')
                install_sh = Executable('make')
                ##clean_sh()
                Executable('make clean')
                install_sh()
                mkdirp(prefix.bin)
                install('lbm3d.mpi', prefix.bin)
        elif spec.satisfies('@03.01'):
            with working_dir('util/lbm3d.mpi', create=False):
                ##clean_sh = Executable('make clean')
                install_sh = Executable('make')
                ##clean_sh()
                Executable('make clean')
                install_sh()
        else:
            pass


    def install_ffx(self, spec, prefix):
        if spec.satisfies('@03.01'):
            mkdirp(prefix.bin)
            install(join_path(self.stage.source_path, "bin", "*"), prefix.bin)
            
            
