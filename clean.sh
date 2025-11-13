#!/bin/bash

rm -rf vendor
rm -rf dependencies
rm -rf bcr
mkdir dependencies

pushd mozc/src
bazel8 clean --expunge
popd
