from spack.package import *

class OpenfoldForFugaku(Package):
    """OpenFold-for-Fugaku is an open-source implementation of the protein structure
       inference software OpenFold adapted for the Japanese supercomputer Fugaku.
       It targets large-scale, high-throughput inference workloads in a massively
       parallel CPU environment, enabling rapid prediction of 3D protein structures
       from amino-acid sequences for applications such as genome medicine and drug
       discovery research."""

    homepage = "https://github.com/RIKEN-RCCS/OpenFold-for-Fugaku"
    has_code = False

    version('1.0')

    depends_on('c', type='build') #dummy
    
    def install(self, spec, prefix):
        ##OpenFold-for-Fugaku is available as an external package; it is not installable in user space.
        pass
