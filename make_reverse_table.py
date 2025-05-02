#!/usr/bin/python3

import base64
import json
import os
import hashlib
import sys

#
# create a table in which a key is a hash of file in the registry
#

reverse_table = {}

def add_to_reverse_table(key: str, obj: dict):
    table_entry = reverse_table.get(key, [])
    table_entry.append(obj)
    reverse_table[key] = table_entry


def main():
    os.chdir("bazel-central-registry")

    # for each file in modules
    modules_dir = "modules"
    for root, _, files in os.walk(modules_dir):
        for file in files:
            # get sha256 hash of the file
            file_path = os.path.join(root, file)
            print(f"File: {file_path}", file=sys.stderr)
            with open(file_path, "rb") as f:
                # calculate sha256 hash of the file
                content = f.read()
                file_hash = hashlib.sha256(content).hexdigest()
                add_to_reverse_table(file_hash, {"url": os.path.join("https://bcr.bazel.build/", file_path)})

                if (file == "source.json"):
                    # parse the content as json
                    source = json.loads(content.decode("utf-8"))

                    # add hash value of source file
                    url = source.get("url")
                    if url is None:
                        continue
                        
                    integrity = source["integrity"]

                    algorithm = integrity.split("-")[0]
                    base64_hash = integrity.split("-")[1]
                    decoded_hash = base64.b64decode(base64_hash)
                    hex_string = decoded_hash.hex()
                    add_to_reverse_table(hex_string, {"url": url, "source.json": file_path, "algorithm": algorithm})


    with open("../reverse_table.json", "w") as f:
        json.dump(reverse_table, f, indent=4, sort_keys=True)


if __name__ == "__main__":
    main()