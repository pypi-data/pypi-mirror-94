# Copyright (c) 2010-2020, Lawrence Livermore National Security, LLC. Produced
# at the Lawrence Livermore National Laboratory. All Rights reserved. See files
# LICENSE and NOTICE for details. LLNL-CODE-806117.
#
# This file is part of the MFEM library. For more information and source code
# availability visit https://mfem.org.
#
# MFEM is free software; you can redistribute it and/or modify it under the
# terms of the BSD-3 license. We welcome feedback and contributions, see file
# CONTRIBUTING.md for details.

# Variables corresponding to defines in config.hpp (YES, NO, or value)
MFEM_VERSION           = 40200
MFEM_VERSION_STRING    = 4.2.0
MFEM_SOURCE_DIR        = /__w/PyMFEM/PyMFEM/PyMFEM/external/mfem
MFEM_INSTALL_DIR       = /__w/PyMFEM/PyMFEM/PyMFEM/build/bdist.linux-x86_64/wheel/mfem/ser
MFEM_GIT_STRING        = (unknown)
MFEM_USE_MPI           = NO
MFEM_USE_METIS         = NO
MFEM_USE_METIS_5       = NO
MFEM_DEBUG             = NO
MFEM_USE_EXCEPTIONS    = YES
MFEM_USE_ZLIB          = NO
MFEM_USE_LIBUNWIND     = NO
MFEM_USE_LAPACK        = NO
MFEM_THREAD_SAFE       = NO
MFEM_USE_LEGACY_OPENMP = NO
MFEM_USE_OPENMP        = NO
MFEM_USE_MEMALLOC      = YES
MFEM_TIMER_TYPE        = 2
MFEM_USE_SUNDIALS      = NO
MFEM_USE_MESQUITE      = NO
MFEM_USE_SUITESPARSE   = NO
MFEM_USE_SUPERLU       = NO
MFEM_USE_SUPERLU5      = OFF
MFEM_USE_STRUMPACK     = NO
MFEM_USE_GINKGO        = NO
MFEM_USE_AMGX          = NO
MFEM_USE_GNUTLS        = NO
MFEM_USE_NETCDF        = NO
MFEM_USE_PETSC         = NO
MFEM_USE_SLEPC         = NO
MFEM_USE_MPFR          = NO
MFEM_USE_SIDRE         = NO
MFEM_USE_CONDUIT       = NO
MFEM_USE_PUMI          = NO
MFEM_USE_HIOP          = OFF
MFEM_USE_GSLIB         = NO
MFEM_USE_CUDA          = NO
MFEM_USE_HIP           = 
MFEM_USE_RAJA          = NO
MFEM_USE_OCCA          = NO
MFEM_USE_CEED          = OFF
MFEM_USE_UMPIRE        = NO
MFEM_USE_SIMD          = NO
MFEM_USE_ADIOS2        = NO
MFEM_USE_MKL_CPARDISO  = OFF

# Compiler, compile options, and link options
MFEM_CXX       = /opt/rh/devtoolset-8/root/usr/bin/c++
MFEM_HOST_CXX  = /opt/rh/devtoolset-8/root/usr/bin/c++
MFEM_CPPFLAGS  = 
MFEM_CXXFLAGS  = -O3 -DNDEBUG -std=c++11
MFEM_TPLFLAGS  = 
MFEM_INCFLAGS  = -I$(MFEM_INC_DIR) $(MFEM_TPLFLAGS)
MFEM_PICFLAG   = -fPIC
MFEM_FLAGS     = $(MFEM_CPPFLAGS) $(MFEM_CXXFLAGS) $(MFEM_INCFLAGS)
MFEM_EXT_LIBS  =  rt
MFEM_LIBS      = -Wl,-rpath,$(MFEM_LIB_DIR) -L$(MFEM_LIB_DIR) -lmfem $(MFEM_EXT_LIBS)
MFEM_LIB_FILE  = $(MFEM_LIB_DIR)/libmfem.so.4.2.0
MFEM_STATIC    = NO
MFEM_SHARED    = YES
MFEM_BUILD_TAG = Linux-5.4.0-1039-azure
MFEM_PREFIX    = /__w/PyMFEM/PyMFEM/PyMFEM/build/bdist.linux-x86_64/wheel/mfem/ser
MFEM_INC_DIR   = /__w/PyMFEM/PyMFEM/PyMFEM/build/bdist.linux-x86_64/wheel/mfem/ser/include
MFEM_LIB_DIR   = /__w/PyMFEM/PyMFEM/PyMFEM/build/bdist.linux-x86_64/wheel/mfem/ser/lib

# Location of test.mk
MFEM_TEST_MK = /__w/PyMFEM/PyMFEM/PyMFEM/build/bdist.linux-x86_64/wheel/mfem/ser/share/mfem/test.mk

# Command used to launch MPI jobs
MFEM_MPIEXEC    = mpirun
MFEM_MPIEXEC_NP = -np
MFEM_MPI_NP     = 4

# The NVCC compiler cannot link with -x=cu
MFEM_LINK_FLAGS := $(filter-out -x=cu, $(MFEM_FLAGS))

# Optional extra configuration

