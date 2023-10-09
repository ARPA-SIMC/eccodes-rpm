%global releaseno 0.2

Name:           eccodes
Version:        2.32.0
Release:        %{releaseno}%{?dist}
Summary:        WMO data format decoding and encoding

# force the shared libraries to have these so versions
%global so_version       0.1
%global so_version_f90   0.1
%global datapack_date    20220526

# latest fedora-38/rawhide grib_api version is 1.27.0-18
# but this version number is to be updated as soon as we know
# what the final release of grib_api by upstream will be.
# latest upstream grib_api release is 1.28.0 (05-Dec-2018)
# as was written on https://confluence.ecmwf.int/display/GRIB/Home
# (Note that this page is no longer available, 17-Oct-2020)
%global final_grib_api_version 1.28.1-1%{?dist}

%ifarch i686 ppc64 armv7hl
  %global obsolete_grib_api 0
%else
  %global obsolete_grib_api 1
%endif

# license remarks:
# Most of eccodes is licensed ASL 2.0 (which is identical to the SPDX
# identifier Apache-2.0) but a special case must be noted.
# These 2 files:
#     src/grib_yacc.c
#     src/grib_yacc.h
# contain a special exception clause that allows them to be
# relicensed if they are included in a larger project

License:        Apache-2.0

URL:            https://confluence.ecmwf.int/display/ECC/ecCodes+Home
Source0:        https://confluence.ecmwf.int/download/attachments/45757960/eccodes-%{version}-Source.tar.gz

# note: this data package is unversioned upstream but still it is updated
# now and then so rename the datapack using the download date
# to make it versioned in fedora
Source1:        https://get.ecmwf.int/repository/test-data/eccodes/eccodes_test_data.tar.gz#/eccodes_test_data_%{datapack_date}.tar.gz

# Add soversion to the shared libraries, since upstream refuses to do so
# https://jira.ecmwf.int/browse/SUP-1809
Patch1:         https://raw.githubusercontent.com/ARPA-SIMC/eccodes-rpm/v%{version}-%{releaseno}/eccodes-soversion.patch

# note that the requests to make the other issues public are filed here:
# https://jira.ecmwf.int/browse/SUP-2073
# (and again, unfortunately this issue is not public)

BuildRequires:  cmake3
BuildRequires:  gcc-c++
BuildRequires:  gcc-gfortran
BuildRequires:  /usr/bin/git
BuildRequires:  jasper-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  netcdf-devel
BuildRequires:  openjpeg2-devel
BuildRequires:  libaec-devel

# For tests
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(File::Compare)

# For creation of man pages
BuildRequires:  help2man

# the data is needed by the library and all tools provided in the main package
# the other way around, the data package could be installed without
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

%if 0%{obsolete_grib_api}
# as stated in the note above, setting provides seems not correct here
# Provides:       grib_api = %%{final_grib_api_version}
Obsoletes:      grib_api < %{final_grib_api_version}
%endif

# as explained in bugzilla #1562066
ExcludeArch: i686
# as explained in bugzilla #1562071
#  note: this is no longer part of fc30/rawhide
#  but the exclude is still needed for EPEL-7 and EPEL-8
ExcludeArch: ppc64
# as explained in bugzilla #1562076
#ExcludeArch: s390x
# as explained in bugzilla #1562084
#ExcludeArch: armv7hl

%if 0%{?rhel} >= 7
# as explained in bugzilla #1629377
ExcludeArch: aarch64
%endif

%description
ecCodes is a package developed by ECMWF which provides an application
programming interface and a set of tools for decoding and encoding messages
in the following formats:

 *  WMO FM-92 GRIB edition 1 and edition 2
 *  WMO FM-94 BUFR edition 3 and edition 4 
 *  WMO GTS abbreviated header (only decoding).

A useful set of command line tools provide quick access to the messages. C,
and Fortran 90 interfaces provide access to the main ecCodes functionality.

