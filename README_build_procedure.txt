# Creating a "virtual_fugaku" environment requires the following three steps:
# 
# First
# Build an environment for using the gcc@14 compiler.
spack install gcc@14.1.0+binutils
spack load gcc
spack compiler find

# Second,
# Create a virtual environment with various applications installed.
cd spack
spack env create virtual_fugaku_app etc/spack/spack.yaml
spack -e virtual_fugaku_app concretize
spack -e virtual_fugaku_app install

# Third,
# Add the netlib library to the virtual environment created at Second step.
spack env create --include-concrete virtual_fugaku_app virtual_fugaku etc/spack/spack_lib.yaml
spack -e virtual_fugaku concretize
spack -e virtual_fugaku install

# The created virtual environment "A" can be used in the following ways.
# "spack env activate virtual_fugaku"
#   or
# Each application can also be used normally without using a virtual environment, as follows:
# "spack load [spec]"
