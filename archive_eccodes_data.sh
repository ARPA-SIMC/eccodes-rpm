#!/bin/bash
set -ue

trap cleanup EXIT

cleanup()
{
    [[ -n "$workdir" ]] && rm -rf $workdir
}

version=$1
outdir=$PWD
pkgfile=eccodes-${version}-Source.tar.gz
pkgurl="https://software.ecmwf.int/wiki/download/attachments/45757960/${pkgfile}?api=v2"
dataurl="http://download.ecmwf.org/test-data/grib_api/data/"
workdir=$(mktemp -d)
listfile=$workdir/list

pushd $workdir
wget --no-verbose -O $pkgfile $pkgurl
tar xvvf $pkgfile
pushd ${pkgfile%.tar.gz}

pushd data
while read l
do
    d=$(dirname $l | sed -e 's,^\./,,g')
    sed -e "s,^,$dataurl/$d/,g" < $l >> $listfile
done < <(find . -name "*_files.txt")
popd

popd

xargs -d '\n' wget --no-verbose -x -nH --cut-dirs=3 --directory data < $listfile

pushd data
tar cvvfz $outdir/eccodes-data.tar.gz *
popd

popd
