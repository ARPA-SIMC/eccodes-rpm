Name:           eccodes
Version:        2.8.2
Release:        1%{?dist}
Summary:        WMO data format decoding and encoding

# force the shared libraries to have these so versions
%global so_version       0.1
%global so_version_f90   0.1
%global datapack_date    20180705

# latest rawhide grib_api version is 1.27.0-1
# but this version number is to be updated as soon as we know
# what the final release of grib_api by upstream will be.
# latest upstream grib_api release is 1.27.0 (09-Sep-2018)
%global final_grib_api_version 1.27.0-1

# license remarks:
# most of eccodes is licensed ASL 2.0 but a special case must be noted.
# these 2 files:
#     src/grib_yacc.c
#     src/grib_yacc.h
# contain a special exception clause that allows them to be
# relicensed if they are included in a larger project

License:        ASL 2.0

URL:            https://software.ecmwf.int/wiki/display/ECC/ecCodes+Home
Source0:        https://software.ecmwf.int/wiki/download/attachments/45757960/eccodes-%{version}-Source.tar.gz
# note: this data package is unversioned upstream but still it is updated
# now and then. The current copy was downloaded 05-Jul-2018
# todo: rename the datapack using the download date to make it versioned
#       in fedora and figure out how to insert this in this Source1 entry
Source1:        http://download.ecmwf.org/test-data/eccodes/eccodes_test_data.tar.gz
# Support 32-bit
# https://software.ecmwf.int/issues/browse/SUP-1813
# (unfortunately this issue is not public)
Patch1:         eccodes-32bit.patch
# Add soversion to the shared libraries, since upstream refuses to do so
# https://software.ecmwf.int/issues/browse/SUP-1809
Patch2:         eccodes-soversion.patch
# remove rpath from cmake/pkg-config.pc.in
Patch3:         eccodes-rpath.patch
# fix compile flags in fortran checks
# this is needed due to rpath removal
Patch4:         eccodes-fortran-check.patch

# note that the requests to make the other issues public are filed here:
# https://software.ecmwf.int/issues/browse/SUP-2073
# (and again, unfortunately this issue is not public)

BuildRequires:  cmake3
BuildRequires:  gcc
BuildRequires:  gcc-gfortran
BuildRequires:  /usr/bin/git
BuildRequires:  jasper-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  netcdf-devel
BuildRequires:  numpy
BuildRequires:  openjpeg2-devel
BuildRequires:  python2-devel

# For tests
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(Test::More)

# the data is needed by the library and all tools provided in the main package
# the other way arpund, the data package could be installed without
# installing the base package. It will probably be pretty useless,
# unless a user wishes to read and study all these grib and bufr
# file format definitions.
Requires: %{name}-data = %{version}-%{release}

# NOTE: upstream writes:
# """
# For GRIB encoding and decoding, the GRIB-API functionality is provided
# fully in ecCodes with only minor interface and behaviour changes.
# Interfaces for C, Fortran 90 and Python are all maintained as in GRIB-API.
# However, the GRIB-API Fortran 77 interface is no longer available.
# """
# Therefore, since the library name and pkg-config file content changes
# and fortran77 support was removed, this replacement package cannot be
# considered compatible enough and no Provides can be defined.
#
# Furthermore, upstream writes:
# "Please note that GRIB-API support is being discontinued at the end of 2018."
# So the old grib_api will need to be obsoleted.

Obsoletes:      grib_api < %{final_grib_api_version}

# as explained in bugzilla #1562066
#ExcludeArch: i686
# as explained in bugzilla #1562071
#ExcludeArch: ppc64
# as explained in bugzilla #1562076
#ExcludeArch: s390x
# as explained in bugzilla #1562084
#ExcludeArch: armv7hl

%description
ecCodes is a package developed by ECMWF which provides an application
programming interface and a set of tools for decoding and encoding messages
in the following formats:

 *  WMO FM-92 GRIB edition 1 and edition 2
 *  WMO FM-94 BUFR edition 3 and edition 4 
 *  WMO GTS abbreviated header (only decoding).

A useful set of command line tools provide quick access to the messages. C,
Fortran 90 and Python interfaces provide access to the main ecCodes
functionality.

ecCodes is an evolution of GRIB-API.  It is designed to provide the user with
a simple set of functions to access data from several formats with a key/value
approach.

For GRIB encoding and decoding, the GRIB-API functionality is provided fully
in ecCodes with only minor interface and behaviour changes. Interfaces for C,
Fortran 90 and Python are all maintained as in GRIB-API.  However, the
GRIB-API Fortran 77 interface is no longer available.

In addition, a new set of functions with the prefix "codes_" is provided to
operate on all the supported message formats. These functions have the same
interface and behaviour as the "grib_" functions. 

