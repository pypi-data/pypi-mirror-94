#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright 2015-2021, Vincenzo Arcidiacono;
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl

"""
It is a patch to sphinx.ext.autosummary.
"""
import warnings
import logging
import os.path as osp
from sphinx import package_dir
from sphinx.util.osutil import ensuredir
from sphinx.util.inspect import safe_getattr
from jinja2.sandbox import SandboxedEnvironment
from sphinx.jinja2glue import BuiltinTemplateLoader
from jinja2 import FileSystemLoader, TemplateNotFound
from sphinx.ext.autosummary import import_by_name, get_documenter
from sphinx.ext.autosummary.generate import (
    _simple_warn, _simple_info, find_autosummary_in_files
)

try:
    from sphinx.ext.autosummary.generate import AutosummaryEntry
except ImportError:
    class AutosummaryEntry:
        pass

logger = logging.getLogger(__name__)
warnings.filterwarnings(
    'ignore', category=DeprecationWarning, module='docutils'
)


def get_members(app, obj, typ, include_public=(), imported=False):
    items = []
    for name in dir(obj):
        try:
            obj_name = safe_getattr(obj, name)
            try:
                documenter = get_documenter(app, obj_name, obj)
            except TypeError:
                documenter = get_documenter(obj_name, obj)

        except AttributeError:
            continue
        if documenter.objtype == typ:
            try:
                cond = imported or (obj_name.__module__ == obj.__name__)
            except AttributeError:
                cond = True

            if cond:
                items.append(name)
    skip = set(app.config.autosummary_skip_members)
    _n = '{}.%s'.format(obj.__name__)

    public = [
        x for x in items
        if (x in include_public or not x.startswith('_')) and _n % x not in skip
    ]
    return public, items


def generate_autosummary_docs(
        sources, output_dir=None, suffix='.rst', warn=_simple_warn,
        info=_simple_info, base_path=None, builder=None, template_dir=None,
        app=None):
    showed_sources = list(sorted(sources))
    if len(showed_sources) > 20:
        showed_sources = showed_sources[:10] + ['...'] + showed_sources[-10:]
    info('[autosummary] generating autosummary for: %s' %
         ', '.join(showed_sources))

    if output_dir:
        info('[autosummary] writing to %s' % output_dir)

    if base_path is not None:
        sources = [osp.join(base_path, filename) for filename in sources]

    # create our own templating environment
    template_dirs = [osp.join(package_dir, 'ext', 'autosummary', 'templates')]
    if builder is not None:
        # allow the user to override the templates
        template_loader = BuiltinTemplateLoader()
        template_loader.init(builder, dirs=template_dirs)
    else:
        if template_dir:
            template_dirs.insert(0, template_dir)
        template_loader = FileSystemLoader(template_dirs)
    template_env = SandboxedEnvironment(loader=template_loader)

    # read
    items = find_autosummary_in_files(sources)
    items = [
        isinstance(v, AutosummaryEntry) and (v.name, v.path, v.template) or v
        for v in items
    ]
    # remove possible duplicates
    items = list(dict([(item, True) for item in items]).keys())

    # keep track of new files
    new_files = []

    # write
    # noinspection PyTypeChecker
    for name, path, template_name in sorted(items, key=str):
        if path is None:
            # The corresponding autosummary:: directive did not have
            # a :toctree: option
            continue

        path = output_dir or osp.abspath(path)
        ensuredir(path)

        try:
            name, obj, parent, mod_name = import_by_name(name)
        except ImportError as e:
            warn('[autosummary] failed to import %r: %s' % (name, e))
            continue

        fn = osp.join(path, name + suffix)

        # skip it if it exists
        if osp.isfile(fn):
            continue

        new_files.append(fn)

        f = open(fn, 'w')

        try:
            try:
                doc = get_documenter(app, obj, parent)
            except TypeError:
                doc = get_documenter(obj, parent)

            if template_name is not None:
                template = template_env.get_template(template_name)
            else:
                try:
                    template = template_env.get_template('autosummary/%s.rst'
                                                         % doc.objtype)
                except TemplateNotFound:
                    template = template_env.get_template('autosummary/base.rst')

            ns = {}

            if doc.objtype == 'module':
                ns['members'] = dir(obj)
                ns['functions'], ns['all_functions'] = \
                    get_members(app, obj, 'function')
                ns['classes'], ns['all_classes'] = \
                    get_members(app, obj, 'class')
                ns['exceptions'], ns['all_exceptions'] = \
                    get_members(app, obj, 'exception')
                ns['data'], ns['all_data'] = \
                    get_members(app, obj, 'data', imported=True)

                ns['data'] = ', '.join(ns['data'])
                ns['all_data'] = ', '.join(ns['all_data'])

                ns['dispatchers'], ns['all_dispatchers'] = \
                    get_members(app, obj, 'dispatcher', imported=True)
            elif doc.objtype == 'class':
                ns['members'] = dir(obj)
                ns['methods'], ns['all_methods'] = \
                    get_members(app, obj, 'method', ['__init__'], True)
                ns['attributes'], ns['all_attributes'] = \
                    get_members(app, obj, 'attribute')

            parts = name.split('.')
            if doc.objtype in ('method', 'attribute'):
                mod_name = '.'.join(parts[:-2])
                cls_name = parts[-2]
                obj_name = '.'.join(parts[-2:])
                ns['class'] = cls_name
            else:
                mod_name, obj_name = '.'.join(parts[:-1]), parts[-1]

            ns['fullname'] = name
            ns['module'] = mod_name
            ns['objname'] = obj_name
            ns['name'] = parts[-1]

            ns['objtype'] = doc.objtype
            ns['underline'] = len(name) * '='

            rendered = template.render(**ns)
            f.write(rendered)
        finally:
            f.close()

    # descend recursively to new files
    if new_files:
        generate_autosummary_docs(new_files, output_dir=output_dir,
                                  suffix=suffix, warn=warn, info=info,
                                  base_path=base_path, builder=builder,
                                  template_dir=template_dir, app=app)


