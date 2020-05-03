# gitignore-generator

This utility creates .gitignore files from the terminal using community templates.

Dependencies: `git`, `python`.

## Template Sources

- [gitignore.io](https://github.com/toptal/gitignore.git)
- [github.com](https://github.com/github/gitignore.git)

## Install

Clone:
```shell script
$ git clone https://github.com/sauljabin/gitignore-generator.git ~/.gitignore-generator
```

Alias (It is recommended to make a backup of `~/.bashrc` and `~/.zshrc`):
```shell script
$ echo "alias gitignore='~/.gitignore-generator/gitignore.py'" >> ~/.bashrc
$ echo "alias gitignore='~/.gitignore-generator/gitignore.py'" >> ~/.zshrc
```

## Commands

```shell script
$ gitignore -h
usage: gitignore [-h] [-d] [-l] [-f] [-c] [-a]
                 [-s [{github.com,gitignore.io}]] [-v]
                 [keys [keys ...]]

Generates .gitignore files from templates

positional arguments:
  keys                  IDEs, Languages or OSs, accepts multiple

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           print full output
  -l, --list            print full template list
  -f, --find            search a template
  -c, --clean           clean sources
  -a, --append          append to existing .gitignore file
  -s [{github.com,gitignore.io}], --source [{github.com,gitignore.io}]
                        select template source, default: gitignore.io
  -v, --version         show program's version number and exit
```
