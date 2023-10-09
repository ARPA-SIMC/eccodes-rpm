#!/bin/sh

# a simple script to create man pages for tools
# provided in the bin dir after installation of eccodes.
#
# Written by: J. de Kloe, 2022.

BINDIR=$1
DESTDIR=$2

if [ ! -e "$DESTDIR" ] ; then
   mkdir -p "$DESTDIR"
fi

for TOOL in "$BINDIR"/*
do
    BASENAME=$(basename "$TOOL")
    help2man --no-info --output="${DESTDIR}/${BASENAME}.1" "${TOOL}"
done

# currently (29-Aug-2022) help2man fails on these 5 tools:
# help2man: can't get `--help' info from ../bin/bufr_count
# help2man: can't get `--help' info from ../bin/codes_count
# help2man: can't get `--help' info from ../bin/grib2ppm
# help2man: can't get `--help' info from ../bin/grib_count
# help2man: can't get `--help' info from ../bin/gts_count

echo "done"
