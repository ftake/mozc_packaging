#!/usr/bin/python3

import json
import os
import shutil

extra_modules = [
    # build-in modules of bazel 8.0.1
    {
        "name": "rules_java",
        "version": "8.6.1"
    },
    {
        "name": "zlib",
        "version": "1.3.1.bcr.3"
    },
    {
        "name": "platforms",
        "version": "0.0.10"
    },
    {
        "name": "bazel_features",
        "version": "1.21.0"
    }
]

def load_reverse_table(filename: str = "cache/reverse_table.json") -> dict:
    """
    Load the reverse table from a JSON file.
    :param filename: The name of the JSON file to load.
    :return: The loaded hash table as a dictionary.
    """
    try:
        with open(filename, "r") as f:
            hash_table = json.load(f)
        return hash_table
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file {filename}.")
        return {}

def main():
    reverse_table = load_reverse_table()

    root_dir = "dependencies/content_addressable/sha256"
    dest_dir = "bcr/"
    prefix = "https://bcr.bazel.build/"

    os.makedirs(dest_dir, exist_ok=True)

    for hash in os.listdir(root_dir):
        if hash in reverse_table:
            entry = reverse_table[hash]
        
            # copy into dest_dir to create copy of bazel central registry
            for file in entry:
                url = file["url"]
                if not url.startswith(prefix):
                    # sekip
                    continue
            
                path = os.path.join(dest_dir, url[len(prefix):])
                print(f"Copying {hash} to {path}")
                os.makedirs(os.path.dirname(path), exist_ok=True)
                shutil.copy(os.path.join(root_dir, hash, "file"), path, )
                shutil.rmtree(os.path.join(root_dir, hash))

    # copy extra modules
    for module in extra_modules:
        src = os.path.join("bazel-central-registry/modules", module["name"], module["version"])
        dest = os.path.join(dest_dir, "modules", module["name"], module["version"])
        print(f"Copying extra module {src} to {dest}")
        shutil.copytree(src, dest, dirs_exist_ok=True)

    # run tar to create bcr.tar.xz
    #  tar cJf ../out/bcr.tar.xz --owner=0 --group=0 bcr
    os.makedirs("out", exist_ok=True)
    shutil.make_archive("out/bcr", "xztar", base_dir=dest_dir, owner="root", group="root")

if __name__ == "__main__":
    main()