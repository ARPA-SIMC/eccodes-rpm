#!/bin/bash
set -exo pipefail

image=$1

if [[ $image =~ ^centos:7 ]]
then
    pkgcmd="yum"
    builddep="yum-builddep"
    sed -i '/^tsflags=/d' /etc/yum.conf
    yum install -q -y epel-release
    yum install -q -y @buildsys-build
    yum install -q -y yum-utils
    yum install -q -y git
    yum install -q -y rpmdevtools
    yum install -q -y pv
elif [[ $image =~ ^centos:8 ]]
then
    pkgcmd="dnf"
    builddep="dnf builddep"
    sed -i '/^tsflags=/d' /etc/dnf/dnf.conf
    dnf install -q -y epel-release
    dnf install -q -y 'dnf-command(config-manager)'
    dnf config-manager --set-enabled powertools
    dnf groupinstall -q -y "Development Tools"
    dnf install -q -y 'dnf-command(builddep)'
    dnf install -q -y git
    dnf install -q -y rpmdevtools
    dnf install -q -y pv
    dnf copr enable -y simc/stable
    # the following lines are useless since cmake 3.18 has been integrated in simc/stable
    ## forcing update of recent cmake, needed for latest eccodes versions
    #dnf install -q -y libarchive libarchive-devel cmake cmake-rpm-macros --disablerepo=\* --enablerepo=appstream,powertools,baseos --releasever=8-stream --refresh
elif [[ $image =~ ^fedora: ]]
then
    pkgcmd="dnf"
    builddep="dnf builddep"
    sed -i '/^tsflags=/d' /etc/dnf/dnf.conf
    dnf install -q -y @buildsys-build
    dnf install -q -y 'dnf-command(builddep)'
    dnf install -q -y git
    dnf install -q -y rpmdevtools
    dnf install -q -y pv
fi

$builddep -q -y eccodes.spec

if [[ $image =~ ^fedora: || $image =~ ^centos: ]]
then
    pkgname="$(rpmspec -q --qf="eccodes-%{version}-%{release}\n" eccodes.spec | head -n1)"
    mkdir -p ~/rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
    cp eccodes.spec ~/rpmbuild/SPECS/
    cp *.patch ~/rpmbuild/SOURCES/
    spectool -g -R ~/rpmbuild/SPECS/eccodes.spec
    rpmbuild -ba ~/rpmbuild/SPECS/eccodes.spec 2>&1 | pv -q -L 3k
else
    echo "Unsupported image"
    exit 1
fi
