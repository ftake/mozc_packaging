#!/bin/bash

pushd mozc

git checkout .

vermajor=`sed -n -e "s/MAJOR = \(.*\)/\1/p" src/data/version/mozc_version_template.bzl`
verminor=`sed -n -e "s/MINOR = \(.*\)/\1/p" src/data/version/mozc_version_template.bzl`
verbuild=`sed -n -e "s/BUILD_OSS = \(.*\)/\1/p" src/data/version/mozc_version_template.bzl`
# REVISION is always 102 for Linux
version=$vermajor.$verminor.$verbuild.102

git archive --prefix=mozc-$version/ HEAD | xz > ../out/mozc-$version.tar.xz

popd
