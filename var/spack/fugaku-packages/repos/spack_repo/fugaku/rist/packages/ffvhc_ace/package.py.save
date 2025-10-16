from spack import *


class FfvhcAce(Package):
    """FFVHC-ACE (FrontFlow/Violet Hierarchical Cartesian for Aeronautics based on Compressible-flow Equations)"""

    homepage = ""
    has_code = False

    version('0.1')

    def setup_run_environment(self, env):
        env.prepend_path('PATH', self.prefix)

    def install(self, spec, prefix):
        ##FFVHC-ACE is available as an external package; it is not installable in user space.
        pass
