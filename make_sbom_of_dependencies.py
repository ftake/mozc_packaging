#!/usr/bin/env python3

import json
import os
import tomllib

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

def load_package_db(filename: str = "packages.toml") -> dict:
    """
    Load the package database from a TOML file.
    :param filename: The name of the TOML file to load.
    :return: The loaded package database as a dictionary.
    """
    try:
        with open(filename, "rb") as f:
            package_db = tomllib.load(f)
        return package_db
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return {}
    except tomllib.TOMLDecodeError:
        print(f"Error decoding TOML from file {filename}.")
        return {}

def create_package_db_index(package_db: dict) -> dict:
    """
    Create an index of the package database for quick lookup.
    :param package_db: The package database as a dictionary.
    :return: An index of the package database.
    """
    package_db_index = {}
    for package in package_db["packages"]:
        package_db_index[package["sha256sum"]] = package
    
    return package_db_index

def is_bazel_central_registry(urls: list):
    for url in urls:
        if url.startswith("https://bcr.bazel.build/"):
            return True
    return False


def main():
    reverse_table = load_reverse_table()
    unknown_packages = []

    if not reverse_table:
        print("Error: No hash table loaded.")
        exit(1)
    package_db = load_package_db()
    if not package_db:
        print("Warning: No package database loaded.")
        # continue with empty package_db
        package_db = {
            "packages": []
        }

    package_db_index = create_package_db_index(package_db)

    root_dir = "dependencies/content_addressable/sha256"

    bazel_central_registry = {
        "name": "bazel-central-registry",
        "purl": "pkg:github/bazelbuild/bazel-central-registry",
        "license": "Apache-2.0",
        "files": []
    }

    sbom = {
        "packages": [
            bazel_central_registry
        ]
    }

    for hash in os.listdir(root_dir):
        # in the package DB
        if hash in package_db_index:
            p = package_db_index[hash]
            package = {
                "name": p["name"],
                "license": p["license"],
                "files": [{
                    "path": f"content_addressable/sha256/{hash}/file",
                    "downloadLocations": [p["downloadLocation"]]
                }]
            }
            sbom["packages"].append(package)

        elif hash in reverse_table:
            entry = reverse_table[hash]
            urls = sorted(list({e["url"] for e in entry if "url" in e}))

            if is_bazel_central_registry(urls):
                bazel_central_registry["files"].append({
                    "path": f"content_addressable/sha256/{hash}/file",
                    "downloadLocations": urls
                })
            
            else:
                # No data in the package database but found in Bazel Central Registry
                package = {
                    "name": "noassertion",
                    "license": "noassertion",
                    "files": [{
                        "path": f"content_addressable/sha256/{hash}/file",
                        "downloadLocations": urls
                    }]
                }
                sbom["packages"].append(package)
                packagename_candidate = urls[-1].split("/")[-1] if urls else urls[-1]
                unknown_packages.append({
                    "name": packagename_candidate,
                    "sha256sum": hash,
                    "urls": urls
                })
        else:
            # maybe a file by http_file / http_archive
            package = {
                "name": "noassertion",
                "license": "noassertion",
                "files": [{
                    "path": f"content_addressable/sha256/{hash}/file",
                }]
            }
            sbom["packages"].append(package)
            unknown_packages.append({
                "name": "",
                "sha256sum": hash,
                "urls": []
            })
    
    with open("dependencies/sbom.json", "w") as f:
        json.dump(sbom, f, indent=4)

    if unknown_packages:
        print("=== Unknown packages ===")
        for package in unknown_packages:
            print()
            print("[[packages]]")
            urls = package["urls"]
            for url in urls:
                print(f"# {url}")
            print(f'name = "{package['name']}"')
            print(f'sha256sum = "{package["sha256sum"]}"')
            if len(urls) == 1:
                print(f"downloadLocation = \"{urls[0]}\"")
            print(f'license = ""')
            print('version = ""')


if __name__ == "__main__":
    main()