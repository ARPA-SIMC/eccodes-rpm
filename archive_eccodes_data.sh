#!/bin/bash
set -ue

trap cleanup EXIT

cleanup()
{
    [[ -n "$workdir" ]] && rm -rf $workdir
}

outdir=$(readlink -f .)
pushd workdir
wget --recursive -nH --cut-dirs=3 --no-parent --directory-prefix=data http://download.ecmwf.org/test-data/grib_api/data/

pushd data
tar cvvfz $outdir/eccodes-data.tar.gz *
popd

popd
