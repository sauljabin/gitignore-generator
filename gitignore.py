#!/usr/bin/python

import argparse
import os

version = "0.1.0"
script_path = os.path.dirname(__file__)

sources = {
    "gitignore.io": "https://github.com/toptal/gitignore.git",
    "github.com": "https://github.com/github/gitignore.git"
}

default_source = sources.keys()[0]


def exec_command(command, *parameters):
    to_exec = "{} {} {}".format(command, " ".join(parameters), "" if args.debug else "> /dev/null 2>&1")
    if args.debug:
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


def setup_args():
    parser = argparse.ArgumentParser(description="Generates .gitignore files from templates", prog='gitignore')

    parser.add_argument("-d", "--debug", help="print full output", action='store_true')
    parser.add_argument("-c", "--clean", help="clean sources", action='store_true')
    parser.add_argument("-a", "--append", help="append to existing .gitignore file", action='store_true')
    parser.add_argument("keys", help="IDEs, Languages or OSs, accepts multiple", type=str, nargs="+")
    parser.add_argument("-s", "--source",
                        help="select template source, default: " + default_source,
                        type=str, nargs="?", default=default_source, choices=sources.keys())
    parser.add_argument("-v", "--version", action='version', version="%(prog)s " + version)

    return parser.parse_args()


try:
    args = setup_args()
    check_git()
    update_script()
    download_sources()
except Exception as e:
    print(e.message)
    exit(1)
