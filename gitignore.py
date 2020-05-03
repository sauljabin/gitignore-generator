#!/usr/bin/python

# Source https://github.com/sauljabin/gitignore-generator

import argparse
import os
import sys

version = "0.1.0"
script_path = os.path.dirname(__file__)

sources = {
    "gitignore.io": "https://github.com/toptal/gitignore.git",
    "github.com": "https://github.com/github/gitignore.git"
}

default_source = sources.keys()[0]


def get_path(*to_join):
    return os.path.join(script_path, *to_join)


def get_command_output(command, *parameters):
    to_exec = "{} {}".format(command, " ".join(parameters))
    return os.popen(to_exec).read().strip()


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
        local_path = get_path(script_path, source)
        if exec_command("git -C", local_path, "status") != 0:
            exec_command("git clone", remote_path, local_path)
        else:
            exec_command("git -C", local_path, "pull")


def update_script():
    current_hash = get_command_output("git -C", script_path, "rev-parse HEAD")
    exec_command("git -C", script_path, "pull")
    new_hash = get_command_output("git -C", script_path, "rev-parse HEAD")
    if current_hash != new_hash:
        os.execv(__file__, sys.argv)


def process_clean():
    if args.clean:
        for source in sources:
            local_path = get_path(script_path, source)
            exec_command("rm -rf", local_path)


def process_gitignore():
    files = []
    for r, d, f in os.walk(get_path(args.source)):
        for source_file in f:
            for key in args.keys:
                gitignore_file = key + ".gitignore"
                if gitignore_file.lower() in source_file.lower():
                    files.append(os.path.join(r, source_file))

    if len(files) <= 0:
        print ("Templates not found")
    else:
        if args.debug:
            print ("Files to save:", files)
        save_gitignore(files)


def save_gitignore(files):
    if args.append:
        gitignore = open(".gitignore", "a")
    else:
        gitignore = open(".gitignore", "w")
    for f in files:
        head, tail = os.path.split(f)
        gitignore.write("### {}: {} ###\n\n".format(args.source, tail))
        file_from_source = open(f, "r")
        gitignore.writelines(file_from_source.readlines())
        gitignore.write("\n")
        file_from_source.close()
    gitignore.close()


def setup_args():
    parser = argparse.ArgumentParser(description="Generates .gitignore files from templates", prog="gitignore")

    parser.add_argument("-d", "--debug", help="print full output", action="store_true")
    parser.add_argument("-c", "--clean", help="clean sources", action="store_true")
    parser.add_argument("-a", "--append", help="append to existing .gitignore file", action="store_true")
    parser.add_argument("keys", help="IDEs, Languages or OSs, accepts multiple", type=str, nargs="+")
    parser.add_argument("-s", "--source",
                        help="select template source, default: " + default_source,
                        type=str, nargs="?", default=default_source, choices=sources.keys())
    parser.add_argument("-v", "--version", action="version", version="%(prog)s " + version)

    return parser.parse_args()


try:
    args = setup_args()
    check_git()
    update_script()
    process_clean()
    download_sources()
    process_gitignore()
except Exception as e:
    print(e.message)
    exit(1)
