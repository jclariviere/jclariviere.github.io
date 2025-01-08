import shlex

from invoke import task
from invoke.main import program
from pelican import main as pelican_main
from pelican.settings import DEFAULT_CONFIG, get_settings_from_file

OPEN_BROWSER_ON_SERVE = True
SETTINGS_FILE = "pelicanconf.py"

SETTINGS = {}
SETTINGS.update(DEFAULT_CONFIG)
LOCAL_SETTINGS = get_settings_from_file(SETTINGS_FILE)
SETTINGS.update(LOCAL_SETTINGS)


@task
def live_reload(c, port=8000, host="127.0.0.1", output_path=SETTINGS["OUTPUT_PATH"]):
    """Runs a dev server that automatically reloads browser tab on file change"""
    import livereload

    def cached_build():
        pelican_run(f"-s {SETTINGS_FILE} -e CACHE_CONTENT=true LOAD_CONTENT_CACHE=true")

    cached_build()
    server = livereload.Server()
    theme_path = SETTINGS["THEME"]
    watched_globs = [
        SETTINGS_FILE,
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

        webbrowser.open(f"http://{host}:{port}")

    server.serve(host=host, port=port, root=output_path)


def pelican_run(cmd):
    cmd += " " + program.core.remainder  # allows to pass-through args to pelican
    pelican_main(shlex.split(cmd))
