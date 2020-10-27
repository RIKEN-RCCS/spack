# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Genesis(AutotoolsPackage):
    """GENESIS is a Molecular dynamics and modeling software
    for bimolecular systems such as proteins, lipids, glycans,
    and their complexes.
    """

    homepage = "https://www.r-ccs.riken.jp/labs/cbrt/"
#    url = "https://www.r-ccs.riken.jp/labs/cbrt/wp-content/uploads/2020/09/genesis-1.5.1.tar.bz2"

    version('2.0b',
            git='https://github.com/genesis-release-r-ccs/genesis-2.0.git')
    version('1.5.1','28d696e681efd76cc8a875dc0b305794',
            url='https://www.r-ccs.riken.jp/labs/cbrt/wp-content/uploads/2020/09/genesis-1.5.1.tar.bz2')
    version('1.5.0','385e35430da2b42a6a9f1961a6345be3',
            url='https://www.r-ccs.riken.jp/labs/cbrt/wp-content/uploads/2020/05/genesis-1.5.0.tar.bz2')
    version('1.4.0', '132d53e7edbd593d67ec53cd4618748a',
            url='https://www.r-ccs.riken.jp/labs/cbrt/wp-content/uploads/2019/10/genesis-1.4.0.tar.bz2')
    version('1.3.0','19dc4249af1472d75a110d157364b610',
            url='https://www.r-ccs.riken.jp/labs/cbrt/wp-content/uploads/2018/06/genesis-1.3.0.tar.bz2')
    version('1.2.1','b40b05e327679fac6d1c20208577ea40',
            url='https://www.r-ccs.riken.jp/labs/cbrt/wp-content/uploads/2018/02/genesis-1.2.1.tar.bz2')
    version('1.2.0','47670beca36398eaae8b3fc72e0a9dcd',
            url='https://www.r-ccs.riken.jp/labs/cbrt/wp-content/uploads/2018/01/genesis-1.2.0.tar.bz2')
    version('1.1.6','2726adf527ab66ffdc2903c0f18c466f',
             url='https://www.r-ccs.riken.jp/labs/cbrt/wp-content/uploads/2017/10/genesis-1.1.6.tar.bz2')
    version('1.1.5','827737354f1c0a265b7d9af7bb9bca75',
             url='https://www.r-ccs.riken.jp/labs/cbrt/wp-content/uploads/2017/07/genesis-1.1.5.tar.bz2')

    resource(when='@1.4.0:1.5.1',
             name='user_guide',
             url='https://www.r-ccs.riken.jp/labs/cbrt/wp-content/uploads/2019/10/GENESIS-1.4.0.pdf',
             sha256='da2c3f8bfa1e93adb992d3cfce09fb45d8d447a94f9a4f884ac834ea7279b9c7',
             expand=False,
             placement='doc')

    variant('openmp', default=True, description='Enable OpenMP.')
    variant('gpu', default=False, description='Enable GPU.')
    variant('single', default=False, description='Enable single precision.')
    variant('hmdisk', default=False, description='Enable huge molecule on hard disk.')

    conflicts('%clang', when='+openmp')
    conflicts('~openmp', when='@:1.4.0')
    conflicts('+fugaku', when='@1.5.0:', msg='Fugaku option is not available.')

    depends_on('mpi', type=('build', 'run'))
    depends_on('cuda', when='+gpu')
    depends_on('lapack')

    parallel = False

    def configure_args(self):
        spec = self.spec
        options = []
        if '~openmp' in spec:
            options.append('--disable-openmp')
        if '+single' in spec:
            options.append('--enable-single')
        if '+hmdisk' in spec:
            options.append('--enable-hmdisk')
        if '+gpu' in spec:
            options.append('--enable-gpu')
            options.append('--with-cuda=%s' % spec['cuda'].prefix)
        if '+debug' in spec:
            options.append('--enable-debug=3')
        if '+fugaku' in spec:
            options.append('--host=Fugaku')
        return options

    def configure(self, spec, prefix):
        # need to unset environment variables of compiler
        env['F77'] = ''
        env['FC'] = ''
        env['CXX'] = ''
        env['CC'] = ''
        if '^openblas' in spec:
            env['LAPACK_LIBS'] = "`pkg-config --libs openblas`"
        configure('--prefix={0}'.format(prefix), *self.configure_args())

    def install(self, spec, prefix):
        make('install')
        install_tree('doc', prefix.share.doc)
