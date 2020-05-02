#!/usr/bin/python

import os

version = "0.1.0"

commands = {
    "git_version": "git --version"
}

sources = {
    "github.com": "https://github.com/github/gitignore.git",
    "gitignore.io": "https://github.com/toptal/gitignore.git"
}


def exec_command(command, output=False):
    return os.system("{}{}".format(commands[command], "" if output else " > /dev/null 2>&1"))


def check_git():
    if exec_command("git_version") != 0:
        raise Exception("Install git first")


def download_sources():
    return


try:
    check_git()
except Exception as e:
    print(e.message)
