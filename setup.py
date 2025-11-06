#!/usr/bin/env python3
"""Setup script."""
import os

from setuptools import Extension, setup


def open_file(fname):
    """Open and return a file-like object for the relative filename."""
    return open(os.path.join(os.path.dirname(__file__), fname))


entropy_module = Extension(
    "_entropy",
    sources=["azul_plugin_index_coincidence/entropy/entropy.c"],
    libraries=["m"],
)

setup(
    name="azul-plugin-index-coincidence",
    description="Find index-of-coincidence widths to find obfuscation key widths and data repetition.",
    author="Azul",
    author_email="azul@asd.gov.au",
    url="https://www.asd.gov.au/",
    packages=["azul_plugin_index_coincidence"],
    include_package_data=True,
    python_requires=">=3.12",
    classifiers=[],
    entry_points={
        "console_scripts": [
            "azul-plugin-index-coincidence = azul_plugin_index_coincidence.main:main",
            "index-coincidence = azul_plugin_index_coincidence.index_coincidence.main:main",
        ]
    },
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    install_requires=[r.strip() for r in open_file("requirements.txt") if not r.startswith("#")],
    ext_modules=[entropy_module],
)
