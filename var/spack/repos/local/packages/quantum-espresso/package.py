from spack import *

class QuantumEspresso(Package):
    """Quantum ESPRESSO is an integrated suite of Open-Source computer codes
    for electronic-structure calculations and materials modeling at the
    nanoscale. It is based on density-functional theory, plane waves, and
    pseudopotentials.
    """

    homepage = "https://www.quantum-espresso.org"
    has_code = False

    version('6.5')
    version('6.6')
    version('6.7')
    version('6.8')
    version('7.0')
    version('7.1')
    version('7.2')
    version('7.3')
    version('7.3.1')

    def setup_run_environment(self, env):
        env.prepend_path('PATH', self.prefix)

    def install(self, spec, prefix):
        pass
