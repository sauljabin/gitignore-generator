#!/usr/bin/python

import os

version = "0.1.0"

debug = True
script_path = os.path.dirname(__file__)

sources = {
    "github.com": "https://github.com/github/gitignore.git",
    "gitignore.io": "https://github.com/toptal/gitignore.git"
}


def exec_command(command, *parameters):
    to_exec = "{} {} {}".format(command, " ".join(parameters), "" if debug else "> /dev/null 2>&1")
    if debug:
        print(to_exec)
    return os.system(to_exec)


def check_git():
    if exec_command("git --version") != 0:
        raise Exception("Install git first")


def download_sources():
    for source, remote_path in sources.items():
        local_path = os.path.join(script_path, source)
        if exec_command("git -C", local_path, "status") != 0:
            exec_command("git clone", remote_path, local_path)
        else:
            exec_command("git -C", local_path, "pull")


def update_script():
    exec_command("git -C", script_path, "pull")


try:
    check_git()
    update_script()
    download_sources()
except Exception as e:
    print(e.message)
    exit(1)
