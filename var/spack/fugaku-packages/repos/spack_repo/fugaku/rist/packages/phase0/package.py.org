from spack import *


class Phase0(Package):
    homepage = "https://azuma.nims.go.jp/cms1"
    has_code = False

    version('2021.01')

    def install(self, spec, prefix):
        ##PHASE0 is available as an external package; it is not installable in user space.
        pass
