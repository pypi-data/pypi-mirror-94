"""Install VASP and dependencies."""
import os

from phytoolkit.base.installer import BaseInstaller
from phytoolkit.exception.installationexception import InstallationException

VASP_MAKE_CONFIG = """
# Precompiler options
CPP_OPTIONS= -DHOST=\\"LinuxGNU\\" \
             -DMPI -DMPI_BLOCK=8000 \
             -Duse_collective \
             -DscaLAPACK \
             -DCACHE_SIZE=4000 \
             -Davoidalloc \
             -Duse_bse_te \
             -Dtbdyn \
             -Duse_shmem

CPP        = gcc -E -P -C -w $*$(FUFFIX) >$*$(SUFFIX) $(CPP_OPTIONS)

FC         = mpif90
FCL        = mpif90

FREE       = -ffree-form -ffree-line-length-none

FFLAGS     = -w
OFLAG      = -O2
OFLAG_IN   = $(OFLAG)
DEBUG      = -O0

LIBDIR     = %s
LIBDIR2    = %s
LIBDIR3    = %s
BLAS       = -L$(LIBDIR) -lblas
LAPACK     = -L$(LIBDIR2) -ltmglib -llapack
BLACS      =
SCALAPACK  = -L$(LIBDIR3) -lscalapack $(BLACS)

LLIBS      = $(SCALAPACK) $(LAPACK) $(BLAS)

FFTW       ?= /usr/local
LLIBS      += -L$(FFTW)/lib -lfftw3
INCS       = -I$(FFTW)/include

OBJECTS    = fftmpiw.o fftmpi_map.o  fftw3d.o  fft3dlib.o

OBJECTS_O1 += fftw3d.o fftmpi.o fftmpiw.o
OBJECTS_O2 += fft3dlib.o

# For what used to be vasp.5.lib
CPP_LIB    = $(CPP)
FC_LIB     = $(FC)
CC_LIB     = gcc
CFLAGS_LIB = -O
FFLAGS_LIB = -O1
FREE_LIB   = $(FREE)

OBJECTS_LIB= linpack_double.o getshmem.o

# For the parser library
CXX_PARS   = g++

LIBS       += parser
LLIBS      += -Lparser -lparser -lstdc++

# Normally no need to change this
SRCDIR     = ../../src
BINDIR     = ../../bin

#================================================
# GPU Stuff

CPP_GPU    = -DCUDA_GPU -DRPROMU_CPROJ_OVERLAP -DCUFFT_MIN=28 -UscaLAPACK # -DUSE_PINNED_MEMORY

OBJECTS_GPU= fftmpiw.o fftmpi_map.o fft3dlib.o fftw3d_gpu.o fftmpiw_gpu.o

CC         = gcc
CXX        = g++
CFLAGS     = -fPIC -DADD_ -openmp -DMAGMA_WITH_MKL -DMAGMA_SETAFFINITY -DGPUSHMEM=300 -DHAVE_CUBLAS

CUDA_ROOT  ?= /usr/local/cuda
NVCC       := $(CUDA_ROOT)/bin/nvcc
CUDA_LIB   := -L$(CUDA_ROOT)/lib64 -lnvToolsExt -lcudart -lcuda -lcufft -lcublas

GENCODE_ARCH    := -gencode=arch=compute_30,code=\\"sm_30,compute_30\\" \
                   -gencode=arch=compute_35,code=\\"sm_35,compute_35\\" \
                   -gencode=arch=compute_60,code=\\"sm_60,compute_60\\"

MPI_INC    = /opt/gfortran/openmpi-1.10.2/install/ompi-1.10.2-GFORTRAN-5.4.1/include
"""