A selection of GRIB-API tools has been included in ecCodes (ecCodes GRIB
tools), while new tools are available for the BUFR (ecCodes BUFR tools) and
GTS formats. The new tools have been developed to be as similar as possible
to the existing GRIB-API tools maintaining, where possible, the same options
and behaviour. A significant difference compared with GRIB-API tools is that
bufr_dump produces output in JSON format suitable for many web based
applications.

#####################################################
%package devel
Summary:    Contains ecCodes development files
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   gcc-gfortran%{?_isa}
Requires:   jasper-devel%{?_isa}

Obsoletes:  grib_api-devel < %{final_grib_api_version}

%description devel
Header files and libraries for ecCodes.

#####################################################
%package -n python2-%{name}
Summary:    A python2 interface to ecCodes
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   gcc-gfortran%{?_isa}
Requires:   jasper-devel%{?_isa}

# a sub package python2-grib_api did not exist
# so no obsoletes needed here

%description -n python2-%{name}
A python2 interface to ecCodes. Also a legacy interface to gribapi is provided.

#####################################################
# note: python3 is not yet supported by eccodes
#       but upstream intents to make it available before the end of 2018

#####################################################
%package data
Summary:    Data needed by the eccodes library and tools
BuildArch:  noarch

%description data
This package provides all tables and definitions needed
to encode and decode grib and bufr files, and includes
both the official WMO tables and a number of often used
local definitions by ECMWF and other meteorological centers.

#####################################################
%package doc
Summary:    Documentation and example code
BuildArch:  noarch

# a sub package grib_api-doc did not exist
# so no obsoletes needed here

%description doc
This package contains the html documentation for ecCodes
and a fair number of example programs and scripts to use it
in C, Fortran 90, and Python.

#####################################################
%prep
%autosetup -n %{name}-%{version}-Source -p1

# unpack the test data below build
mkdir build
cd build
tar xf %SOURCE1

