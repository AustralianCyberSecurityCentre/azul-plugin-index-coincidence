# Azul Plugin Index Coincidence

This plugin uses the index-coincidence package to compute the index of
coincidence and search for widths which improve the index of coincidence.

The Index of Coincidence (IC) is a statistical tool used in cryptography to analyze the frequency distribution of
letters in a ciphertext.
It helps determine whether a cipher is monoalphabetic (e.g Caesar cipher) or polyalphabetic (e.g Vigenère cipher).

It can be useful for detecting the type of cipher and estimating the encryption key length (width).

For the application of this see:

    https://en.wikipedia.org/wiki/Index_of_coincidence#Application

## Development Installation

To install azul-plugin-index-coincidence for development run the command
(from the root directory of this project):

```bash
pip install -e .
```

## Usage

Usage on local files:

```bash
$ azul-index-coincidence test_039.enc
Output features:
    index_of_coincidence_width: 0.10374224863997697 - 39
        index_of_coincidence: 0.0039474089988589525
```

The 'index_of_coincidence' feature is the result of the file as it is. The
'index_of_coincidence_width' feature shows that the index of coincidence
increases significantly (from 0.0039 -> 0.1037) with a width of 39.

Check `azul-plugin-index-coincidence --help` for advanced usage.

## Python Package management

This python package is managed using a `pyproject.toml` file.

Standardisation of installing and testing the python package is handled through tox.
Tox commands include:

```bash
# Run all standard tox actions
tox
# Run linting only
tox -e style
# Run tests only
tox -e test
```

## Developer note

This package uses setuptools rather than hatchling due to it's need for a C extension module.

## Dependency management

Dependencies are managed in the pyproject.toml and debian.txt file.

Version pinning is achieved using the `uv.lock` file.
Because the `uv.lock` file is configured to use a private UV registry, external developers using UV will need to delete the existing `uv.lock` file and update the project configuration to point to the publicly available PyPI registry instead.

To add new dependencies it's recommended to use uv with the command `uv add <new-package>`
    or for a dev package `uv add --dev <new-dev-package>`

The tool used for linting and managing styling is `ruff` and it is configured via `pyproject.toml`

The debian.txt file manages the debian dependencies that need to be installed on development systems and docker images.

Sometimes the debian.txt file is insufficient and in this case the Dockerfile may need to be modified directly to
install complex dependencies.