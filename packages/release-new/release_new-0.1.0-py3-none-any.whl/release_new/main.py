#!/usr/bin/env python3
# coding: utf-8

import os
import subprocess
from argparse import ArgumentParser
from pathlib import Path
from distutils.core import run_setup
from redbaron import RedBaron


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--release-type", "-r", choices=["patch", "minor", "major"], default="patch"
    )

    args = parser.parse_args()
    root = Path(".")

    # assert there is a pkginfo and a setup.py
    pkginfo_path = root / "__pkginfo__.py"
    if not pkginfo_path.exists():
        try:
            pkginfo_path = next(root.glob("cubicweb*/__pkginfo__.py"))
        except StopIteration:
            raise ValueError("no pkginfo")

    setup_path = root / "setup.py"
    if not setup_path.exists():
        raise ValueError("no setup.py")

    # assert on public head, and clean environment
    id_last_public = subprocess.check_output(
        ["hg", "id", "-r", "last(public() and branch(default))", "--template", "{node}"]
    )
    current_id = subprocess.check_output(
        ["hg", "id", "-r", ".", "--template", "{node}"]
    )

    if current_id != id_last_public:
        raise ValueError(
            f"not on the last public head, go to {id_last_public.decode('utf-8')}"
        )

    debian_directory = root / "debian"
    has_debian_pkg = debian_directory.exists()

    if not has_debian_pkg:
        print("no debian directory found")

    # verify there is a debian directory
    #    dch must be installed
    #    DEBEMAIL and DEBEMAIl in os.environ
    if has_debian_pkg:
        try:
            subprocess.check_output(["which", "dch"])
        except subprocess.CalledProcessError:
            raise ValueError("no dch command found")

        if "DEBEMAIL" not in os.environ:
            raise ValueError("no DEBEMAIL in environment")
        if "DEBFULLNAME" not in os.environ:
            raise ValueError("no DEBFULLNAME in environment")

    # get current version in the setup.py -> compare with existing tags. If it

    setup_result = run_setup(setup_path, stop_after="init")
    current_version = setup_result.get_version()

    existing_tags = (
        subprocess.check_output(["hg", "tags", "--template", "{tags}\n"])
        .decode("utf-8")
        .split("\n")
    )

    if not any(current_version in tag for tag in existing_tags):
        raise ValueError(
            "cannot handle this situation right now. "
            f"Your current version ({current_version}) is not found in "
            f"the existing mercurial tags (last found {existing_tags[1]})"
        )

    # should we check the version against pypi ?

    # exist, warn and exit
    # ask for :
    #  - patch
    #  - minor
    #  - major

    print(f"Let's go for a {args.release_type} release")

    red = RedBaron(pkginfo_path.read_text())
    assignement = red.find("assign", target=lambda x: x.value == "numversion")
    assert assignement

    if args.release_type == "patch":
        assignement.value[2].value = str(int(assignement.value[2].value) + 1)

    elif args.release_type == "minor":
        assignement.value[2].value = "0"
        assignement.value[1].value = str(int(assignement.value[1].value) + 1)

    elif args.release_type == "major":
        assignement.value[2].value = "0"
        assignement.value[1].value = "0"
        assignement.value[0].value = str(int(assignement.value[0].value) + 1)

    else:
        raise Exception("unhandled situation")

    pkginfo_path.write_text(red.dumps())

    new_version = run_setup(setup_path, stop_after="init").get_version()

    if has_debian_pkg:
        subprocess.check_call(
            f"dch -v {new_version}-1 -D unstable 'New {args.release_type} release'",
            shell=True,
        )

    subprocess.check_call(
        f'hg commit -m "chore(pkg): new {args.release_type} release ({new_version})"',
        shell=True,
    )

    subprocess.check_call(f'hg tag "{new_version}"', shell=True)

    # emojis for Arthur
    print(
        f"🎉 Congratulation, we've made a new {args.release_type} release {new_version} \\o/ 🎇"
    )
    print()
    print("✨ 🍰 ✨")
    print()
    print("Now you need to hg push the new commits")