class VaspInstaller(BaseInstaller):
    """Installs VASP."""

    def __init__(self, config):
        super().__init__(config)
        self.console = config.console
        self.required_os_packages = ["mpich", "libblas3", "libblas-dev", "liblapack3",
                                     "liblapack-dev", "build-essential", "gfortran", "rsync",
                                     "curl"]

    def pre_installation(self):
        """Download and extract prerequisites."""
        # download required third-party libraries
        self.net_helper.download_file("http://fftw.org/fftw-3.3.8.tar.gz", "fftw.tar.gz")
        self.net_helper.download_file("http://www.netlib.org/blas/blas.tgz", "blas.tgz")
        self.net_helper.download_file("http://www.netlib.org/lapack/lapack-3.4.0.tgz", "lapack.tgz")
        self.net_helper.download_file("http://www.netlib.org/scalapack/scalapack-2.0.2.tgz",
                                      "scalapack.tgz")

        # extract the third-party libraries and VASP
        for file in ["fftw.tar.gz", "blas.tgz", "lapack.tgz", "scalapack.tgz"]:
            if not self.os_helper.extract_tar_file(file):
                raise InstallationException("Unable to extract tar file %s" % file)
        source_dir = os.path.join(self.config.vasp_source, "vasp.5.4.4.tar.gz")
        if not self.os_helper.run_shell_command(["cp", source_dir, self.config.dest_dir]):
            raise InstallationException(
                "Unable to copy VASP source from %s." % self.config.vasp_source)
        if not self.os_helper.extract_tar_file("vasp.5.4.4.tar.gz", self.config.dest_dir):
            raise InstallationException(
                "Unable to extract vasp.5.4.4.tar.gz file from location %s" %
                self.config.dest_dir)
        self.console.info("Downloaded and extracted package archives.")

    def installation(self):
        """Install prerequisites and VASP"""
        # build FFTW
        fftw_dir = os.path.join(self.config.dest_dir, "fftw-3.3.8")
        if not self.os_helper.run_shell_command(["./configure", ], fftw_dir):
            raise InstallationException("FFTW build configuration failed.")
        self.console.verbose_success("FFTW configuration successful.")
        if not self.os_helper.run_shell_command(["make", ], fftw_dir):
            raise InstallationException("FFTW make failed.")
        self.console.verbose_success("FFTW make successful.")
        if not self.os_helper.run_shell_command(["sudo", "make", "install"], fftw_dir):
            raise InstallationException("FFTW installation failed.")
        self.console.verbose_success("FFTW installation successful.")

        # build BLAS
        blas_dir = os.path.join(self.config.dest_dir, "BLAS-3.8.0")
        if not self.os_helper.run_shell_command(["make", ], blas_dir):
            raise InstallationException("BLAS make failed.")
        self.console.verbose_success("BLAS make successful.")
        if not self.os_helper.run_shell_command(["cp", "blas_LINUX.a", "libblas.a"], blas_dir):
            raise InstallationException("Copying BLAS to target failed.")
        self.console.verbose_success("Copied blas_LINUX.a to libblas.a.")

        # build Lapack
        lapack_dir = os.path.join(self.config.dest_dir, "lapack-3.4.0")
        if not self.os_helper.run_shell_command(["cp", "make.inc.example", "make.inc"], lapack_dir):
            raise InstallationException("Coping configuration file for Lapack failed.")
        self.console.verbose_info("Copied make.inc to installation directory.")
        if not self.os_helper.run_shell_command(["make", "lapack_install", "lib"], lapack_dir):
            raise InstallationException("Lapack make failed.")
        self.console.verbose_success("Lapack make successful.")

        # build ScaLapack
        scalapack_dir = os.path.join(self.config.dest_dir, "scalapack-2.0.2")
        if not self.os_helper.run_shell_command(["cp", "SLmake.inc.example", "SLmake.inc"],
                                                scalapack_dir):
            raise InstallationException("Coping configuration file for ScaLapack failed.")
        self.console.verbose_info("Copied SLmake.inc to installation directory.")
        if not self.os_helper.run_shell_command(["make", "lib", "exe"], scalapack_dir):
            raise InstallationException("ScaLapack make failed.")
        self.console.verbose_success("ScaLapack make successful.")

        # build VASP
        vasp_dir = os.path.join(self.config.dest_dir, "vasp.5.4.4")
        makefile_path = os.path.join(vasp_dir, "makefile.include")
        self.os_helper.write_file(makefile_path,
                                  VASP_MAKE_CONFIG % (blas_dir, lapack_dir, scalapack_dir))
        if not self.os_helper.run_shell_command(["make", ], vasp_dir):
            raise InstallationException("VASP make failed.")
        self.console.success("VASP make successful.")

    def post_installation(self):
        """Updates .bashrc and cleans up archives."""
        vasp_dir = os.path.join(self.config.dest_dir, "vasp.5.4.4", "bin")
        bash_rc = os.path.join(os.path.expanduser("~"), ".bashrc")
        self.os_helper.append_file(bash_rc, "export PATH=$PATH:%s" % vasp_dir)
        self.console.info("VASP binaries 'vasp_std', 'vasp_gam' and 'vasp_ncl' installed.")
        self.console.info("Run 'source ~/.bashrc' or open a new terminal to start using VASP.")
        self.console.success("Installation of VASP completed.")
