# adapted from F37 sources

%global releaseno 1

Name:           eccodes
Version:        2.25.0
Release:        %{releaseno}SIMC%{?dist}
Summary:        WMO data format decoding and encoding

# force the shared libraries to have these so versions
%global so_version       0.1
%global so_version_f90   0.1
%global datapack_date    20200626

# latest fedora-36 grib_api version is 1.27.0-12
# but this version number is to be updated as soon as we know
# what the final release of grib_api by upstream will be.
# latest upstream grib_api release is 1.28.0 (05-Dec-2018)
# as was written on https://confluence.ecmwf.int/display/GRIB/Home
# (Note that this page is no longer available, 17-Oct-2020)
%global final_grib_api_version 1.28.1-1%{?dist}

%ifarch i686 ppc64 s390x armv7hl
  %global obsolete_grib_api 0
%else
  %global obsolete_grib_api 1
%endif

# license remarks:
# Most of eccodes is licensed ASL 2.0 but a special case must be noted.
# These 2 files:
#     src/grib_yacc.c
#     src/grib_yacc.h
# contain a special exception clause that allows them to be
# relicensed if they are included in a larger project

License:        ASL 2.0

URL:            https://confluence.ecmwf.int/display/ECC/ecCodes+Home
Source0:        https://confluence.ecmwf.int/download/attachments/45757960/eccodes-%{version}-Source.tar.gz
# note: this data package is unversioned upstream but still it is updated
# now and then so rename the datapack using the download date
# to make it versioned in fedora
#Source1:        http://download.ecmwf.org/test-data/eccodes/eccodes_test_data.tar.gz#/eccodes_test_data_%{datapack_date}.tar.gz
# http protocol disabled in copr
Source1:        https://github.com/ARPA-SIMC/eccodes-rpm/releases/download/v%{version}-%{releaseno}/eccodes_test_data.tar.gz
# Add soversion to the shared libraries, since upstream refuses to do so
# https://software.ecmwf.int/issues/browse/SUP-1809
#Patch1:         eccodes-soversion.patch
Patch1:         https://raw.githubusercontent.com/ARPA-SIMC/eccodes-rpm/v%{version}-%{releaseno}/eccodes-soversion.patch

# note that the requests to make the other issues public are filed here:
# https://software.ecmwf.int/issues/browse/SUP-2073
# (and again, unfortunately this issue is not public)

# jasper3 now hides internal encoder / decoder. Use wrapper entry point
# c.f. https://github.com/jasper-software/jasper/commit/5fe57ac5829ec31396e7eaab59a688da014660af
# Also, now with jasper3, calling jas_stream_memopen (for example) always needs jasper
# library initialization
#Patch2:         eccodes-jasper3-use-wrapper-entry-point.patch
Patch2:         https://raw.githubusercontent.com/ARPA-SIMC/eccodes-rpm/v%{version}-%{releaseno}/eccodes-jasper3-use-wrapper-entry-point.patch

BuildRequires:  cmake >= 3.12
# forcing libarchive update in CentOS 8 from simc/stable repo
%{?el8:BuildRequires: libarchive >= 3.3.3}
BuildRequires:  gcc
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
# as explained in bugzilla #1562084
ExcludeArch: armv7hl

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

