# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class Ffb(MakefilePackage):
    """Computational Fluid Dynamics Software for aeroacoustics"""

    homepage = "http://www.ciss.iis.u-tokyo.ac.jp/dl/index.php"
    url      = "file://{0}/FrontFlow_blue.8.1.tar.gz".format(os.getcwd())
    manual_download = True

    version('9.0', sha256='f72862170c2ccd08d52448fbb15f96463f11c271779e96909b14e00d52d9833b',
                   url="file://{0}/FFB.ver.9.0_202210.r1.tar.gz".format(os.getcwd()))
    version('8.1', sha256='1ad008c909152b6c27668bafbad820da3e6ec3309c7e858ddb785f0a3d6e43ae')

    patch('revocap_refiner.patch', when='@8.1')
    patch('revocap_refiner-size_t.patch', when='@8.1')
    patch('fortran-format.patch', when='@8.1')
    patch('xvx.patch', when='@8.1')
    patch('gffv3tr.patch', when='@8.1')
    patch('revocap_refiner-1.1.02.patch', when='@9.0')

    depends_on('mpi')
    depends_on('blas')
    depends_on('scalapack')

    parallel = False

    def flag_handler(self, name, flags):
        opt_flag_found = any(f in self.compiler.opt_flags for f in flags)
        if name == 'cflags':
            if not opt_flag_found:
                flags.append('-Kvisimpact')
        elif name == 'cxxflags':
            if not opt_flag_found:
                flags.append('-Kvisimpact')
            flags.append(self.compiler.cxx_pic_flag)
        if name == 'fflags':
            if not opt_flag_found:
                flags.append('-Kvisimpact')
        if name in ('cflags', 'cxxflags', 'fflags'):
            return (None, flags, None)
        else:
            return (flags, None, flags)

    def edit(self, spec, prefix):
        workdir = os.getcwd()
        cflags = env['CFLAGS']
        cxxflags = env['CXXFLAGS']
        fflags = env['FFLAGS']

        if spec.satisfies('@8.1'):
            make = join_path('make', 'makefile')
            m = FileFilter(make)
            m.filter(
                r'#LES3DHOME   =', 'LES3DHOME= {0}\n'.format(workdir))

        if spec.satisfies('@8.1'):
            make = join_path('make', 'OPTION')
            m = FileFilter(make)
            m.filter(r'CPP\s*=.*$', 'CPP = /usr/bin/cpp')
            m.filter(r'CCOM\s*=.*$', 'CCOM = {0}'.format(spack_cc))
            m.filter(r'COPT\s*=.*$', 'COPT = {0}'.format(cflags))
            m.filter(r'FCOM\s*=.*$', 'FCOM = {0}\n'.format(spack_fc))
            m.filter(r'FOPT\s*=.*$', 'FOPT = {0}\n'.format(fflags))
            m.filter(r'INCDIR\s*=.*$', 'INCDIR = {0}\n'
                     .format(spec['mpi'].headers.directories[0]))
            m.filter(r'LIBDIR\s*=.*$', 'LIBDIR = {0}\n'
                     .format(spec['mpi'].libs.directories[0]))
        elif spec.satisfies('@9.0'):
            make = join_path('FFB', 'make', 'OPTION')
            m = FileFilter(make)
            m.filter(r'CCOM\s*=.*$', 'CCOM = {0}'.format(spec['mpi'].mpicc))
            m.filter(r'COPT\s*=.*$', 'COPT = -Nnoclang -Kocl,openmp,parallel $(OPT) -Nlst=t {0}'.format(cflags) )
            m.filter(r'FCOM\s*=.*$', 'FCOM = {0}\n'.format(spec['mpi'].mpifc))
            m.filter(r'FOPT\s*=.*$', 'FOPT = -Nnoclang -Kocl,visimpact,optmsg=2,openmp $(OPT) -Nlst=t -Cpp -Cfpp {0}\n'.format(fflags))
            m.filter(r'LINK\s*=.*$', 'LINK = {0}'.format(spec['mpi'].mpicxx))
            m.filter(r'LOPT\s*=.*$', 'LOPT = -Nnoclang --linkfortran -Kopenmp,parallel $(OPT) {0}'.format(cxxflags))

        if spec.satisfies('@8.1'):
            srcdir = join_path('lib', 'src')
            utildir = join_path(workdir, 'util')
            with open(join_path('make', 'Makeall'), 'w') as m:
                m.write('#!/bin/csh -f\n')
                m.write('setenv LES3DHOME {0}\n'.format(workdir))
                m.write('cd {0}\n'.format(srcdir))
                m.write('./Makeall\n')
                m.write('cd {0}\n'.format(utildir))
                m.write('./Makeall\n')
        elif spec.satisfies('@9.0'):
            makefp3 = join_path('FFB', '.', 'make.FP3.sh')
            m = FileFilter(makefp3)
            m.filter(r'module load lang/tcsds-1.2.24', '')
            m.filter('util/les3x.mpi', '../SRC/solver/ver.67.01')

        if spec.satisfies('@8.1'):
            makeall = join_path('lib', 'src', 'dd_mpi', 'Makeall')
            dd_mpi_dir = join_path('lib', 'src', 'dd_mpi')
            with open(makeall, 'w') as m:
                m.write('#!/bin/csh -f\n')
                m.write('setenv LES3DHOME {0}\n'.format(workdir))
                m.write('cd {0}\n'.format(dd_mpi_dir))
                m.write('make lib FCOM={0}\n'.format(spec['mpi'].mpifc))
            os.chmod(makeall, 0o755)

            makeall = join_path('.',  'Makeall.les')
            les3d_dir = join_path('util', 'les3d.mpi')
            les3c_dir = join_path('util', 'les3c.mpi')
            les3ct_dir = join_path('util', 'les3ct.mpi')
            les3x_dir = join_path('util', 'les3x.mpi')
            with open(makeall, 'w') as m:
                m.write('#!/bin/csh -f\n')
                m.write('setenv LES3DHOME {0}\n'.format(workdir))
                m.write('cd {0}\n'.format(join_path(workdir, les3d_dir)))
                m.write('make CCOM={0}'.format(spec['mpi'].mpicc))
                m.write(' FCOM={0}\n'.format(spec['mpi'].mpifc))
                m.write('cd {0}\n'.format(join_path(workdir, les3c_dir)))
                m.write('make CCOM={0}'.format(spec['mpi'].mpicc))
                m.write(' FCOM={0}\n'.format(spec['mpi'].mpifc))
                m.write('cd {0}\n'.format(join_path(workdir, les3ct_dir)))
                m.write('make CCOM={0}'.format(spec['mpi'].mpicc))
                m.write(' FCOM={0}\n'.format(spec['mpi'].mpifc))
                m.write('cd {0}\n'.format(join_path(workdir, les3x_dir)))
                m.write('make CCOM={0}'.format(spec['mpi'].mpicc))
                m.write(' FCOM={0}\n'.format(spec['mpi'].mpifc))

                for d in [les3c_dir, les3ct_dir, les3d_dir]:
                    editfile = join_path(d, 'FILES')
                    m = FileFilter(editfile)
                    m.filter(r'-lmpi_f77', '')
            os.chmod(makeall, 0o755)

            editfile = join_path('lib', 'src', 'Makeall')
            m = FileFilter(editfile)
            m.filter(r'x86_64-linux', '{0}-linux'.format(spec.target.family))

            editfile = join_path('lib', 'src', 'REVOCAP_Refiner-0.4.3', 'OPTIONS')
            m = FileFilter(editfile)
            m.filter(r'ARCH\s*=.*$', 'ARCH= $(shell arch)-linux')
            m.filter(r'CC\s*=.*$', 'CC={0}'.format(spack_cc))
            m.filter(r'CFLAGS\s*=.*$', 'CFLAGS={0}'.format(cflags))
            m.filter(r'CXX\s*=.*$',  'CXX={0}'.format(spack_cxx))
            m.filter(r'CXXFLAGS\s*=.*$',
                     'CXXFLAGS={0}'.format(cxxflags))
            m.filter(r'F90\s*=.*$', 'CC={0}'.format(spack_fc))
            m.filter(r'LD\s*=.*$', 'LD={0}'.format(spack_fc))
            m.filter(r'LIBPATH\s*=.*$', 'LIBPATH= ')
            m.filter(r'FFLAGS\s*=.*$', 'FFLAGS={0}'.format(fflags))
            m.filter(r'LDFLAGS\s*=.*$', 'LDFLAGS={0}'.format(fflags))

        elif spec.satisfies('@9.0'):
            editfile = join_path('FFB', 'lib', 'src', 'REVOCAP_Refiner-1.1.02', 'OPTIONS')
            m = FileFilter(editfile)
            m.filter(r'CC\s*=.*$',       'CC={0}'.format(spec['mpi'].mpicc))
            m.filter(r'CFLAGS\s*=.*$',   'CFLAGS= -Nnoclang $(DEBUGFLAG) {0}'.format(cflags))
            m.filter(r'CXX\s*=.*$',      'CXX={0}'.format(spec['mpi'].mpicxx))
            m.filter(r'CXXFLAGS\s*=.*$', 'CXXFLAGS= -Nnoclang $(DEBUGFLAG) {0}'.format(cxxflags))
            m.filter(r'F90\s*=.*$',      'F90={0}'.format(spec['mpi'].mpifc))
            m.filter(r'FFLAGS\s*=.*$',   'FFLAGS= $(DEBUGFLAG) {0}'.format(fflags))
            m.filter(r'LDFLAGS\s*=.*$',  'LDFLAGS= -Nnoclang --linkfortran $(FFLAGS)')

            editfile = join_path('FFB', 'lib', 'src', 'REVOCAP_Refiner-1.1.02', 'MakefileConfig.in')
            m = FileFilter(editfile)
            m.filter(r'CC \s*=.*$',      'CC ={0}'.format(spec['mpi'].mpicc))
            m.filter(r'CFLAGS\s*=.*$',   'CFLAGS= -Nnoclang $(DEBUGFLAG) {0}'.format(cflags))
            m.filter(r'CXX \s*=.*$',     'CXX ={0}'.format(spec['mpi'].mpicxx))
            m.filter(r'CXXFLAGS\s*=.*$', 'CXXFLAGS= -Nnoclang $(DEBUGFLAG) {0}'.format(cxxflags))
            m.filter(r'F90\s*=.*$',      'F90={0}'.format(spec['mpi'].mpifc))
            m.filter(r'FFLAGS\s*=.*$',   'FFLAGS= $(DEBUGFLAG) {0}'.format(fflags))

        if spec.satisfies('@8.1'):
            editfile = join_path('lib', 'src', 'ParMetis-3.1', 'Makefile.in')
            m = FileFilter(editfile)
            m.filter(r'CC \s*=.*$', 'CC ={0}'.format(spack_cc))
            m.filter(r'INCDIR\s*=.*$', 'INCDIR = \n')
        elif spec.satisfies('@9.0'):
            editfile = join_path('FFB', 'lib', 'src', 'ParMetis-3.1', 'Makefile.in')
            m = FileFilter(editfile)
            m.filter(r'CC \s*=.*$', 'CC ={0}'.format(spec['mpi'].mpicc))
            m.filter(r'OPTFLAGS \s*=.*$', 'OPTFLAGS = -Nnoclang -Kvisimpact \n')

        if spec.satisfies('@8.1'):
            editfile = join_path('util', 'xvx2gf', 'Makefile')
            m = FileFilter(editfile)
            m.filter(
                r'#LES3DHOME   =', 'LES3DHOME= {0}\n'.format(workdir))
            m.filter(r'g\+\+', (spack_cxx))

            editfile = join_path('util', 'les3x.mpi', 'FILES')
            m = FileFilter(editfile)
            m.filter(r'LIBS = -lfort -lgf2 -ldd_mpi -lmpi_f77',
                     'LIBS = -lfort -lgf2  -ldd_mpi')

            editfile = join_path('util', 'xvx2gf', 'FILES')
            cxx_fortran_flags = []
            if spec.satisfies('%gcc'):
                cxx_fortran_flags.append('-lgfortran')
                m = FileFilter(editfile)
                m.filter('-lifcore -limf', ' '.join(cxx_fortran_flags))
            elif spec.satisfies('%fj'):
                cxx_fortran_flags.append('--linkfortran')
                m = FileFilter(editfile)
                m.filter('-lifcore -limf', ' '.join(cxx_fortran_flags))
            elif spec.satisfies('%intel'):
                pass

        elif spec.satisfies('@9.0'):
            with open(join_path('FFB', 'clean.sh'), 'a') as m:
                m.write('find ../SRC/solver/ver.67.01 -name "*.o"   -exec rm {} \;\n')
                m.write('find ../SRC/solver/ver.67.01 -name "*.lst" -exec rm {} \;\n')

    def build(self, spec, prefix):
        if spec.satisfies('@8.1'):
            for m in [join_path('make',  'Makeall'),
                      join_path('lib', 'src', 'dd_mpi', 'Makeall'),
                      join_path('.', 'Makeall.les')]:
                Executable(m)()
        elif spec.satisfies('@9.0'):
            cd('FFB')
            bash = which('bash')
            bash('./clean.sh')
            bash('./make.FP3.sh')

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)
        install_tree('macro', prefix.macro)

    def setup_run_environment(self, env):
        env.prepend_path('PATH', prefix.macro)
