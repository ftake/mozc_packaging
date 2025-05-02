#!/bin/bash

export CC=gcc-10
export CXX=g++-10

pushd mozc/src

bazel8 build package \
    -c opt --config oss_linux \
    --explain=build.txt \
    --repository_cache=../../dependencies
#   --repository_disable_download
#   --registry=file:$(realpath ../bazel-central-registry) \
#   --ignore_dev_dependency

popd
