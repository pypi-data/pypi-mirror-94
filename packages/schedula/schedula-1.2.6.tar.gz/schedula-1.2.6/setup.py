#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright 2015-2021, Vincenzo Arcidiacono;
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl

import io
import os
import collections
import os.path as osp

name = 'schedula'
mydir = osp.dirname(__file__)


# Version-trick to have version-info in a single place,
# taken from: http://stackoverflow.com/questions/2058802/how-can-i-get-the-
# version-defined-in-setup-py-setuptools-in-my-package
##
def read_project_version():
    fglobals = {}
    with io.open(osp.join(mydir, name, '_version.py'), encoding='UTF-8') as fd:
        exec(fd.read(), fglobals)  # To read __version__
    return fglobals['__version__']


# noinspection PyPackageRequirements
def get_long_description(cleanup=True):
    from sphinx.application import Sphinx
    from sphinx.util.osutil import abspath
    import tempfile
    import shutil
    from doc.conf import extensions
    from sphinxcontrib.writers.rst import RstTranslator
    from sphinx.ext.graphviz import text_visit_graphviz
    RstTranslator.visit_dsp = text_visit_graphviz
    outdir = tempfile.mkdtemp(prefix='setup-', dir='.')
    exclude_patterns = os.listdir(mydir or '.')
    exclude_patterns.remove('pypi.rst')

    # noinspection PyTypeChecker
    app = Sphinx(abspath(mydir), osp.join(mydir, 'doc/'), outdir,
                 outdir + '/.doctree', 'rst',
                 confoverrides={
                     'exclude_patterns': exclude_patterns,
                     'master_doc': 'pypi',
                     'dispatchers_out_dir': abspath(outdir + '/_dispatchers'),
                     'extensions': extensions + ['sphinxcontrib.restbuilder']
                 }, status=None, warning=None)

    app.build(filenames=[osp.join(app.srcdir, 'pypi.rst')])

    with open(outdir + '/pypi.rst') as file:
        res = file.read()

    if cleanup:
        shutil.rmtree(outdir)
    return res


proj_ver = read_project_version()
url = 'https://github.com/vinci1it2000/%s' % name
download_url = '%s/tarball/v%s' % (url, proj_ver)
project_urls = collections.OrderedDict((
    ('Documentation', 'http://%s.readthedocs.io' % name),
    ('Issue tracker', '%s/issues' % url),
))

if __name__ == '__main__':
    import functools
    from setuptools import setup, find_packages

    long_description = ''
    if os.environ.get('ENABLE_SETUP_LONG_DESCRIPTION') == 'TRUE':
        try:
            long_description = get_long_description()
            print('LONG DESCRIPTION ENABLED!')
        except Exception as ex:
            print('LONG DESCRIPTION ERROR:\n %r', ex)

    extras = {
        'io': ['dill!=0.2.7'],
        'web': ['requests', 'regex', 'flask'],
        'parallel': ['multiprocess'],
        'plot': [
            'requests', 'graphviz', 'regex', 'flask', 'Pygments', 'jinja2',
            'docutils'
        ]
    }
    extras['sphinx'] = ['sphinx'] + extras['plot']
    # noinspection PyTypeChecker
    extras['all'] = sorted(functools.reduce(set.union, extras.values(), set()))
    extras['dev'] = extras['all'] + [
        'wheel', 'sphinx', 'gitchangelog', 'mako', 'sphinx_rtd_theme',
        'setuptools>=36.0.1', 'sphinxcontrib-restbuilder', 'nose', 'coveralls',
        'requests', 'readthedocs-sphinx-ext'
    ]

    setup(
        name=name,
        version=proj_ver,
        packages=find_packages(exclude=[
            'doc', 'doc.*',
            'tests', 'tests.*',
            'examples', 'examples.*',
            'micropython', 'micropython.*',
            'requirements', 'binder', 'bin'
        ]),
        url=url,
        project_urls=project_urls,
        download_url=download_url,
        license='EUPL 1.1+',
        author='Vincenzo Arcidiacono',
        author_email='vinci1it2000@gmail.com',
        description='Produce a plan that dispatches calls based on a graph of '
                    'functions, satisfying data dependencies.',
        long_description=long_description,
        keywords=[
            "flow-based programming", "dataflow", "parallel", "asynchronous",
            "async", "scheduling", "dispatch", "functional programming",
            "dataflow programming",
        ],
        classifiers=[
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: Implementation :: CPython",
            "Development Status :: 5 - Production/Stable",
            'Natural Language :: English',
            "Intended Audience :: Developers",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: European Union Public Licence 1.1 "
            "(EUPL 1.1)",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX",
            "Operating System :: Unix",
            "Operating System :: OS Independent",
            "Topic :: Scientific/Engineering",
            "Topic :: Scientific/Engineering :: Information Analysis",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: Utilities",
        ],
        install_requires=[],
        extras_require=extras,
        test_suite='nose.collector',
        tests_require=['nose>=1.0', 'requests', 'cryptography'],
        package_data={
            'schedula.utils.drw': [
                'templates/*', 'index/js/*', 'index/css/*', 'viz/*'
            ]
        },
    )