# remove executable permissions from c files
chmod 644 tigge/*.c
chmod 644 tools/*.c

# remove executable permissions from the authors and license file
chmod 644 AUTHORS LICENSE

%build

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

%if 0%{?fedora} >= 34
# we have working cmake3 macros
%else
pushd %{_vpath_builddir}
%define cmake_path 1
%endif

%cmake3 -DINSTALL_LIB_DIR=%{_lib} \
        -DCMAKE_INSTALL_MESSAGE=NEVER \
        -DENABLE_ECCODES_OMP_THREADS=ON \
        -DENABLE_EXTRA_TESTS=ON \
        -DENABLE_JPG=ON \
        -DENABLE_PNG=ON \
        -DENABLE_FORTRAN=ON \
        -DENABLE_NETCDF=ON \
        -DCMAKE_SKIP_INSTALL_RPATH=TRUE \
        -DECCODES_SOVERSION=%{so_version} \
        -DECCODES_SOVERSION_F90=%{so_version_f90} \
        -DCMAKE_Fortran_FLAGS="-fPIC" %{?cmake_path:..} \
        -DENABLE_PYTHON2=OFF

# note the final '..' is no longer needed to the cmake3 call.
# this is now hidden in the %%cmake3 macro

%cmake_build

%if 0%{?fedora} >= 34
# we have working cmake3 macros
%else
popd
%endif

# copy some include files to the build dir
# that are otherwise not found when creating the debugsource sub-package
cp fortran/eccodes_constants.h %{_vpath_builddir}/fortran/
cp fortran/grib_api_constants.h %{_vpath_builddir}/fortran/

%install
%if 0%{?fedora} >= 34
# we have working cmake3 macros
%else
pushd %{_vpath_builddir}
%endif

%cmake_install

%if 0%{?fedora} >= 34
# we have working cmake3 macros
%else
popd
%endif

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
%if 0%{?fedora} >= 34
ctest3 %{?_smp_mflags}
%else
ctest %{?_smp_mflags}
%endif

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
* Sun Mar 06 2022 Jos de Kloe <josdekloe@gmail.com> - 2.25.0-1
- Upgrade to upstream version 2.25.0
- Add new BR libaec-devel

* Mon Feb 14 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.24.0-4
- jasper3: use wrapper entry point for jpeg2000 decoder

* Sun Feb 13 2022 Josef Ridky <jridky@redhat.com> - 2.24.0-3
- Rebuilt for libjasper.so.6

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.24.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Dec 09 2021 Jos de Kloe <josdekloe@gmail.com> - 2.24.0-1
- Upgrade to upstream version 2.24.0
- Remove no longer needed patch2 (grib_to_netcdf test fix)

* Wed Dec  1 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.23.0-2
- Patch grib_api_internal.h for big endian test suite issue (upstream bug SUP-2410)

* Thu Sep 02 2021 Jos de Kloe <josdekloe@gmail.com> - 2.23.0-1
- Upgrade to upstream version 2.23.0

* Wed Aug 11 2021 Orion Poplawski <orion@nwra.com> - 2.22.1-4
- Rebuild for netcdf 4.8.0

* Tue Aug 10 2021 Orion Poplawski <orion@nwra.com> - 2.22.1-3
- Rebuild for netcdf 4.8.0

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.22.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jun 19 2021 Jos de Kloe <josdekloe@gmail.com> - 2.22.1-1
- Upgrade to upstream version 2.22.1

* Mon May 24 2021 Jos de Kloe <josdekloe@gmail.com> - 2.22.0-1
- Upgrade to upstream version 2.22.0

* Sun Mar 28 2021 Jos de Kloe <josdekloe@gmail.com> - 2.21.0-1
- Upgrade to upstream version 2.21.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.20.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan 23 2021 Jos de Kloe <josdekloe@gmail.com> - 2.20.0-1
- Upgrade to upstream version 2.20.0

* Fri Nov 13 2020 Jos de Kloe <josdekloe@gmail.com> - 2.19.1-1
- Upgrade to upstream version 2.19.1

* Sat Oct 17 2020 Jos de Kloe <josdekloe@gmail.com> - 2.19.0-1
- Upgrade to upstream version 2.19.0 and remove patch 1
- Add -fpic to the fortran flags (needed for compiling on armv7hl)

* Wed Aug 05 2020 Jos de Kloe <josdekloe@gmail.com> - 2.18.0-5
- Adapt the spec file to use the new style cmake macros

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.0-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jun 27 2020 Jos de Kloe <josdekloe@gmail.com> - 2.18.0-2
- Rebuild after fixing mistake in ExcludeArch statements

* Sat Jun 27 2020 Jos de Kloe <josdekloe@gmail.com> - 2.18.0-1
- Upgrade to upstream version 2.18.0

* Sun Mar 15 2020 Jos de Kloe <josdekloe@gmail.com> - 2.17.0-1
- Upgrade to upstream version 2.17.0
- Add explcit BR to perl(File::Compare) as needed by the tests now

* Sat Feb 08 2020 Jos de Kloe <josdekloe@gmail.com> - 2.16.0-1
- Upgrade to upstream version 2.16.0

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Dec 15 2019 Jos de Kloe <josdekloe@gmail.com> - 2.15.0-1
- Upgrade to upstream version 2.15.0

* Sun Oct 27 2019 Jos de Kloe <josdekloe@gmail.com> - 2.14.1-1
- Upgrade to upstream version 2.14.1

* Sat Aug 10 2019 Jos de Kloe <josdekloe@gmail.com> - 2.13.0-2
- apply bugfix to pc files contribuited by Emanuele Di Giacomo

* Thu Jul 25 2019 Jos de Kloe <josdekloe@gmail.com> - 2.13.0-1
- Upgrade to upstream version 2.13.0

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 09 2019 Jos de Kloe <josdekloe@gmail.com> - 2.12.5-1
- Upgrade to upstream version 2.12.5

* Mon Mar 18 2019 Orion Poplawski <orion@nwra.com> - 2.12.0-3
- Rebuild for netcdf 4.6.3

* Thu Feb 21 2019 Jos de Kloe <josdekloe@gmail.com> - 2.12.0-2
- bump final_grib_api_version global variable to 1.27.1, so just above the
  actual final version, to prevent the obsoletes to be disabled if the release
  gets bumped. See BZ #1677968

* Sun Feb 17 2019 Jos de Kloe <josdekloe@gmail.com> - 2.12.0-1
- Upgrade to upstream version 2.12.0

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

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