ecCodes is an evolution of GRIB-API.  It is designed to provide the user with
a simple set of functions to access data from several formats with a key/value
approach.

For GRIB encoding and decoding, the GRIB-API functionality is provided fully
in ecCodes with only minor interface and behaviour changes. Interfaces for C,
and Fortran 90 are all maintained as in GRIB-API.  However, the
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

%if 0%{obsolete_grib_api}
# Provides:   grib_api-devel = %%{final_grib_api_version}
Obsoletes:  grib_api-devel < %{final_grib_api_version}
%endif

%description devel
Header files and libraries for ecCodes.

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
in C, and Fortran 90.

#####################################################
%prep
%autosetup -n %{name}-%{version}-Source -p1

# unpack the test data below build
mkdir -p %{_vpath_builddir}
pushd %{_vpath_builddir}
tar xf %SOURCE1
popd

%build

%if 0%{?rhel} == 8
pushd %{_vpath_builddir}
%endif

#-- The following features are disabled by default and not switched on:
#
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
#-- The following features are set to AUTO by default and
#   explicitely switched on to ensure they don't vanish unnoticed
#   in case of dependency problems during the build:
# * ENABLE_JPG
# ^ ENABLE_FORTRAN
# * ENABLE_NETCDF
#   NetCDF is only needed to create the grib_to_netcdf convert tool
#
# * ENABLE_PYTHON has value AUTO as default, so if python2 is available
#   during a package build it will build an interface for it.
#   To make sure it does not do so,  explicitely switch it off.
#   Python3 support has been moved to an additional project now,
#   so python handling has been removed completely from this spec file.
#
#-- Also add an explicit option to not use rpath
#
# Note: -DINSTALL_LIB_DIR=%%{_lib} is needed because otherwise
#        the library so files get installed in /usr/lib in stead
#        of /usr/lib64 on x86_64.

# added -DCMAKE_Fortran_FLAGS="-fPIC"
# because the koji build crashes with the error that it needs this setting
# when I try to build for armv7hl (other archs do not complain ......)
# I have no idea what causes this difference in behaviour.

%cmake3 -DINSTALL_LIB_DIR=%{_lib} \
        -DENABLE_ECCODES_OMP_THREADS=ON \
        -DENABLE_EXTRA_TESTS=ON \
        -DENABLE_JPG=ON \
        -DENABLE_PNG=ON \
        -DENABLE_FORTRAN=ON \
        -DENABLE_NETCDF=ON \
        -DCMAKE_SKIP_INSTALL_RPATH=TRUE \
        -DECCODES_SOVERSION=%{so_version} \
        -DECCODES_SOVERSION_F90=%{so_version_f90} \
        -DCMAKE_Fortran_FLAGS="-fPIC" \
        -DENABLE_PYTHON2=OFF \
        -DENABLE_AEC=ON \
%if 0%{?rhel} == 8
        ..
%endif

%if 0%{?rhel} == 8
%make_build
%else
%cmake_build
%endif

%if 0%{?rhel} == 8
popd
%endif

# copy some include files to the build dir
# that are otherwise not found when creating the debugsource sub-package
cp fortran/eccodes_constants.h %{_vpath_builddir}/fortran/
cp fortran/grib_api_constants.h %{_vpath_builddir}/fortran/

%install
%make_install -C %{_vpath_builddir}
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

# Fix permissions
chmod 644 AUTHORS LICENSE

# also not needed for x86_64
# maybe they fixed it for all archs?
#%%ifarch i686 armv7hl
#  # pass (nothing to do)
#%%else
#  # it seems pkgconfig files end up in lib in stead of lib64 now
#  # so move them to the right place
#  mv %%{buildroot}/%%{_usr}/lib/pkgconfig/ \
#     %%{buildroot}/%%{_libdir}/pkgconfig/
#%%endif

