# Setup

## First clone

This repo contains submodules. If it was not cloned with `git clone --recurse-submodules`,
use `git submodule update --init --recursive` to initialize the submodules.

# Helpers

Some helper commands are available in the `Makefile` and `tasks.py` files.
Use `make` or `invoke --list` to list them.
See here for more details: https://docs.getpelican.com/en/stable/publish.html#automation

This project uses [uv](https://github.com/astral-sh/uv) to manage python dependencies.
To run commands in the virtual environment, prefix them with `uv run` (`uv run invoke` or `uv run make`)
Technically `make` doesn't need to run in a virtual env, but most commands in the `Makefile` use python packages.
