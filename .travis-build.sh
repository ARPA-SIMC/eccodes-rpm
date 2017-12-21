#!/bin/bash
set -ex

image=$1

if [[ $image =~ ^centos: ]]
then
    pkgcmd="yum"
    builddep="yum-builddep"
    sed -i '/^tsflags=/d' /etc/yum.conf
    yum install -y epel-release
    yum install -y @buildsys-build
    yum install -y yum-utils
    yum install -y git
    yum install -y rpmdevtools
elif [[ $image =~ ^fedora: ]]
then
    pkgcmd="dnf"
    builddep="dnf builddep"
    sed -i '/^tsflags=/d' /etc/dnf/dnf.conf
    dnf install -y @buildsys-build
    dnf install -y 'dnf-command(builddep)'
    dnf install -y git
    dnf install -y rpmdevtools
fi

$builddep -y eccodes.spec

if [[ $image =~ ^fedora: || $image =~ ^centos: ]]
then
    pkgname="$(rpmspec -q --qf="eccodes-%{version}-%{release}\n" eccodes.spec | head -n1)"
    mkdir -p ~/rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
    cp eccodes.spec eccodes-py3-fixes.patch eccodes-python3.patch ~/rpmbuild/SPECS/
    spectool -g -R ~/rpmbuild/SPECS/eccodes.spec
    rpmbuild -ba ~/rpmbuild/SPECS/eccodes.spec &>/dev/null
    find ~/rpmbuild/{RPMS,SRPMS}/ -name "${pkgname}*rpm" -exec cp -v {} . \;
    # TODO upload ${pkgname}*.rpm to github release on deploy stage
else
    echo "Unsupported image"
    exit 1
fi
