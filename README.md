# gitignore-generator

This utility creates .gitignore files from the terminal

Dependencies: `git`, `python`.

## Template Sources

- [github.com](https://github.com/github/gitignore.git)
- [gitignore.io](https://github.com/toptal/gitignore.git)

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

