from spack_repo.builtin.build_systems.python import PythonPackage
from spack.package import *

class PyPhonopy(PythonPackage):
    """Phonopy is an open source package for phonon
    calculations at harmonic and quasi-harmonic levels."""

    homepage = "https://atztogo.github.io/phonopy/index.html"
    url      = "https://github.com/phonopy/phonopy/archive/refs/tags/v2.27.0.tar.gz"
    git      = "https://github.com/phonopy/phonopy.git"

    version("2.27.0", commit="7fac9a33e6208a801ca1af2fe21ef1db21f714d5")
    version("2.20.0", sha256="1dd47cb6e5b427d5cb88ce0b810b91f05533f434d53d22ea69eb974d4eb0ab46")
    version("2.12.0", sha256="a48d1f750e72da3c43c9a205572966b250f890311be2310c27f527056ba84648")
    version("1.10.0", sha256="6b7c540bbbb033203c45b8472696db02a3a55913a0e5eb23de4dc9a3bee473f7")

    # Python build system
    build_system_class = "python"

    # Core dependencies
    depends_on("python@3.8:", type=("build", "run"), when="@2.20.0:")
    depends_on("py-setuptools", type="build")
    depends_on("py-pip", type="build", when="@2.26.0:")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))

    # Version-specific dependencies
    depends_on("py-numpy@1.11:", type=("build", "run"), when="@2.12.0")
    depends_on("py-matplotlib@2.0:", type=("build", "run"), when="@2.12.0")
    depends_on("py-h5py", type=("build", "run"), when="@2.12.0:")
    depends_on("py-spglib", type="run", when="@2.12.0:")
    depends_on("py-scipy@1.5.4:", type=("build", "run"), when="@2.12.0:")

    depends_on("py-numpy@1.15:", type=("build", "run"), when="@2.20.0")
    depends_on("py-matplotlib@2.2.2:", type=("build", "run"), when="@2.20.0")

    depends_on("py-spglib", type=("build", "run"), when="@2.26.0:")
    depends_on("py-seekpath", type=("build", "run"), when="@2.26.0:")
    depends_on("py-numpy@1.17:", type="build", when="@2.26.0:")

    # Optional: custom install method for pip-based install
    def install(self, spec, prefix):
        if spec.satisfies("@2.26.0:"):
            pip = which("pip")
            pip("install", ".", "--prefix={0}".format(prefix), "--no-deps")
