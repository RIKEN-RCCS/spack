# To create SIF file for singularity.
# It is created with "virtual_fugaku" environment activated.
# (Below is an example executing on AWS for creating SIF file)
# 
singularity build --fakeroot --bind /opt/amazon vf-ver1.1.sif spack-ver1-1.def
