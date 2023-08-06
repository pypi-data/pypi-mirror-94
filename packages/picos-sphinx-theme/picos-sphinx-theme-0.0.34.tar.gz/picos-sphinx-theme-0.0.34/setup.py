# -----------------------------------------------------------------------------
# Copyright 2020 Faculty Science Limited
# Copyright 2021 Maximilian Stahlberg
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# This file was obtained from Faculty Science Limited under the Apache License,
# Version 2.0, and has been modified by PICOS Developers.
# -----------------------------------------------------------------------------

"""PICOS Sphinx Theme installation script."""

from setuptools import setup


def forbidden_version_scheme(version):
    """Just append the commit distance to the tag version."""
    return "{}.{}".format(
        version.tag, version.distance if version.distance else 0
    )


setup(
    name="picos-sphinx-theme",
    use_scm_version={
        "version_scheme": forbidden_version_scheme,
        "local_scheme": "no-local-version",
    },
    description="A Sphinx theme for the PICOS documentation.",
    long_description=open("README.rst").read(),
    long_description_content_type="text/x-rst",
    author="PICOS Developers",
    author_email="incoming+picos-api/picos@incoming.gitlab.com",
    license="Apache License 2.0",
    classifiers=[
        "Framework :: Sphinx :: Theme",
        "Topic :: Documentation :: Sphinx",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Example": "https://picos-api.gitlab.io/picos/",
        "Source": "https://gitlab.com/picos-api/picos-sphinx-theme",
    },
    packages=["picos_sphinx_theme"],
    setup_requires=["setuptools_scm"],
    install_requires=[
        "sphinx-rtd-theme==0.4.3",
        "pallets-sphinx-themes==1.2.3",  # For jinja pygments style.
    ],
    package_data={
        "picos_sphinx_theme": [
            "theme.conf",
            "*.html",
            "static/css/*.css",
        ]
    },
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "sphinx.html_themes": ["picos = picos_sphinx_theme"],
    },
)