# remove executable permissions from c files
cd ..
chmod 644 tigge/*.c
chmod 644 tools/*.c

# remove executable permissions from the authors and license file
chmod 644 AUTHORS LICENSE

%build
cd build

#-- The following features are disabled by default and not switched on:
#
# * AEC , support for Adaptive Entropy Coding
# * MEMFS , Memory based access to definitions/samples
# * MEMORY_MANAGEMENT , enable memory management
# * ALIGN_MEMORY , enable memory alignment
# * GRIB_TIMER , enable timer
# * ECCODES_THREADS , enable POSIX threads
#
#-- The following features are disabled by default and switched on:
# * PNG , support for PNG decoding/encoding
# * ECCODES_OMP_THREADS , enable OMP threads
# * EXTRA_TESTS , enable extended regression testing
#
#-- Also add an explicit option to not use rpath
#
# Note: -DINSTALL_LIB_DIR=%%{_lib} is needed because otherwise
#        the library so files get installed in /usr/lib in stead
#        of /usr/lib64 on x86_64.
# Note: -DPYTHON_EXECUTABLE was added to prevent deprecation warnings
#        during running of tests which breaks
#        Test #184: eccodes_p_grib_keys_iterator_test

%cmake3 -DINSTALL_LIB_DIR=%{_lib} \
        -DENABLE_ECCODES_OMP_THREADS=ON \
        -DENABLE_EXTRA_TESTS=ON \
        -DENABLE_PNG=ON \
        -DCMAKE_SKIP_RPATH=TRUE \
        -DECCODES_SOVERSION=%{so_version} \
        -DECCODES_SOVERSION_F90=%{so_version_f90} \
        -DPYTHON_EXECUTABLE=%{_bindir}/python2 \
        ..

%make_build

# copy some include files to the build dir
# that are otherwise not found when creating the debugsource subpackage
cd ..
cp fortran/eccodes_constants.h build/fortran/
cp fortran/grib_api_constants.h build/fortran/

%install
%make_install -C build
mkdir -p %{buildroot}%{_fmoddir}
mv %{buildroot}%{_includedir}/*.mod %{buildroot}%{_fmoddir}/

# remove a script that does not belong in the doc section
# and triggers an rpmlint error
rm %{buildroot}%{_datadir}/%{name}/definitions/installDefinitions.sh
# by the way, is there a way in the files section to include a directory
# but exclude a given file in it? I could not find such a trick.

# copy the html documentation to the install directory
mkdir -p %{buildroot}%{_datadir}/doc/%{name}/
cp -r html %{buildroot}%{_datadir}/doc/%{name}/
# and remove an unneeded Makefile from the html directory
rm %{buildroot}%{_datadir}/doc/%{name}/html/Makefile.am

# copy the example scripts/programs to the install directory
# but dont copy the shell scripts and Makefiles, since these
# are part of the cmake test setup and not usefull as example.
# Use %%{_datadir}/doc/%%{name}/ rather than %%{_datadir}/%%{name}/
# otherwise the rpmbuild will create a lot off unnecessary
# pyc and pyo files.

mkdir -p %{buildroot}%{_datadir}/doc/%{name}/examples/C
cp examples/C/*.c %{buildroot}%{_datadir}/doc/%{name}/examples/C
mkdir -p %{buildroot}%{_datadir}/doc/%{name}/examples/F90
cp examples/F90/*.f90 %{buildroot}%{_datadir}/doc/%{name}/examples/F90
mkdir -p %{buildroot}%{_datadir}/doc/%{name}/examples/python
cp examples/python/*.py %{buildroot}%{_datadir}/doc/%{name}/examples/python
cp examples/python/*.c %{buildroot}%{_datadir}/doc/%{name}/examples/python
cp examples/python/*.csv %{buildroot}%{_datadir}/doc/%{name}/examples/python

# adapt a shebang to make it point explicitely to python2
sed -i -e 's/\/bin\/env python/\/usr\/bin\/python2/' \
    %{buildroot}%{_datadir}/doc/%{name}/examples/python/high_level_api.py

# move cmake files to the cmake folder below libdir
# as suggested in the review request
mkdir -p %{buildroot}%{_libdir}/cmake/%{name}/
mv %{buildroot}%{_datadir}/%{name}/cmake/* %{buildroot}%{_libdir}/cmake/%{name}/

%ldconfig_scriptlets

%check
cd build

# notes:
# * the LD_LIBRARY_PATH setting is required to let the tests
#   run inside the build dir, otherwise they are broken due to
#   the removal of rpath
# * the LIBRARY_PATH setting is needed te let the
#   'eccodes_t_bufr_dump_(de|en)code_C' tests run.
#   These tests compile on the fly generated C code, and
#   without this setting the loader does not find the libraries.
# 
# These fail due to build flag issues, i.e. the test script does a
# test build of some on the fly generated fortran code, but cannot
# find the necessary *.mod fortran module definition files.
# There is no easy way to define this as environment setting,
# so a patch has been added to solve this for now.
# See: https://software.ecmwf.int/issues/browse/SUP-1812
# (unfortunately this issue is not public)
LD_LIBRARY_PATH=%{buildroot}/%{_libdir} \
LIBRARY_PATH=%{buildroot}/%{_libdir} \
ctest -V %{?_smp_mflags}

%files
%license LICENSE
%doc README ChangeLog AUTHORS
%{_bindir}/*
%{_libdir}/*.so.*

%files -n python2-%{name}
%{python2_sitearch}/%{name}
%{python2_sitearch}/%{name}-*-py*.egg-info
%{python2_sitearch}/gribapi

%files devel
%{_includedir}/*
%{_fmoddir}/%{name}.mod
%{_fmoddir}/grib_api.mod
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/%{name}_f90.pc
%{_libdir}/*.so
%dir %{_libdir}/cmake/%{name}
%{_libdir}/cmake/%{name}/*

%files data
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/definitions/
%{_datadir}/%{name}/samples/
%{_datadir}/%{name}/ifs_samples/

%files doc
%doc %{_datadir}/doc/%{name}/

%changelog

* Sun Sep 9 2018 Jos de Kloe <josdekloe@gmail.com> - 2.8.2-1
- Upgrade to version 2.8.2

* Fri Aug 17 2018 Jos de Kloe <josdekloe@gmail.com> - 2.8.0-3
- rebuild with patch provided by Matthew Krupcale for f28

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 5 2018 Jos de Kloe <josdekloe@gmail.com> - 2.8.0-1
- Upgrade to version 2.8.0

* Tue May 08 2018 Jos de Kloe <josdekloe@gmail.com> - 2.7.3-1
- Upgrade to version 2.7.3
- adjust latest grib_api version to 1.26.1-1

* Thu Mar 29 2018 Jos de Kloe <josdekloe@gmail.com> - 2.7.0-2
- added ExcludeArch statements for the failing architectures

* Thu Mar 22 2018 Jos de Kloe <josdekloe@gmail.com> - 2.7.0-1
- Upgrade to version 2.7.0
- Fix rpath and some permission issues
- Remove Provides, add post/postun sections, add LD_LIBRARY_PATH
- Fix failing tests in check section
- Implement so version because upstream refuses to do so
- Add fix for test failure 184 and ldconfig_scriptlets
  and move unversioned so file to devel package
  as suggested by Robert-André Mauchin
- Add a documentation and a data sub-package
- Change the license and add a note explaining why this was done

* Fri Mar 24 2017 Orion Poplawski <orion@cora.nwra.com> - 2.2.0-1
- Initial Fedora package
