#!/usr/bin/env python3

# This will try to import setuptools. If not here, it fails with a message
import os
import codecs
try:
    from setuptools import setup
except ImportError:
    raise ImportError(
        "This module could not be installed, probably because"
        " setuptools is not installed on this computer."
        "\nInstall ez_setup ([sudo] pip install ez_setup) and try again."
    )


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('APPLICATION_VERSION'):
            delimiter = '"' if '"' in line else "'"
            return line.split(delimiter)[1]
    else:
        raise RuntimeError("Unable to find version string.")


pre_version = get_version("glxviewer/__init__.py")

if os.environ.get('CI_COMMIT_TAG'):
    version = os.environ['CI_COMMIT_TAG']
else:
    if os.environ.get('CI_JOB_ID'):
        version = os.environ['CI_JOB_ID']
    else:
        version = pre_version

with open('README.rst') as f:
    long_description = f.read()

# setup(tests_require=["green"], setup_requires=["pbr"], pbr=True)
setup(
    name='galaxie-viewer',
    version=version,
    description='Galaxie Viewer is a Python toolkit it permit to display text over templates, like a micro STDOUT '
                'logging.',
    author='Tuxa',
    author_email='tuxa@rtnp.org',
    license=' GPLv3+',
    packages=['glxviewer'],
    url=' https://gitlab.com/Tuuux/galaxie-viewer',
    download_url='https://pypi.org/project/galaxie-viewer',
    project_urls={
        'Read the Docs': 'https://glxviewer.readthedocs.io',
        'GitLab': 'https://gitlab.com/Tuuux/galaxie-viewer',
    },
    zip_safe=False,
    long_description=long_description,
    long_description_content_type="text/x-rst; charset=UTF-8",
    keywords="Galaxie utility text format template",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
    ],
    setup_requires=["green", "wheel"],
    tests_require=["wheel"]
)
