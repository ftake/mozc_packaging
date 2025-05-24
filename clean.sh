#!/bin/bash

rm -rf dependencies
mkdir dependencies

pushd mozc/src
bazel8 clean --expunge
popd
