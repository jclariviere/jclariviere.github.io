import datetime
import os
import shlex
import shutil

from invoke import task
from invoke.main import program
from pelican import main as pelican_main
from pelican.settings import DEFAULT_CONFIG, get_settings_from_file

OPEN_BROWSER_ON_SERVE = True
SETTINGS_FILE_BASE = "pelicanconf.py"
SETTINGS = {}
SETTINGS.update(DEFAULT_CONFIG)
LOCAL_SETTINGS = get_settings_from_file(SETTINGS_FILE_BASE)
SETTINGS.update(LOCAL_SETTINGS)

CONFIG = {
    "settings_base": SETTINGS_FILE_BASE,
    "settings_publish": "publishconf.py",
    # Output path. Can be absolute or relative to tasks.py. Default: 'output'
    "deploy_path": SETTINGS["OUTPUT_PATH"],
    # Github Pages configuration
    "github_pages_branch": "master",
    "commit_message": f"'Publish site on {datetime.date.today().isoformat()}'",
    # Host and port for `serve`
    "host": "localhost",
    "port": 8000,
}


@task
def clean(c):
    """Remove generated files"""
    if os.path.isdir(CONFIG["deploy_path"]):
        shutil.rmtree(CONFIG["deploy_path"])
        os.makedirs(CONFIG["deploy_path"])


@task
def build(c):
    """Build local version of site"""
    pelican_run("-s {settings_base}".format(**CONFIG))


@task
def rebuild(c):
    """`build` with the delete switch"""
    pelican_run("-d -s {settings_base}".format(**CONFIG))


@task
def regenerate(c):
    """Automatically regenerate site upon file modification"""
    pelican_run("-r -s {settings_base}".format(**CONFIG))


@task
def serve(c):
    """Serve site at http://$HOST:$PORT/ (default is localhost:8000)"""
    pelican_run("-l -s {settings_base}".format(**CONFIG))


@task
def dev_server(c):
    """`serve` and `regenerate` together"""
    pelican_run("-lr -s {settings_base}".format(**CONFIG))


@task
def live_reload(c):
    """Like `dev-server`, but also automatically reload browser tab upon file modification."""
    from livereload import Server

    def cached_build():
        cmd = "-s {settings_base} -e CACHE_CONTENT=true LOAD_CONTENT_CACHE=true"
        pelican_run(cmd.format(**CONFIG))

    cached_build()
    server = Server()
    theme_path = SETTINGS["THEME"]
    watched_globs = [
        CONFIG["settings_base"],
        f"{theme_path}/templates/**/*.html",
    ]

    content_file_extensions = [".md", ".rst"]
    for extension in content_file_extensions:
        content_glob = "{}/**/*{}".format(SETTINGS["PATH"], extension)
        watched_globs.append(content_glob)

    static_file_extensions = [".css", ".js"]
    for extension in static_file_extensions:
        static_file_glob = f"{theme_path}/static/**/*{extension}"
        watched_globs.append(static_file_glob)

    for glob in watched_globs:
        server.watch(glob, cached_build)

    if OPEN_BROWSER_ON_SERVE:
        # Open site in default browser
        import webbrowser

        webbrowser.open("http://{host}:{port}".format(**CONFIG))

    server.serve(host=CONFIG["host"], port=CONFIG["port"], root=CONFIG["deploy_path"])


@task
def build_prod(c):
    """Build production version of site"""
    pelican_run("-s {settings_publish}".format(**CONFIG))


@task
def gh_pages(c):
    """`build-prod` then publish to GitHub Pages"""
    build_prod(c)
    c.run("cp CNAME {deploy_path}/CNAME".format(**CONFIG))
    c.run(
        "ghp-import --branch {github_pages_branch} "
        "--message {commit_message} "
        "--no-jekyll "
        "{deploy_path} --push".format(**CONFIG)
    )


@task
def lint(c):
    """Run the linter on python files"""
    c.run("ruff check --fix --show-fixes")


@task
def format(c):
    """Run the formatter on python files"""
    c.run("ruff format")


def pelican_run(cmd):
    cmd += " " + program.core.remainder  # allows to pass-through args to pelican
    pelican_main(shlex.split(cmd))
