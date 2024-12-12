from spack import *


class Pmlib(Package):
    """PMlib is open source software library to measure the run time performance of the
       user application and to report the performance statistics of the processes.
       PMlib supports serial and parallel (MPI & OpeMP) models of C/C++/Fortran applications.
       PMlib can be used in various forms. The simplest usage is to spack load pmlib and link
       into the application by its own. However, in most realistic cases, it is used with
       the hardware performance counters, or maybe with Power API features.
       For typical use, see examples in ${PMLIB}/doc/scripts/.
       PMlib categorizes the performance stats obtained from hardware counters as controlled
       via environment variables.
       See Readme.md in the development repository https://github.com/mikami3heart/PMlib .
    """

    homepage = "https://github.com/mikami3heart/PMlib"
    has_code = False

    version('9.2-clang')
    version('9.2-trad')
    version('10.0-clang')
    version('10.0-trad')
    version('10.0-pybind')

    def install(self, spec, prefix):
        ## PMlib source programs and native installation scripts are availale from the homepage
        pass

    def setup_run_environment(self, env):
        env.set("PMLIB_DIR", self.prefix)
        env.prepend_path("C_INCLUDE_PATH", self.prefix.include)
        env.prepend_path("CPLUS_INCLUDE_PATH", self.prefix.include)
        env.prepend_path("LD_LIBRARY_PATH", self.prefix.lib)
        #   if version == Version("10.0-pybind"):
        env.prepend_path("PYTHONPATH", self.prefix.lib)


