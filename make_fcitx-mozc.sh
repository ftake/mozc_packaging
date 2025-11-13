#!/bin/bash -e

pushd mozc

mozc_rev=`git rev-parse HEAD`

popd

pushd fcitx-mozc

# check if fcitx-mozc is synced with mozc by comparing src/data/version/mozc_version_template.bzl
if ! diff -q ../mozc/src/data/version/mozc_version_template.bzl src/data/version/mozc_version_template.bzl > /dev/null; then
    echo "fcitx-mozc is not synced with mozc"
    exit 1
fi

vermajor=`sed -n -e "s/MAJOR = \(.*\)/\1/p" src/data/version/mozc_version_template.bzl`
verminor=`sed -n -e "s/MINOR = \(.*\)/\1/p" src/data/version/mozc_version_template.bzl`
verbuild=`sed -n -e "s/BUILD_OSS = \(.*\)/\1/p" src/data/version/mozc_version_template.bzl`
# REVISION is always 102 for Linux
version=$vermajor.$verminor.$verbuild.102

git restore .
git archive --format=tar HEAD \
    src/unix/fcitx src/unix/fcitx5 src/BUILD.fcitx.bazel | \
    xz > ../out/fcitx-mozc-`git rev-parse --short=8 HEAD`.tar.xz

git diff $mozc_rev -- src/MODULE.bazel src/session/BUILD.bazel > ../out/fcitx-mozc-bazel-build.patch

echo $version

popd