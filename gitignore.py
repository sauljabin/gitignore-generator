#!/usr/bin/python

# Source https://github.com/sauljabin/gitignore-generator

import argparse
import os
import re
import sys

version = "0.3.1"
script_path = os.path.dirname(__file__)

sources = {
    "gitignore.io": "https://github.com/toptal/gitignore.git",
    "github.com": "https://github.com/github/gitignore.git",
}

default_source = sources.keys()[1]


def join_to_script_path(*to_join):
    return os.path.join(script_path, *to_join)


def get_command_output(command, *parameters):
    to_exec = "{} {}".format(command, " ".join(parameters))
    return os.popen(to_exec).read().strip()


def exec_command(command, *parameters):
    to_exec = "{} {} {}".format(
        command, " ".join(parameters), "" if args.debug else "> /dev/null 2>&1"
    )

    if args.debug:
        print(to_exec)

    return os.system(to_exec)


def check_git():
    if exec_command("git --version"):
        raise Exception("Install git first")


def download_sources():
    for source, remote_path in sources.items():

        local_path = join_to_script_path(script_path, source)

        if exec_command("git -C", local_path, "status"):
            exec_command("git clone", remote_path, local_path)
        else:
            exec_command("git -C", local_path, "pull")


def get_script_commit():
    return get_command_output("git -C", script_path, "rev-parse HEAD")


def update_script():
    current_hash = get_script_commit()
    exec_command("git -C", script_path, "pull")
    new_hash = get_script_commit()

    if current_hash != new_hash:
        os.execv(__file__, sys.argv)


def process_clean():
    if not args.clean:
        return

    for source in sources:
        local_path = join_to_script_path(script_path, source)
        exec_command("rm -rf", local_path)


def process_gitignore_command():
    verify_keys()

    keys = [re.escape(key) for key in args.keys]
    templates = find_templates("({})\\.gitignore".format("|".join(keys)))
    save_gitignore(templates)
    exit(0)


def print_templates_command():
    if not args.read:
        return

    verify_keys()

    keys = [re.escape(key) for key in args.keys]
    templates = find_templates("({})\\.gitignore".format("|".join(keys)))
    print_templates(templates, True)
    exit(0)


def find_templates_command():
    if not args.find:
        return

    verify_keys()

    keys = [re.escape(key) for key in args.keys]
    templates = find_templates(".*({}).*gitignore".format("|".join(keys)))
    print_templates(templates)
    exit(0)


def print_template_list_command():
    if not args.list:
        return

    print("Source: {}".format(args.source))
    templates = find_templates(".+\\.gitignore")
    print_templates(templates)
    exit(0)


def verify_keys():
    if not args.keys:
        args_parser.print_usage()
        exit(1)


def save_gitignore(templetes):
    gitignore = open(".gitignore", "a" if args.append else "w")

    for template in templetes:
        path, template_name = os.path.split(template)
        gitignore.write("##### {}: {} #####\n\n".format(args.source, template_name))
        template_file = open(template, "r")
        gitignore.writelines(template_file.readlines())
        gitignore.write("\n")
        template_file.close()

    gitignore.close()


def print_templates(templates, full_file=False):
    for template in templates:
        path, template_name = os.path.split(template)
        print(template_name)
        if full_file:
            template_file = open(template, "r")
            print(template_file.read())
    print("Total: {}".format(len(templates)))


def find_templates(pattern):
    filtered_templates = []
    for root, dirs, files in os.walk(join_to_script_path(args.source)):
        for template in files:
            if re.match(pattern.lower(), template.lower()):
                filtered_templates.append(os.path.join(root, template))

    if args.debug:
        print("Templates found: {}".format(filtered_templates))

    if not filtered_templates:
        raise Exception("Templates not found")

    return filtered_templates


def setup_args():
    parser = argparse.ArgumentParser(
        description="Generates .gitignore files from templates", prog="gitignore"
    )

    parser.add_argument("-d", "--debug", help="print full output", action="store_true")

    parser.add_argument(
        "-r", "--read", help="print the found template completely", action="store_true"
    )

    parser.add_argument(
        "-l", "--list", help="print full template list", action="store_true"
    )

    parser.add_argument("-f", "--find", help="search a template", action="store_true")

    parser.add_argument(
        "-c", "--clean", help="delete sources repositories", action="store_true"
    )

    parser.add_argument(
        "-a", "--append", help="append to existing .gitignore file", action="store_true"
    )

    parser.add_argument(
        "keys", help="IDEs, Languages or OSs, accepts multiple", type=str, nargs="*"
    )

    parser.add_argument(
        "-s",
        "--source",
        help="select template source, default: " + default_source,
        type=str,
        nargs="?",
        default=default_source,
        choices=sources.keys(),
    )

    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s " + version
    )

    return parser, parser.parse_args()


try:
    args_parser, args = setup_args()
    check_git()
    update_script()
    process_clean()
    download_sources()
    print_template_list_command()
    print_templates_command()
    find_templates_command()
    process_gitignore_command()
except Exception as e:
    print(e.message)
    exit(1)
