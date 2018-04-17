# rpm packaging files for ecCodes


## Build status


| Environment | Status |
| ----------- | ------ |
| CentOS 7    | [![Build Status](https://badges.herokuapp.com/travis/ARPA-SIMC/eccodes-rpm?branch=master&env=DOCKER_IMAGE=centos:7&label=centos7)](https://travis-ci.org/ARPA-SIMC/eccodes-rpm) |
| Fedora 26   | [![Build Status](https://badges.herokuapp.com/travis/ARPA-SIMC/eccodes-rpm?branch=master&env=DOCKER_IMAGE=fedora:26&label=fedora26)](https://travis-ci.org/ARPA-SIMC/eccodes-rpm) |
| Fedora 27   | [![Build Status](https://badges.herokuapp.com/travis/ARPA-SIMC/eccodes-rpm?branch=master&env=DOCKER_IMAGE=fedora:27&label=fedora27)](https://travis-ci.org/ARPA-SIMC/eccodes-rpm) |
| Fedora 28   | [![Build Status](https://badges.herokuapp.com/travis/ARPA-SIMC/eccodes-rpm?branch=master&env=DOCKER_IMAGE=fedora:28&label=fedora28)](https://travis-ci.org/ARPA-SIMC/eccodes-rpm) |


## Introduction


This github repository neither hosts nor provide ecCodes sources, it's meant to
host (unofficial) convenience files for Fedora and CentOs rpm packaging.

ecCodes is a package developed by ECMWF which provides an application
programming interface and a set of tools for decoding and encoding messages in
GRIB e BUFR formats. For more info see:
https://software.ecmwf.int/wiki/display/ECC/ecCodes+Home

Python 3 patches are adapted from the one provided in debian package. For more
info see: https://tracker.debian.org/pkg/eccodes


## License

Apache 2.0

## Authors

* Emanuele Di Giacomo <edigiacomo@arpae.it>
* Daniele Branchini <dbranchini@arpae.it>
* Alastair McKinstry <mckinstry@debian.org>
