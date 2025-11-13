#!/bin/bash

export CC=gcc-15
export CXX=g++-15

pushd mozc

git clean -df
git checkout .

patch -p1 < ../patches/use-system-python.patch

pushd src

bazel8 build package \
    -c opt --config oss_linux \
    --explain=build.txt \
    --repository_cache=../../dependencies \
    --registry=file:$(realpath ../../bazel-central-registry)


popd
popd
