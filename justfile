output_dir := env_var_or_default("OUTPUT_DIR", "output/")

settings_file := "pelicanconf.py"
settings_file_prod := "publishconf.py"

# List available commands
_default:
    just --list --unsorted

# Remove generated files
clean:
    rm -rf "{{ output_dir }}"

# Build local version of site
build:
    uv run pelican \
        --settings "{{ settings_file }}" \
        --output "{{ output_dir }}"

# Serve site at http://$HOST:$PORT
serve PORT="8000" HOST="127.0.0.1":
    uv run pelican \
        --listen \
        --port "{{ PORT }}" \
        --bind "{{ HOST }}" \
        --settings "{{ settings_file }}" \
        --output "{{ output_dir }}"

# `serve` + autoreload server on file change
dev-server PORT="8000" HOST="127.0.0.1":
    uv run pelican \
        --listen \
        --autoreload \
        --port "{{ PORT }}" \
        --bind "{{ HOST }}" \
        --settings "{{ settings_file }}" \
        --output "{{ output_dir }}"

# `dev-server` + autoreload browser tab on file change
live-reload PORT="8000" HOST="127.0.0.1":
    uv run invoke live-reload \
        --port="{{ PORT }}" \
        --host="{{ HOST }}" \
        --output-path="{{ output_dir }}"

# Build production version of site
build-prod:
    uv run pelican \
        --settings "{{ settings_file_prod }}" \
        --output "{{ output_dir }}"

# Run the linter on python files
[group("python")]
lint:
    uv run ruff check --fix --show-fixes

# Run the formatter on python files
[group("python")]
format:
    uv run ruff format