def process_generate_options(app):
    genfiles = app.config.autosummary_generate

    if genfiles and not hasattr(genfiles, '__len__'):
        env = app.builder.env
        genfiles = [env.doc2path(x, base=None) for x in env.found_docs
                    if osp.isfile(env.doc2path(x))]

    if not genfiles:
        return

    ext = tuple(app.config.source_suffix)
    genfiles = [genfile + (not genfile.endswith(ext) and ext[0] or '')
                for genfile in genfiles]
    try:
        from sphinx.ext.autosummary import get_rst_suffix
        suffix = get_rst_suffix(app)
    except ImportError:
        suffix = '.rst'

    if suffix is None:
        logger.warning('autosummary generats .rst files internally. '
                       'But your source_suffix does not contain .rst. Skipped.')
        return
    generate_autosummary_docs(genfiles, builder=app.builder,
                              warn=logger.warning, info=logger.info,
                              suffix=suffix, base_path=app.srcdir, app=app)


def setup(app):
    app.setup_extension('sphinx.ext.autosummary')
    app.add_config_value('autosummary_skip_members', [], 'html')

    # replace callback process_generate_options of 'builder-inited' event.
    import sphinx.ext.autosummary as mdl
    pgo = mdl.process_generate_options
    event = 'builder-inited'

    try:
        listeners = app._listeners[event]
    except AttributeError:  # Sphinx 1.6.2
        listeners = app.events.listeners[event]
    if isinstance(listeners, list):  # Sphinx >= 3.0.0
        from sphinx.events import EventListener
        for i, event in enumerate(listeners):
            if pgo in event:
                listeners[i] = EventListener(*(
                    process_generate_options if e is pgo else e for e in event
                ))
    else:
        for listener_id, callback in listeners.items():
            if callback is pgo:
                listeners[listener_id] = process_generate_options
