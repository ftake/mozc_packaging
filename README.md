mozc-packaging
================================================================================

## A quick tutorial

### (1) Checkouts submodules

```
git submodule init
git submodule update --recursive
```

### (2) Update submodules

```
cd mozc
git fetch
git checkout xxxxxx
cd ../fcitx-mozc
git fetch
git checkout yyyyyy
cd ../bazel-central-registry
git fetch
git checkout origin/main
```

### (3) Test build

```
./build.sh
```

### (4) Generate SBOM document of dependencies.tar

```
./make_reverse_table.py
./make_sbom_of_dependencies.py
```

If you get a message like below, you need to check license, version and downloadLocation of unknown packages and fill the missing fields packages.toml:

```
=== Unknown packages ===

[[packages]]
# https://github.com/bazelbuild/rules_shell/releases/download/v0.3.0/rules_shell-v0.3.0.tar.gz
name = "rules_shell-v0.3.0.tar.gz"
sha256sum = "d8cd4a3a91fc1dc68d4c7d6b655f09def109f7186437e3f50a9b60ab436a0c53"
downloadLocation = "https://github.com/bazelbuild/rules_shell/releases/download/v0.3.0/rules_shell-v0.3.0.tar.gz"
license = ""
version = ""

[[packages]]
# https://github.com/bazel-contrib/rules_python/releases/download/1.5.4/rules_python-1.5.4.tar.gz
name = "rules_python-1.5.4.tar.gz"
sha256sum = "13671d304cfe43350302213a60d93a5fc0b763b0a6de17397e3e239253b61b73"
downloadLocation = "https://github.com/bazel-contrib/rules_python/releases/download/1.5.4/rules_python-1.5.4.tar.gz"
license = ""
version = ""
```

### (5) Create archive files for packaging

```
./make_bcr.py
./make_dependencies.sh
./make_archive.sh
./make_fcitx-mozc.sh
```