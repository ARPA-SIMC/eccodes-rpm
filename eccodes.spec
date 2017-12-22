%if 0%{?rhel} == 7
%define python3_vers python34
%else
%define python3_vers python3
%endif

%global releaseno 2

Name:           eccodes
Version:        2.6.0
Release:        %{releaseno}%{?dist}
Summary:        Application programming interface and a set of tools for decoding and encoding messages in GRIB, BUFR and GTS
URL:            https://software.ecmwf.int/wiki/display/ECC/ecCodes+Home
Source0:        https://software.ecmwf.int/wiki/download/attachments/45757960/%{name}-%{version}-Source.tar.gz?api=v2#/%{name}-%{version}-Source.tar.gz
Source1:        http://download.ecmwf.org/test-data/grib_api/eccodes_test_data.tar.gz
Source2:        https://raw.githubusercontent.com/ARPA-SIMC/eccodes-rpm/v%{version}-%{releaseno}/PACKAGE-LICENSING
Patch0:         https://raw.githubusercontent.com/ARPA-SIMC/eccodes-rpm/v%{version}-%{releaseno}/eccodes-python3.patch
Patch1:         https://raw.githubusercontent.com/ARPA-SIMC/eccodes-rpm/v%{version}-%{releaseno}/eccodes-py3-fixes.patch
Patch2:         https://raw.githubusercontent.com/ARPA-SIMC/eccodes-rpm/v%{version}-%{releaseno}/eccodes-disable-download-tests.patch
Patch3:         https://raw.githubusercontent.com/ARPA-SIMC/eccodes-rpm/v%{version}-%{releaseno}/eccodes-numpy-fixes.patch
License:        Apache License, Version 2.0

BuildRequires:  gcc-c++
BuildRequires:  gcc-gfortran
BuildRequires:  cmake
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  perl
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libpng-devel
BuildRequires:  libaec-devel
BuildRequires:  jasper-devel
BuildRequires:  openjpeg2-devel
BuildRequires:  hdf5-devel
BuildRequires:  netcdf-devel
BuildRequires:  %{python3_vers}-devel
BuildRequires:  %{python3_vers}-numpy
BuildRequires:  swig

Provides:       grib_api = 1.23.0
Obsoletes:      grib_api < 1.23.0


%description
ecCodes is a package developed by ECMWF which provides an application programming interface and a set of tools for decoding and encoding messages in the following formats:

WMO FM-92 GRIB edition 1 and edition 2
WMO FM-94 BUFR edition 3 and edition 4 
WMO GTS abbreviated header (only decoding).

A useful set of command line tools provide quick access to the messages. C, Fortran 90 and Python interfaces provide access to the main ecCodes functionality.

ecCodes is an evolution of GRIB-API.  It is designed to provide the user with a simple set of functions to access data from several formats with a key/value approach.

For GRIB encoding and decoding, the GRIB-API functionality is provided fully in ecCodes with only minor interface and behaviour changes. Interfaces for C, Fortran 90 and Python are all maintained as in GRIB-API.  However, the GRIB-API Fortran 77 interface is no longer available.

In addition, a new set of functions with the prefix "codes_" is provided to operate on all the supported message formats. These functions have the same interface and behaviour as the "grib_" functions. 

A selection of GRIB-API tools has been included in ecCodes (ecCodes GRIB tools), while new tools are available for the BUFR (ecCodes BUFR tools) and GTS formats. The new tools have been developed to be as similar as possible to the existing GRIB-API tools maintaining, where possible, the same options and behaviour. A significant difference compared with GRIB-API tools is that bufr_dump produces output in JSON format suitable for many web based applications.

%package doc
Summary:        Application programming interface and a set of tools for decoding and encoding messages in GRIB, BUFR and GTS

%description doc
Documentation for eccodes.

%package devel
Summary:        Application programming interface and a set of tools for decoding and encoding messages in GRIB, BUFR and GTS
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libaec-devel
Requires:       libpng-devel
Requires:       libjpeg-turbo-devel

Provides:       grib_api-devel = 1.23.0
Obsoletes:      grib_api-devel < 1.23.0

%description devel
Header files and libraries for eccodes.

%package -n python3-%{name}
Summary:        Application programming interface and a set of tools for decoding and encoding messages in GRIB, BUFR and GTS
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{python3_vers}-numpy

%description -n python3-%{name}
Python3 bindings for eccodes.

%prep
%setup -q -n %{name}-%{version}-Source
%patch0
%patch1
%patch2
%patch3

%build
pushd python
swig -python -module gribapi_swig -o swig_wrap_numpy.c gribapi_swig.i
popd

mkdir build
pushd build

%cmake .. \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DINSTALL_LIB_DIR=%{_lib} \
    -DCMAKE_BUILD_TYPE=Release \
    -DENABLE_INSTALL_ECCODES_DEFINITIONS=ON \
    -DENABLE_INSTALL_ECCODES_SAMPLES=ON \
    -DENABLE_PNG=ON \
    -DENABLE_AEC=ON \
    -DENABLE_RPATHS=OFF \
    -DENABLE_RELATIVE_RPATHS=OFF \
    -DENABLE_MEMFS=ON \
    -DHAVE_BIT_REPRODUCIBLE=ON \
    -DENABLE_EXAMPLES=OFF \
    -DENABLE_NETCDF=ON \
    -DENABLE_PYTHON=ON \
    -DENABLE_FORTRAN=ON \
    -DENABLE_ALIGN_MEMORY=ON \
    -DENABLE_GRIB_TIMER=ON \
    -DENABLE_ECCODES_OMP_THREADS=ON \
    -DENABLE_PYTHON=ON \
    -DPYTHON_EXECUTABLE=%{__python3}

%{make_build}

popd

%check
# It seems that some tests look for the data in data/ and other tests look for
# the data in build/data...
tar axpf %{SOURCE1}

pushd build
tar axpf %{SOURCE1}
ctest
popd

%install
pushd build
%{make_install}

pushd %{buildroot}%{_libdir}
for l in libeccodes.so libeccodes_f90.so libeccodes_memfs.so
do
    mv $l $l.0.0.0
    ln -s $l.0.0.0 $l.0
    ln -s $l.0.0.0 $l
done
popd

pushd %{buildroot}%{_bindir}
for b in bufr_count grib_count
do
    rm $b
    ln -s codes_count $b
done
popd

popd

chmod 644 README ChangeLog AUTHORS
cp %{SOURCE2} .

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc README ChangeLog AUTHORS
%license PACKAGE-LICENSING
%{_bindir}/*
%{_libdir}/*.so.0*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/definitions

%files doc
%doc %{_datadir}/%{name}/ifs_samples/
%doc %{_datadir}/%{name}/samples/
%doc html
%doc examples

%files devel
%{_datadir}/%{name}/cmake
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files -n python3-%{name}
%{python3_sitearch}


%changelog
* Fri Dec 22 2017 Emanuele Di Giacomo <edigiacomo@arpae.it> - 2.6.0-2
- New eccodes version
- Fix SWIG for Python3 support

* Tue Dec 19 2017 Emanuele Di Giacomo <edigiacomo@arpae.it> - 2.5.0-2
- Python3 support
- Fixed spec

* Fri Dec 15 2017 Enrico Barca <enrico.barca@yacme.com> - 2.5.0-1
- Prima pacchettizzazione per f24
