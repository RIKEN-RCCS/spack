# The steps to create "virtual_fugaku" environment are as follows:
# 
# First
# Build the GCC environment
spack install gcc@14.1.0+binutils
spack load gcc
spack compiler find

# Second,
# Create environment for python.
cd spack
spack env create virtual_fugaku_python etc/spack/spack_python.yaml
spack -e virtual_fugaku_python concretize
spack -e virtual_fugaku_python install

# Third,
# Create environment for application including "virtual_fugaku_python".
spack env create --include-concrete virtual_fugaku_python virtual_fugaku etc/spack/spack.yaml
spack -e virtual_fugaku concretize
spack -e virtual_fugaku install

# You can use the spack in one of the following ways.
# "spack env activate virtual_fugaku"
#   or
# "spack load [spec]"