# It seems the cmake options
# -DCMAKE_SKIP_RPATH=TRUE
# -DCMAKE_SKIP_INSTALL_RPATH=TRUE
# have no effect on the generated *.pc files.
# These still contain an rpath reference, so patch them and remove 
# the rpath using sed
sed -i 's|^libs=.*$|libs=-L${libdir} -leccodes|g' %{buildroot}/%{_libdir}/pkgconfig/eccodes.pc
sed -i 's|^libs=.*$|libs=-L${libdir} -leccodes_f90 -leccodes|g' %{buildroot}/%{_libdir}/pkgconfig/eccodes_f90.pc

%ldconfig_scriptlets

%check
cd  %{_vpath_builddir}

# notes:
# * the LD_LIBRARY_PATH setting is required to let the tests
#   run inside the build dir, otherwise they are broken due to
#   the removal of rpath
# * the LIBRARY_PATH setting is needed te let the
#   'eccodes_t_bufr_dump_(de|en)code_C' tests run.
#   These tests compile on the fly generated C code, and
#   without this setting the loader does not find the libraries.
# * this is a 'non-standard' use of ctest3 so it does currently not
#   work with the %%ctest macro.

LD_LIBRARY_PATH=%{buildroot}/%{_libdir} \
LIBRARY_PATH=%{buildroot}/%{_libdir} \
ctest3 -v %{?_smp_mflags}
# Remove the extra verbose option because it conflicts with moncic-ci
# ctest3 -V %{?_smp_mflags}

%files
%license LICENSE
%doc README.md ChangeLog AUTHORS NEWS NOTICE
%{_bindir}/*
%{_libdir}/*.so.*

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
* Mon Oct 09 2023 Emanuele Di Giacomo <edigiacomo@arpae.it> - 2.32.0-0.1
- Pre-release 2.32.0-0.1 waiting for EPEL release

* Sat Sep 09 2023 Jos de Kloe <josdekloe@gmail.com> - 2.31.0-1
- Upgrade to upstream version 2.31.0

* Thu May 18 2023 Jos de Kloe <josdekloe@gmail.com> - 2.30.0-1
- Upgrade to upstream version 2.30.0
- explicitly switch on ENABLE_AEC
- migrated to SPDX license

* Wed Jun 1 2022 Jos de Kloe <josdekloe@gmail.com> - 2.26.0-1
- Upgrade to upstream version 2.26.0

* Mon Oct 11 2021 Jos de Kloe <josdekloe@gmail.com> - 2.23.0-1
- Upgrade to upstream version 2.23.0

* Sat Jun 27 2020 Jos de Kloe <josdekloe@gmail.com> - 2.18.0-1
- Upgrade to upstream version 2.18.0

* Sun Oct 27 2019 Jos de Kloe <josdekloe@gmail.com> - 2.14.1-1
- Upgrade to upstream version 2.14.1

* Sat Nov 24 2018 Jos de Kloe <josdekloe@gmail.com> - 2.9.2-1
- Upgrade to upstream version 2.9.2

* Sun Oct 7 2018 Jos de Kloe <josdekloe@gmail.com> - 2.9.0-1
- Upgrade to upstream version 2.9.0

* Sat Sep 15 2018 Jos de Kloe <josdekloe@gmail.com> - 2.8.2-4
- add Excludearch for aarch64 on epel7

* Sat Sep 15 2018 Jos de Kloe <josdekloe@gmail.com> - 2.8.2-3
- Explicitely disable python in cmake call and use ctest3 rather than ctest
  to ensure the build runs on EPEL-7 as well

* Thu Sep 13 2018 Jos de Kloe <josdekloe@gmail.com> - 2.8.2-2
- Remove python2 sub-package as per Mass Python 2 Package Removal for f30

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
  as suggested by Robert-Andre Mauchin
- Add a documentation and a data sub-package
- Change the license and add a note explaining why this was done

* Fri Mar 24 2017 Orion Poplawski <orion@cora.nwra.com> - 2.2.0-1
- Initial Fedora package
