from spack.package import *

class Abinitmp(Package):
    """ABINIT-MP is a user-friendly FMO program (by which 4-body fragments can be computed),
       especially for in-house Linux/Intel servers under the standard MPI environment.
       Additionally, the associated graphical user-interface system, BioStation Viewer (on
       Windows) helps the preparation of input data including the tedious fragmentation
       setting and also assists intuitive understanding of the target system through the
       inter-fragment interaction energies (IFIEs)."""

    homepage = "http://www.cenav.org/abinit-mp-open_ver-1-rev-22/"
    has_code = False

    version('1-22')
    version('2-4')
    version('2-8')
    version('dd1-2024')

    depends_on('c', type='build') #dummy
    
    def install(self, spec, prefix):
        ##ABINIT-MP is available as an external package; it is not installable in user space.
        pass
