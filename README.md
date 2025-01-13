# jclariviere.github.io

Source code for generating https://jclariviere.com

## Setup

Most of the tooling in this repo is very overkill for such a simple blog.
It has served as a testing and learning ground for many tools, including
`just`, `uv`, `invoke` and GitHub Actions.

### First clone

This repo contains submodules. If it was not cloned with `git clone --recurse-submodules`,
use `git submodule update --init --recursive` to initialize the submodules.

### Dependencies

Here are the dependencies that need to be installed to work with this project:

- [uv](https://github.com/astral-sh/uv) to manage python dependencies
- [just](https://github.com/casey/just) as a command runner

## Available commands

The `justfile` should contain all the needed commands to run and manage this Pelican project.
To list them, simply run `just` without arguments.

A notable exception is managing python dependencies, since I didn't want to create a wrapper for the already excellent and well-documented `uv` command line.
For this, use the `uv add/remove` commands.

### tasks.py

The `tasks.py` file was first created by the `pelican-quickstart` command.
See here for details on the initial `Makefile` and `tasks.py` files: https://docs.getpelican.com/en/stable/publish.html#automation

Most of the commands in these files have been merged and moved to the `justfile`, but python-heavy tasks such as `live-reload` have been kept in `tasks.py`.
The `justfile` will contain entries for these commands, but they can still be listed manually with `uv run invoke --list` and run with `uv run invoke <command>`.

## Deployment

The site is deployed to GitHub Pages using a GitHub Actions workflow.
