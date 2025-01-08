# Setup

## First clone

This repo contains submodules. If it was not cloned with `git clone --recurse-submodules`,
use `git submodule update --init --recursive` to initialize the submodules.

## Virtual environment

This repo uses [uv](https://github.com/astral-sh/uv) to manage python dependencies.
To run commands in the virtual environment, prefix them with `uv run`.

## Helpers

The `tasks.py` file should contain all the needed commands to run and manage this Pelican project.
Use `uv run invoke --list` to list them and `uv run invoke <command>` to run them.

The `tasks.py` file was first created by the `pelican-quickstart` command, but has since been modified.
See here for details on the initial file: https://docs.getpelican.com/en/stable/publish.html#automation

# Deployment

Deployment is done using a GitHub Actions workflow.
