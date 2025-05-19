#!/bin/bash

export CC=gcc-10
export CXX=g++-10

pushd mozc

git clean -f
git checkout .

patch -p1 < ../patches/use-system-python-3.12.patch

pushd src

bazel8 build package \
    -c opt --config oss_linux \
    --explain=build.txt \
    --repository_cache=../../dependencies
#   --repository_disable_download
#   --registry=file:$(realpath ../bazel-central-registry) \
#   --ignore_dev_dependency

cp MODULE.bazel.lock ../../out/

popd
popd
