#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright 2015-2021, Vincenzo Arcidiacono;
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl

"""
It provides functions to plot dispatcher map and workflow.

Sub-Modules:

.. currentmodule:: schedula.utils.drw

.. autosummary::
    :nosignatures:
    :toctree: drw/

    nodes
"""

import os
import glob
import copy
import html
import regex
import socket
import pprint
import string
import shutil
import inspect
import weakref
import logging
import datetime
import platform
import tempfile
import functools
import itertools
import collections
import os.path as osp
import urllib.parse as urlparse

from ..cst import START, SINK, END, EMPTY, SELF, NONE, PLOT
from ..dsp import SubDispatch, combine_dicts, map_dict, combine_nested_dicts, \
    selector, stlp, parent_func, get_nested_dicts, NoSub
from ..gen import counter

__author__ = 'Vincenzo Arcidiacono <vinci1it2000@gmail.com>'

log = logging.getLogger(__name__)

PLATFORM = platform.system().lower()

_UNC = u'\\\\?\\' if PLATFORM == 'windows' else ''


def uncpath(p):
    return _UNC + osp.abspath(p)


def _encode_file_name(s):
    """
    Take a string and return a valid filename constructed from the string.

    Uses a whitelist approach: any characters not present in valid_chars are
    removed. Also spaces are replaced with underscores.
    """

    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ', '_')  # I don't like spaces in filenames.
    return filename


def _upt_styles(styles, base=None):
    d, base = {}, copy.deepcopy(base or {})
    res = {}
    for i in ('info', 'warning', 'error'):
        combine_nested_dicts(base.get(i, {}), styles.get(i, {}), base=d)
        res[i] = copy.deepcopy(d)
    return res


def autoplot_function(kwargs):
    keys = sorted(kwargs, key=lambda x: (x is not PLOT, x))
    kw = combine_dicts(*selector(keys, kwargs, output_type='list'))
    return {'dsp': kw.pop('obj'), 'kw': kw}


def autoplot_callback(res):
    res['plot'] = res['dsp'].plot(**res['kw'])


def jinja2_format(source, context=None, **kw):
    from jinja2 import Environment
    return Environment(**kw).from_string(source).render(context or {})


def valid_filename(item, filenames, ext=None):
    if isinstance(item, str):
        _filename = item
    else:
        _filename = item._filename
        if ext is None:
            ext = item.ext
    _ = '%s' + ('.{}'.format(ext) if ext != '' else '')

    filename, c = _ % _filename, counter()
    while filename in filenames:
        filename = _ % '{}-{}'.format(_filename, c())
    return filename


def update_filenames(node, filenames):
    if node is not None:
        filename = valid_filename(node, filenames)
        yield (node, None), (filename,)
        filenames.add(filename)
        base = osp.splitext(filename)[0]
        for _, file in node.extra_files:
            filename, ext = osp.splitext(file)
            filename = valid_filename(filename, filenames, ext=ext[1:])
            yield (node, file), (osp.join(base, filename),)
            filenames.add(osp.split(filename)[0].split('.')[0])


def site_view(
        app, node, context, generated_files, rendered, extra=None, viz=False):
    static_folder, filepath = app.static_folder, context[(node, extra)]
    if not osp.isfile(osp.join(static_folder, filepath)):
        files = cached_view(node, static_folder, context, rendered, viz)
        generated_files.extend(files.values())
    return app.send_static_file(filepath)


def render_output(out, pformat):
    out = parent_func(out)
    if inspect.isfunction(out):
        # noinspection PyBroadException
        try:
            out = inspect.getsource(out)
        except Exception:
            pass

    if isinstance(out, (datetime.datetime, datetime.timedelta)):
        out = str(out)

    if isinstance(out, str):
        return out

    return pformat(out)


class SiteNode:
    counter = counter()
    ext = 'html'
    pprint = pprint.PrettyPrinter(compact=True, width=200)

    def __init__(self, folder, node_id, item, obj, dsp_node_id):
        self.folder = folder
        self.node_id = node_id
        self.item = item
        self.obj = obj
        self.id = str(self.counter())
        self.dsp_node_id = dsp_node_id
        self.extra_files = []

    @property
    def name(self):
        try:
            return parent_func(self.item).__name__
        except AttributeError:
            return self.node_id

    @property
    def view_id(self):
        return id(self.item), self.__class__.__name__

    @property
    def title(self):
        return self.name

    @property
    def _filename(self):
        return _encode_file_name(self.title)

    @property
    def filename(self):
        return '.'.join((self._filename, self.ext))

    def __repr__(self):
        return self.title

    def render(self, *args, **kwargs):
        from pygments import highlight
        from pygments.lexers import Python3Lexer
        from pygments.formatters import HtmlFormatter
        code = render_output(self.item, self.pprint.pformat)
        formatter = HtmlFormatter(noclasses=True)
        formatter.style.background_color = 'transparent'
        return _format_output(highlight(code, Python3Lexer(), formatter))

    def view(self, filepath, *args, **kwargs):
        fpath = uncpath(filepath)
        os.makedirs(osp.dirname(fpath), exist_ok=True)
        with open(fpath, 'w') as f:
            f.write(self.render(*args, **kwargs))
        rend = {(self.view_id, None): fpath}
        directory = osp.splitext(filepath)[0]
        for src, fn in self.extra_files:
            dst = uncpath(osp.join(directory, fn))
            os.makedirs(osp.dirname(dst), exist_ok=True)
            shutil.copy(src(**kwargs) if callable(src) else src, dst)
            rend[(self.view_id, src)] = dst
        return rend


class FolderNode:
    counter = counter()

    node_styles = _upt_styles({
        'info': {
            START: {'shape': 'egg', 'fillcolor': 'red', 'label': 'start'},
            SELF: {'shape': 'egg', 'fillcolor': 'gold', 'label': 'self'},
            PLOT: {'shape': 'egg', 'fillcolor': 'gold', 'label': 'plot'},
            END: {'shape': 'egg', 'fillcolor': 'blue', 'fontcolor': 'white',
                  'label': 'end'},
            EMPTY: {'shape': 'egg', 'fillcolor': 'gray', 'label': 'empty'},
            SINK: {'shape': 'egg', 'fillcolor': 'black', 'fontcolor': 'white',
                   'label': 'sink'},
            NONE: {
                'data': {'shape': 'box', 'style': 'rounded,filled',
                         'fillcolor': 'cyan'},
                'function': {'shape': 'box', 'fillcolor': 'springgreen'},
                'subdispatch': {'shape': 'note', 'style': 'filled',
                                'fillcolor': 'yellow'},
                'mapdispatch': {'shape': 'note', 'style': 'filled',
                                'fillcolor': 'seagreen1'},
                'subdispatchfunction': {'shape': 'note', 'style': 'filled',
                                        'fillcolor': 'yellowgreen'},
                'subdispatchpipe': {'shape': 'note', 'style': 'filled',
                                    'fillcolor': 'greenyellow'},
                'dispatchpipe': {'shape': 'note', 'style': 'filled',
                                 'fillcolor': 'chartreuse'},
                'dispatcher': {'shape': 'note', 'style': 'filled',
                               'fillcolor': 'springgreen'},
                'edge': {None: None}
            }
        },
        'warning': {
            NONE: {
                'data': {'fillcolor': 'orange'},
                'function': {'fillcolor': 'orange'},
                'subdispatch': {'fillcolor': 'orange'},
                'subdispatchfunction': {'fillcolor': 'orange'},
                'subdispatchpipe': {'fillcolor': 'orange'},
                'dispatchpipe': {'fillcolor': 'orange'},
                'dispatcher': {'fillcolor': 'orange'},
            }
        },
        'error': {
            NONE: {
                'data': {'fillcolor': 'red'},
                'function': {'fillcolor': 'red'},
                'subdispatch': {'fillcolor': 'red'},
                'subdispatchfunction': {'fillcolor': 'red'},
                'subdispatchpipe': {'fillcolor': 'red'},
                'dispatchpipe': {'fillcolor': 'red'},
                'dispatcher': {'fillcolor': 'red'},
            }
        }
    })

    node_data = (
        '-', '.tooltip', '!default_values', 'wait_inputs', 'await_result',
        '+function|solution', 'weight', 'remote_links',
        '+filters|solution_filters', 'distance', '!error', '*output'
    )

    node_function = (
        '-', '.tooltip', 'await_domain', 'await_result',
        '+input_domain|solution_domain', 'weight', '+filters|solution_filters',
        'missing_inputs_outputs', 'distance', 'started', 'duration', '!error',
        '*function|solution'
    )

    edge_data = '?', '+wildcard', 'inp_id', 'out_id', 'weight'

    node_map = {
        '-': (),  # Add title.
        '?': (),  # Optional title.
        '': ('dot', 'table'),  # item in the table.
        '+': ('dot', 'table'),  # link.
        '!': ('dot', 'table'),  # if str is big add a link, otherwise table.
        '.': ('dot',),  # dot attr.
        '*': ('link',)  # title link.
    }
    re_node = regex.compile(r"^([.*+!]?)([\w ]+)(?>\|([\w ]+))?$")
    max_lines = 5
    max_width = 200
    pprint = pprint.PrettyPrinter(compact=True, width=200)

    def __init__(self, folder, node_id, attr, **options):
        self.folder = folder
        self.node_id = node_id
        self.attr = attr
        self.id = str(self.counter())
        self._links = {}
        for k, v in options.items():
            setattr(self, k, v)

    @property
    def title(self):
        return self.attr.get('title', self.node_id)

    @property
    def type(self):
        return self.attr.get('type', 'data')

    def __repr__(self):
        return self.title

    def yield_attr(self, name):
        try:
            yield name, self.attr[name]
        except KeyError:
            pass

    def render_size(self, out):
        lines = render_output(out, self.pprint.pformat).splitlines(True)
        n, w = self.max_lines, self.max_width
        return len(lines) <= n and not any(len(v) > w for v in lines)

    def items(self):
        check = self.render_size
        for k, func in self.render_funcs():
            if k and k in '*+':
                yield from func()
            elif k == '!':
                yield from ((i, j) for i, j in func() if not check(j))

    def _tooltip(self):
        try:
            from ..des import search_node_description
            tooltip = search_node_description(
                self.node_id, self.attr, self.folder.dsp
            )[0]
        except (AttributeError, KeyError):
            tooltip = None
        yield 'tooltip', '"%s"' % (tooltip or self.title).replace('"', "'")

    def _wait_inputs(self):
        attr = self.attr
        try:
            if attr['type'] == 'data' and attr['wait_inputs']:
                yield 'wait_inputs', attr['wait_inputs']
        except KeyError:
            pass

    def _default_values(self):
        try:
            dfl = self.folder.dsp.default_values.get(self.node_id, {})
            res = map_dict({'value': 'default'}, dfl)

            if not res.get('initial_dist', 1):
                res.pop('initial_dist')
        except AttributeError:
            res = {}
        yield from sorted(res.items())

    def _filters(self):
        try:
            for i, f in enumerate(self.attr['filters']):
                yield 'filter %d' % i, f
        except (AttributeError, KeyError):
            pass

    def _solution_filters(self):
        try:
            it = self.attr['solution_filters']
            yield 'input_filter 0', it[0]
            for i, f in enumerate(it[1:]):
                yield 'output_filter %d' % i, f
        except (AttributeError, KeyError, IndexError):
            pass

    def _remote_links(self):
        if not self.folder.parent:
            return
        dsp_id, dsp = self.folder.name, self.folder.parent.dsp
        node = dsp.nodes[dsp_id]
        if node['type'] == 'dispatcher':
            i, nid = 0, self.node_id
            for k, tag in (('inputs', 'parent'), ('outputs', 'child')):
                d = node.get(k, {})
                if tag == 'parent':
                    n = tuple(k for k, v in d.items() if nid in stlp(v))
                else:
                    n = stlp(d.get(nid, ()))

                if not n:
                    continue
                elif len(n) == 1:
                    n = n[0]

                n = 'parent_ref("{}", attr)'.format(n)
                yield 'remote %s %d' % (tag, i), '{{%s}}' % n
                i += 1

    def _output(self):
        if self.node_id not in (START, SINK, SELF, END):
            try:
                out = self.folder.item[self.node_id]
                yield 'output', out
            except (KeyError, TypeError):
                pass  # Output not in solution or item is not a solution.

    def _started(self):
        try:
            if isinstance(self.attr['started'], str):
                yield 'started', self.attr['started']
            else:
                started = datetime.datetime.fromtimestamp(self.attr['started'])
                yield 'started', started.isoformat()
        except KeyError:
            pass

    def _duration(self):
        k = 'duration'
        try:
            if isinstance(self.attr[k], str):
                yield k, self.attr[k]
            else:
                yield k, datetime.timedelta(seconds=self.attr[k])
        except KeyError:
            pass

    def _distance(self):
        try:
            yield 'distance', self.folder.item.dist[self.node_id]
        except (AttributeError, KeyError):
            yield from self.yield_attr('distance')

    def _weight(self):
        try:
            yield 'weight', self.attr['weight']
        except (AttributeError, KeyError):
            pass

    def _missing_inputs_outputs(self):
        attr, res = self.attr, {}
        try:
            if attr['wait_inputs']:
                graph = self.folder.graph
                pred, succ = graph.pred[self.node_id], graph.succ[self.node_id]
                for i, j in (('inputs', pred), ('outputs', succ)):
                    v = tuple(k for k in attr[i] if k not in j)
                    if v:
                        yield 'M_%s' % i, v
        except (AttributeError, KeyError):
            pass

    def _wildcard(self):
        if 'wildcard' in self.attr:
            if self.folder.workflow and 'value' in self.attr:
                yield 'wildcard', self.attr['value']

    def style(self):
        attr = self.attr

        if 'error' in attr:
            nstyle = 'error'
        elif list(self._missing_inputs_outputs()):
            nstyle = 'warning'
        else:
            nstyle = 'info'

        node_styles = self.node_styles.get(nstyle, self.node_styles['info'])
        if self.node_id in node_styles:
            node_style = node_styles[self.node_id].copy()
            node_style.pop(None, None)
            return node_style
        else:
            if self.type in ('dispatcher', 'function'):
                ntype = 'function',
                try:
                    ntype = (_get_type(attr['function']),) + ntype
                except (KeyError, AttributeError):
                    pass
            elif self.type == 'edge':
                ntype = 'edge',
            else:
                ntype = 'data',
            for style in ntype:
                try:
                    node_style = node_styles[NONE][style].copy()
                    node_style.pop(None, None)
                    return node_style
                except KeyError:
                    pass

    def render_funcs(self):
        if self.type in ('dispatcher', 'function'):
            funcs = self.node_function
        elif self.type == 'edge':
            funcs = self.edge_data
        else:
            funcs = self.node_data
        r, s, match = {}, '_%s', self.re_node.match
        workflow = self.folder.workflow
        for f in funcs:
            if f == '-' or f == '?':
                yield f, lambda *args: self.title
            else:
                k, v, v1 = match(f).groups()
                if workflow and v1:
                    try:
                        yield k, getattr(self, s % v1)
                        continue
                    except AttributeError:
                        if v1 in self.attr:
                            yield k, functools.partial(self.yield_attr, v1)
                            continue
                try:
                    yield k, getattr(self, s % v)
                except AttributeError:
                    yield k, functools.partial(self.yield_attr, v)

    def parent_ref(self, context, node_id, attr=None):
        attr, text = attr or {}, '(%s)' % node_id
        try:
            dirname = osp.dirname(context[(self.folder, None)])
            node, rule = next((n, f) for (n, e), f in context.items()
                              if e is None and dirname == osp.splitext(f)[0])
            attr, href = attr.copy(), osp.relpath(rule, dirname)
            node_id = next(
                '?id=%d' % n.attr['index'][-1]
                for n in node.nodes
                if n.node_id == node_id
            )
            attr['href'] = html.escape(urlparse.unquote('./%s%s' % (
                href.replace('\\', '/'), node_id or ''
            )))
        except StopIteration:
            pass

        return '_Td(**{}).add("{}")'.format(attr, text)

    def href(self, context, link_id):
        res = {}
        if link_id in self._links:
            node = self._links[link_id]
            res['text'] = node.title
            try:
                dirname = osp.dirname(context[(self.folder, None)])
                href = osp.relpath(context[(node, None)], dirname)
                res['href'] = urlparse.unquote('./%s' % href.replace('\\', '/'))
            except KeyError:
                pass
        return res

    def dot(self, context=None):
        if context is None:
            context = {}
        dot = self.style()
        if 'label' in dot:
            dot.update(self.attr.get('graphviz', {}))
            return dot
        from .nodes import _Tr, _Td
        key, val = dict(ALIGN="RIGHT", BORDER=1), dict(ALIGN="LEFT", BORDER=1)
        rows, funcs, cnt = [], list(self.render_funcs()), {'attr': val}
        cnt['parent_ref'] = functools.partial(self.parent_ref, context)
        href, pformat, links = self.href, self.pprint.pformat, self._links
        for k, func in funcs:
            if k == '.':
                dot.update(func())
            elif not (k == '*' or k == '-' or k == '?'):

                for i, j in func():
                    tr = _Tr().add(i, **key)
                    if i in links and (k == '!' or k == '+'):
                        v = combine_dicts(val, {'text': j}, href(context, i))
                        tr.add(**v)
                    else:
                        j = render_output(j, pformat)
                        s = jinja2_format(j, cnt)
                        if s.startswith('_Td('):
                            tr += eval(s)
                        else:  # It is not a valid jinja2 format.
                            tr.add(j, **val)
                    rows.append(tr)

        def get_link():
            for _k, f in funcs:
                if _k == '*':
                    for _link_id in f():
                        return _link_id[0]

        if any(k[0] == '-' or (rows and k[0] == '?') for k in funcs):
            link_id = get_link()
            kw = combine_dicts(
                self.href(context, link_id),
                {'COLSPAN': 2, 'BORDER': 0, 'text': self.title}
            )
            rows = [_Tr().add(**kw)] + rows

        if rows:
            k = 'xlabel' if self.type == 'edge' else 'label'
            k = self.attr.get('label_type', k)
            from .nodes import _Table
            dot[k] = '<%s>' % _Table(BORDER=0, CELLSPACING=0).adds(rows)
        dot.update(self.attr.get('graphviz', {}))
        return {k: str(v) for k, v in dot.items()}


def _format_output(obj, **kwargs):
    import pkg_resources
    from jinja2 import PackageLoader
    pkg_dir = pkg_resources.resource_filename(__name__, '')
    fpath = osp.join(pkg_dir, 'templates', 'render.html')
    with open(fpath) as template:
        return jinja2_format(
            template.read(), combine_dicts({'obj': obj}, kwargs),
            loader=PackageLoader(__name__)
        )


def _format_kw_digraph(*dicts, base=None):
    kw = combine_nested_dicts(*dicts, base=base)
    if 'body' in kw:
        kw['body'] = ['%s = %s' % (k, v) for k, v in sorted(kw['body'].items())]
    return kw


class SiteFolder:
    counter = SiteNode.counter
    digraph = {
        'node_attr': {'style': 'filled'},
        'graph_attr': {'bgcolor': 'transparent'},
        'edge_attr': {},
        'body': {'splines': 'ortho', 'style': 'filled'},
        'format': 'svg'
    }
    folder_node = FolderNode
    ext = 'html'

    def __init__(self, item, dsp, graph, obj, name='', workflow=False,
                 digraph=None, parent=None, **options):
        self.item, self.dsp, self.graph, self.obj = item, dsp, graph, obj
        self._name = name
        self.workflow = workflow
        self.parent = parent
        self.id = str(self.counter())
        self.options = options
        nodes = collections.OrderedDict(self._nodes)
        self.nodes = list(nodes.values())
        self.edges = [e for k, e in self._edges(nodes)]
        self.sitemap = None
        self.extra_files = []
        if digraph is not None:
            self.digraph = combine_dicts(self.__class__.digraph, digraph)

    @property
    def view_id(self):
        return id(self.item), self.__class__.__name__

    @property
    def title(self):
        return self.name or ''

    @property
    def _filename(self):
        return _encode_file_name(self.title)

    @property
    def filename(self):
        return '.'.join((self._filename, self.ext))

    def __repr__(self):
        return self.title

    @property
    def inputs(self):
        try:
            from ..sol import Solution
            if isinstance(self.item, Solution):
                return self.item.parent.inputs or ()
            return self.item.inputs or ()
        except AttributeError:
            return ()

    @property
    def outputs(self):
        item = self.item
        from ..sol import Solution
        try:
            if isinstance(item, Solution):
                item = item.parent
            if isinstance(item, SubDispatch) and item.output_type != 'all':
                return item.outputs or ()
        except AttributeError:
            pass
        return ()

    @property
    def name(self):
        if not self._name:
            dsp = self.dsp
            name = dsp.name or '%s %d' % (type(dsp).__name__, id(dsp))
        else:
            name = self._name
        return name

    @property
    def label_name(self):
        return 'workflow' if self.workflow else 'dmap'

    @property
    def _nodes(self):
        try:
            errors = self.item._errors
        except AttributeError:
            errors = {}
        nodes, graph = self.dsp.nodes, self.graph
        gnode, succ, pred = graph.nodes, graph.succ, graph.pred
        it = {
            i: v for i, v in gnode.items()
            if i in nodes and (i is not SINK or succ[SINK] or pred[SINK])
        }
        if not nodes or not (graph.edges or self.inputs or self.outputs):
            it[EMPTY] = {'index': (EMPTY,)}

        if START in gnode or any(i in it for i in self.inputs):
            it[START] = {'index': (START,)}

        if any(o in it for o in self.outputs) and END not in gnode:
            it[END] = {'index': (END,)}

        for k, a in sorted(it.items()):
            attr = combine_dicts(nodes.get(k, {}), a)
            if k in errors:
                attr['error'] = errors[k]

            yield k, self.folder_node(self, k, attr, **self.options)

    def _edges(self, nodes):
        edges = {(u, v): a for (u, v), a in self.graph.edges.items() if u != v}
        from ..sol import Solution
        from ..dsp import SubDispatchFunction
        wildcards = ()
        if isinstance(self.item, Solution):
            wildcards = self.item._wildcards
        elif isinstance(self.item, SubDispatchFunction):
            wildcards = self.item._sol._wildcards

        for i, v in enumerate(self.inputs):
            if v != START and v in nodes:
                n = (START, v)
                edges[n] = combine_dicts(edges.get(n, {}), {'inp_id': i})

        for i, u in enumerate(self.outputs):
            if u != END and u in nodes:
                n = (u, END)
                edges[n] = combine_dicts(edges.get(n, {}), {'out_id': i})

        for w in [v for u, v in edges if u is START and v in wildcards]:
            a = combine_dicts(edges.pop((START, w)), dict(
                label_type='label', wildcard=w, title=w
            ))
            a1 = selector(('value',), a, allow_miss=True)
            for u, v in list(edges):
                if u == w and v != END:
                    edges[(START, v)] = combine_dicts(a, edges.pop((u, v)), a1)

        d_nodes = self.dsp.nodes
        for (u, v), a in edges.items():
            base = {'type': 'edge', 'dot_ids': (nodes[u].id, nodes[v].id)}
            a = combine_dicts(a, base=base)
            if v in d_nodes and d_nodes[v]['type'] == 'dispatcher':
                if not a.get('weight', 1):
                    a.pop('weight')
            elif a.get('weight') == 1:
                a.pop('weight')

            yield (u, v), self.folder_node(self, '{} --> {}'.format(u, v), a)

    def dot(self, context=None):
        context = context or {}

        kw = _format_kw_digraph(self.digraph, base=dict(
            name=self.label_name,
            body={'label': '<%s>' % self.label_name}
        ))
        from .nodes import _DspPlot
        dot = _DspPlot(self.sitemap, **kw)
        id_map, clr = {}, {}
        for node in self.nodes:
            i = id_map[node.node_id] = node.id
            dot.node(i, id=str(node.attr['index'][-1]), **node.dot(context))
            clusters = node.attr.get('clusters', ())
            if isinstance(clusters, (str, dict)):
                clusters = clusters,
            for c in clusters:
                if isinstance(c, dict):
                    j = c['body']['label']
                    combine_nested_dicts(c, base=get_nested_dicts(clr, j, 'kw'))
                    if j and j[0] == '<' and j[-1] == '>':
                        j = j[1:-1]
                else:
                    j = c
                get_nested_dicts(clr, j, 'nodes', default=list).append(i)

        for edge in self.edges:
            dot.edge(*edge.attr['dot_ids'], **edge.dot(context))

        for i, (cluster, d) in enumerate(clr.items()):
            kw = _format_kw_digraph(d.get('kw', {}), base=dict(
                name='cluster_%d' % i, body={'label': '<%s>' % cluster}
            ))
            with dot.subgraph(**kw) as g:
                for node in d['nodes']:
                    g.node(node)
        return dot

    def view(self, filepath, context=None, viz=False):
        dot = self.dot(context=context)
        dot.format = self.digraph['format']
        filepath = uncpath(filepath)
        if osp.isfile(filepath):
            os.remove(filepath)
        else:
            os.makedirs(osp.dirname(filepath), exist_ok=True)
        if viz and dot.format == 'svg':
            out = '<viz engine="%s" digraph="%s"/>'
            out %= dot.engine, html.escape(dot.source)
        else:
            try:
                # noinspection PyArgumentList
                fpath = dot.render(directory=tempfile.mkdtemp(), cleanup=True)
                with open(fpath) as src:
                    out = src.read()
                os.remove(fpath)
            except Exception as ex:
                log.error('dot could not render %s due to:\n %r', filepath, ex)
                return {}
        with open(filepath, 'w') as dst:
            if viz:
                viz = len(context[(self, None)].split(osp.sep)) - 1
                viz = '/'.join(('..',) * viz + ('viz.js',))
            dst.write(_format_output(out, viz=viz))
        return {(self.view_id, None): filepath}


def _get_type(obj):
    from ..sol import Solution
    obj = isinstance(obj, Solution) and obj.parent or obj
    return type(parent_func(obj)).__name__.lower()


sort_tree_map = {v: k for k, v in enumerate((
    'data', 'function', 'dispatchpipe', 'subdispatchpipe',
    'subdispatchfunction', 'mapdispatch', 'subdispatch', 'dispatcher'
), 1)}


def _folder2tree(folder, smap, context, type):
    extra, extra_dsp = {}, {item.name: (item, v) for item, v in smap.items()}
    for item in smap.nodes:
        get_nested_dicts(extra, item.dsp_node_id, default=list).append(item)
    url = context[(folder, None)]
    nodes = [
        dict(text='-%s' % type, url=url, type=type)
    ]
    url = '{}?id=%d'.format(url)
    for node_id, attr in folder.dsp.nodes.items():
        if node_id not in folder.graph.nodes:
            continue
        type = attr['type']
        if type == 'function' and attr.get('function'):
            type = _get_type(attr['function'])
        n = dict(
            text=html.escape(node_id),
            url=url % attr['index'][-1],
            type=type
        )
        nodes.append(n)
        if node_id in extra_dsp:
            n['nodes'] = _folder2tree(*extra_dsp[node_id], context, type)
        else:
            i = len(node_id)
            n['nodes'] = [dict(
                text=html.escape(item.title[i:] or '-function'),
                url=context[(item, None)],
                type=_get_type(item.item)
            ) for item in extra.get(node_id, [])]
        if not n['nodes']:
            n.pop('nodes')
    return nodes[:1] + list(sorted(
        nodes[1:], key=lambda x: sort_tree_map.get(x['type'], 0), reverse=True
    ))


def _pipe2icicle(pipe):
    for k, v in pipe.items():
        child, (i, s) = dict(name=' → '.join(stlp(k))), v['task'][2]
        value, t = 0, s.workflow.nodes.get(i, {}).get('duration')
        if 'sub_pipe' in v:
            child['children'] = children = list(_pipe2icicle(v['sub_pipe']))
            dt = sum((v['duration'] for v in children), 0)
            if t is None:
                t = dt
            else:
                value = t - dt
        else:
            value = t or 0
        child['duration'] = t or 0
        child['value'] = value
        yield child


def _sitemap2icicle(sitemap):
    cdn = []
    for folder in sitemap:
        try:
            pipe = folder.item.pipe
        except AttributeError:
            continue
        c = list(_pipe2icicle(pipe))
        cdn.append(dict(
            name=folder.name, children=c, value=0,
            duration=sum((v['duration'] for v in c), 0)
        ))
    if not cdn:
        return {}
    return dict(
        name='main', duration=sum((v['duration'] for v in cdn), 0), children=cdn
    )


def _sitemap2tree(sitemap, context):
    tree = []
    for folder, smap in sitemap.items():
        type = _get_type(folder.item)
        tree.append(dict(
            text=html.escape(folder.name),
            url=context[(folder, None)],
            type=type,
            nodes=_folder2tree(folder, smap, context, type)[1:]
        ))
    return tree


def _add_explanation(dsp, node_id, description, **kw):
    dsp.dmap.add_edge(node_id, dsp.add_data(graphviz=dict(
        label=description, shape='plaintext', style='', fillcolor=''
    ), **kw), graphviz={'style': 'dashed'})
    return node_id


class NoView:
    pass


class SiteViz(SiteNode, NoView):
    ext = 'js'

    def __init__(self, sitemap, node_id='viz'):
        super(SiteViz, self).__init__(None, node_id, self, None, object())
        self.sitemap = sitemap

    def render(self, context, *args, **kwargs):
        import pkg_resources
        dfl_folder = osp.join(
            pkg_resources.resource_filename(__name__, ''), 'viz'
        )
        with open(osp.join(dfl_folder, 'viz.js')) as f:
            return f.read()


class SiteIndex(SiteNode):
    ext = 'html'

    def __init__(self, sitemap, node_id='index'):
        super(SiteIndex, self).__init__(None, node_id, self, None, object())
        self.sitemap = sitemap
        import pkg_resources
        dfl_folder = osp.join(
            pkg_resources.resource_filename(__name__, ''), 'index'
        )
        for default_file in glob.glob(osp.join(dfl_folder, '**/*')):
            if osp.isfile(default_file):
                self.extra_files.append(
                    (default_file, osp.relpath(default_file, dfl_folder))
                )
        self.extra_files.append((self.legend, 'html/legend.html'))

    # noinspection PyUnusedLocal
    @staticmethod
    def legend(viz=False, **kwargs):
        import schedula as sh
        dsp = sh.Dispatcher(name='legend')
        _add_explanation(dsp, dsp.add_data(
            clusters='Data',
            data_id='<data_id>(Data)',
            default_value='Default value.',
            initial_dist='Initial distance from `START` node.',
            wait_inputs='Wait all data estimations? `<bool>`',
            function='Process data function `data = f({"<node name>": data})`.',
            callback='Callback function `f(data)`.',
            await_result='Wait async for function result? `<bool>`',
            distance='Distance from `START` node.',
            started='Execution started time.',
            duration='Time elapsed to execute all functions '
                     'that belong to the node.',
            **{'remote parent x': 'Link to a node of the parent dispatcher.',
               'remote child x': 'Link to a node ot a child dispatcher.',
               'filter x': 'Filter function x used in the loop '
                           '`for f in filters: data = f(data)`.',
               'input_filter 0': 'Result of the function.',
               'output_filter x': 'Result of filters[x](`input_filter x` | '
                                  '`output_filter x-1`).'}
        ), clusters='Data', description=(
            'Data node. The current one is a\n'
            'sample showing the main attributes.'
        ))
        _add_explanation(
            dsp, dsp.add_data(sh.EMPTY, clusters='Special Nodes'),
            'Empty dispatcher/workflow.', clusters='Special Nodes'
        )
        _add_explanation(
            dsp, dsp.add_data(sh.START, clusters='Special Nodes'),
            'Starting node. It identifies'
            '\nthe initial inputs.', clusters='Special Nodes'
        )
        _add_explanation(
            dsp, dsp.add_data(sh.END, clusters='Special Nodes'),
            'Ending node of SubDispatcherFunction.\n'
            'It collects the function\'s outputs.', clusters='Special Nodes'
        )
        _add_explanation(
            dsp, dsp.add_data(sh.SINK, clusters='Special Nodes'),
            'Sink node. It collects \n'
            'all unused outputs.', clusters='Special Nodes'
        )
        _add_explanation(
            dsp, dsp.add_data(sh.SELF, clusters='Special Nodes'),
            'Self node of the plotted dispatcher.\n'
            'It represents the dispatcher as data node.',
            clusters='Special Nodes'
        )
        _add_explanation(
            dsp, dsp.add_data(sh.PLOT, clusters='Special Nodes'),
            'Plot node. When invoked, it\n'
            'plots the dispatcher solution.', clusters='Special Nodes'
        )

        fun_kw = dict(inputs=[], outputs=[], clusters='Functions')

        class subdispatch:
            pass

        class mapdispatch:
            pass

        class subdispatchfunction:
            pass

        class subdispatchpipe:
            pass

        class dispatchpipe:
            pass

        _add_explanation(dsp, dsp.add_function(
            function_id='<function_id>(Function)',
            input_domain='Domain function `f(*inputs)`.',
            solution_domain='Domain function result.',
            weight='Distance weight coeff.',
            await_domain='Wait async for domain result? `<bool>`',
            await_result='Wait async for function result? `<bool>`',
            distance='Distance from `START` node.',
            started='Execution started time.',
            duration='Time elapsed to execute the function.',
            **fun_kw,
            **{'filter x': 'Filter function x used in the loop '
                           '`for f in filters: output = f(output)`.',
               'input_filter 0': 'Result of the function.',
               'output_filter x': 'Result of filters[x](`input_filter x` | '
                                  '`output_filter x-1`).'}
        ), clusters='Functions', description=(
            'Function node. The current one is a\n'
            'sample showing the main attributes.'
        ))

        _add_explanation(dsp, dsp.add_function(
            function_id='<function_id>(SubDispatch)',
            function=subdispatch(), **fun_kw
        ), clusters='Functions', description=(
            'SubDispatch node. It wraps\n'
            'a given Dispatcher into a function.\n'
            'Inputs are dictionaries {<node_id>: <value>}.'
        ))

        _add_explanation(dsp, dsp.add_function(
            function_id='<function_id>(MapDispatch)',
            function=mapdispatch(), **fun_kw
        ), clusters='Functions', description=(
            'MapDispatch node. It wraps and executes iteratively\n'
            'a given Dispatcher into a function.\n'
            'Hence, it behaves like a `map` function.'
        ))
        _add_explanation(dsp, dsp.add_function(
            function_id='<function_id>(SubDispatchFunction)',
            function=subdispatchfunction(), **fun_kw
        ), clusters='Functions', description=(
            'SubDispatchFunction node. It wraps and shrink\n'
            'a given Dispatcher into a function.\n'
            'Hence, it behaves like a function.'
        ))
        _add_explanation(dsp, dsp.add_function(
            function_id='<function_id>(SubDispatchPipe)',
            function=subdispatchpipe(), **fun_kw
        ), clusters='Functions', description=(
            'SubDispatchPipe node. It wraps and compiles\n'
            'a given Dispatcher into a function.\n'
            'Hence, it behaves like a function.'
        ))
        _add_explanation(dsp, dsp.add_function(
            function_id='<function_id>(DispatchPipe)',
            function=dispatchpipe(), **fun_kw
        ), clusters='Functions', description=(
            'DispatchPipe node. It behaves like a\n'
            'SubDispatchPipe node, but it overwrites\n'
            'its solution.'
        ))

        _add_explanation(dsp, dsp.add_function(
            function_id='<node_id>(Error)',
            clusters='Warnings and Errors', inputs=[], outputs=[],
            error='Error message.'
        ), clusters='Warnings and Errors', description=(
            'Node that raised an error during its execution.'
        ))
        d = dsp.nodes[_add_explanation(dsp, dsp.add_function(
            function_id='<node_id>(Warning)',
            clusters='Warnings and Errors', inputs=[], outputs=[]
        ), clusters='Warnings and Errors', description=(
            'Node that did not return all inputs/outputs.'
        ))]
        d['outputs'].append('missing outputs')
        d['inputs'].append('missing inputs')

        _add_explanation(dsp, dsp.add_dispatcher(
            clusters='Sub-dispatcher',
            dsp={},
            inputs={},
            outputs={},
            dsp_id='<dispatcher_id>(Dispatcher)',
            input_domain='Domain function `f(**inputs)`.',
            solution_domain='Domain function result.',
            weight='Distance weight coeff.',
            await_domain='Wait async for domain result? `<bool>`',
            distance='Distance from `START` node.',
        ), clusters='Sub-dispatcher', description=(
            'Sub-dispatcher node. It connects a given\n'
            'dispatcher to the current one. The current\n'
            'node one is a sample showing the main attributes.'
        ))

        dsp.add_data('<from>', clusters='Edges', graphviz=dict(style='invis'))
        dsp.add_function(
            function_id='<to>',
            clusters='Edges',
            inputs=['<from>'],
            outputs=[],
            inp_weight={'<from>': 'Edge distance.'},
            graphviz=dict(style='invis')
        )
        dsp.dmap['<from>']['<to>'].update(dict(
            label_type='label',
            inp_id='Index of input args.',
            out_id='Index of output list.',
            graphviz={
                'xlabel': 'This is an edge sample showing the main attributes.'
            }
        ))
        return dsp.plot(
            view=False,
            name='legend',
            body={'label': '""'},
            graph_attr={'rankdir': 'LR', 'id': 'graph'},
            node_data=(
                '-', 'default_values', 'wait_inputs',
                'await_result', 'distance', 'function', 'solution', 'weight',
                'remote_links', 'filter x', 'input_filter 0', 'output_filter x',
                'error', '*output', 'remote parent x', 'remote child x',
            ),
            node_function=(
                '-', 'await_domain', 'await_result', 'input_domain',
                'solution_domain', 'weight', 'filter x', 'input_filter 0',
                'output_filter x', 'error', 'missing_inputs_outputs',
                'distance', 'started', 'duration',
            )
        ).render(view=False, index=False, directory=tempfile.mkdtemp(), viz=viz)

    def render(self, context, *args, **kwargs):
        import threading
        import pkg_resources
        from jinja2 import PackageLoader
        pkg_dir = pkg_resources.resource_filename(__name__, '')
        fpath = osp.join(pkg_dir, 'templates', 'index.html')

        with open(fpath) as template:
            return jinja2_format(
                template.read(),
                {'tree': _sitemap2tree(self.sitemap, context),
                 'icicle': _sitemap2icicle(self.sitemap),
                 'pid': threading.get_ident(),
                 'folder': self._filename},
                loader=PackageLoader(__name__)
            )


def run_server(app, options):
    import threading
    MUTE_REQUESTS[threading.get_ident()] = getattr(app, 'mute', False)
    app.run(**options)


MUTE_REQUESTS = {}
logging.getLogger('werkzeug').addFilter(
    lambda r: not MUTE_REQUESTS.pop(r.thread, False)
)


def before_request(mute):
    import flask
    import threading
    from flask import request
    MUTE_REQUESTS[threading.get_ident()] = mute
    method = request.form.get('_method', '').upper()
    if method:
        request.environ['REQUEST_METHOD'] = method
        ctx = flask._request_ctx_stack.top
        ctx.url_adapter.default_method = method
        assert request.method == method


def _cleanup(files=None, rendered=None):
    if files is None and rendered is None:
        return 'Nothing to cleanup.'
    while files:
        fpath = files.pop()
        try:
            os.remove(fpath)
        except FileNotFoundError:
            pass
        try:
            os.removedirs(osp.dirname(fpath))
        except OSError:  # The directory is not empty.
            pass
    rendered and rendered.clear()
    return 'Cleaned up generated files by the server.'


def _shutdown_server():
    import flask
    func = flask.request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'


def basic_app(root_path, cleanup=None, shutdown=None, mute=True, **kwargs):
    import flask
    app = flask.Flask(root_path, root_path=root_path, **kwargs)
    app.before_request(functools.partial(before_request, mute))
    app.mute = mute

    cleanup, rule = (cleanup or _cleanup), '/cleanup'
    app.add_url_rule(rule, rule[1:], cleanup, methods=['DELETE'])

    shutdown, rule = (shutdown or _shutdown_server), '/shutdown'
    app.add_url_rule(rule, rule[1:], shutdown, methods=['DELETE'])
    return app


_repr_html = '''
<style> .sh-box {{ width: 100%; height: 500px }} </style>
<iframe id="{id}" class="sh-box" src="http://{host}:{port}/" allowfullscreen>
</iframe>
'''


class Site:
    def __init__(self, sitemap, host='localhost', port=0, delay=0.1, until=30,
                 run_options=None, **kwargs):
        self.sitemap = sitemap
        self.kwargs = kwargs
        self.host = host
        self.port = port
        self.shutdown = lambda: False
        self.delay = delay
        self.until = until
        self._html = os.environ.get("SCHEDULA_SITE_REPR_HTML", _repr_html)
        self.run_options = {} if run_options is None else run_options

    def __repr__(self):
        s = "%s(%s, " % (self.__class__.__name__, self.sitemap)
        s += "host='{}', port={}".format(self.host, self.port)
        for k, v in sorted(self.kwargs.items()):
            s += ', {}={}'.format(k, ("'%s'" % v) if isinstance(v, str) else v)
        return s + ')'

    def get_port(self, host=None, port=None, **kw):
        kw = kw.copy()
        kw['host'] = self.host = host or self.host
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, port or self.port))
        kw['port'] = self.port = sock.getsockname()[1]
        sock.close()
        return kw

    def _repr_html_(self):
        from IPython.display import HTML
        if not self.is_running:
            self.run()
        # noinspection PyTypeChecker
        kw = combine_dicts(os.environ, dict(
            id=id(self), host=self.host, port=self.port
        ))
        return HTML(self._html.format(**kw))._repr_html_()

    @property
    def url(self):
        return 'http://{}:{}'.format(self.host, self.port)

    def app(self):
        return self.sitemap.app(**self.kwargs)

    @staticmethod
    def shutdown_site(url):
        import requests
        try:
            requests.delete('%s/cleanup' % url)
            requests.delete('%s/shutdown' % url)
        except requests.exceptions.ConnectionError:
            return False
        return True

    def run(self, **options):
        self.shutdown()
        import threading
        options = combine_dicts(self.run_options, options)
        memo = os.environ.get("WERKZEUG_RUN_MAIN")
        try:
            os.environ["WERKZEUG_RUN_MAIN"] = "true"
            threading.Thread(
                target=run_server,
                args=(self.app(), self.get_port(**options))
            ).start()
            # noinspection PyArgumentList
            self.shutdown = weakref.finalize(self, self.shutdown_site, self.url)
            self.wait_server()
        finally:
            if memo is None:
                os.environ.pop("WERKZEUG_RUN_MAIN")
            else:
                os.environ["WERKZEUG_RUN_MAIN"] = memo

        return self

    @property
    def is_running(self):
        running = False
        if self.port:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:  # Tries to connect to the host.
                sock.connect((self.host, self.port))
                running = True
            except ConnectionRefusedError:
                pass
            finally:
                sock.close()
        return running

    def wait_server(self, elapsed=0):
        import time
        end = time.time() + self.until
        while not self.is_running:
            time.sleep(self.delay)
            if time.time() > end:
                msg = 'After %.3fs the server %s is down!' % (elapsed, self.url)
                raise ConnectionRefusedError(msg)


class SiteMap(collections.OrderedDict):
    site_folder = SiteFolder
    site_node = SiteNode
    site_index = SiteIndex
    site_viz = SiteViz
    _view = None
    options = {
        'digraph', 'node_styles', 'node_data', 'node_function', 'edge_data',
        'max_lines', 'max_width'
    }
    include_folders_as_filenames = True

    def __init__(self):
        super(SiteMap, self).__init__()
        if self._view is None:
            from .nodes import _DspPlot
            self._view = _DspPlot(None)._view
        self._nodes = []
        self.foldername = ''
        self.filenames = {'index', 'index.html', 'viz.js'}

    def __setitem__(self, key, value, *args, **kwargs):
        value.foldername = valid_filename(key, self.filenames, ext='')
        self.filenames.add(value.foldername)
        # noinspection PyArgumentList
        super(SiteMap, self).__setitem__(key, value, *args, **kwargs)

    def _repr_svg_(self):
        dot = list(self)[-1].dot()
        return dot.pipe(format='svg').decode(dot._encoding)

    @property
    def nodes(self):
        return sorted(self._nodes, key=lambda x: x.title)

    def rules(self, depth=-1, index=True, viz_js=False):
        filenames, rules = set(), []
        rules.extend(self._rules(depth=depth, filenames=filenames))
        for b, f in ((viz_js, self.site_viz), (index, self.site_index)):
            if b:
                rules.extend(list(update_filenames(f(self), filenames))[::-1])
        it = ((k, osp.join(*v).replace('\\', '/')) for k, v in reversed(rules))
        return collections.OrderedDict(it)

    def _rules(self, depth=-1, rule=(), filenames=None):
        if self.foldername:
            rule += self.foldername,
        if filenames is None:
            filenames = set()
        if self.include_folders_as_filenames:
            filenames.update(v.foldername for k, v in self.items())
        if depth != 0:
            depth -= 1
            for folder, smap in self.items():
                yield from smap._rules(rule=rule, depth=depth)
                for k, filename in update_filenames(folder, filenames):
                    yield k, rule + filename

        for node in self._nodes:
            for k, filename in update_filenames(node, filenames):
                yield k, rule + filename

    def _add_obj(self, obj, workflow=False, folder=None, **options):
        item = parent_func(obj)
        workflow &= not isinstance(item, NoSub)
        if workflow:
            item = self.get_sol_from(item)
            dsp, graph = item.dsp, item.workflow
        else:
            dsp = self.get_dsp_from(item)
            graph = dsp.dmap

        folder = self.site_folder(
            item, dsp, graph, obj, workflow=workflow, parent=folder, **options
        )
        folder.sitemap = smap = self[folder] = self.__class__()
        return smap, folder

    def add_items(self, item, workflow=False, depth=-1, folder=None, **options):
        opt = selector(self.options, self.__dict__, allow_miss=True)
        opt = combine_dicts(options, base=opt)
        smap, folder = self._add_obj(
            item, workflow=workflow, folder=folder, **opt
        )
        if depth > 0:
            depth -= 1
        site_node, append = self.site_node, smap._nodes.append
        add_items = functools.partial(
            smap.add_items, workflow=workflow, folder=folder, **opt
        )
        for node in itertools.chain(folder.nodes, folder.edges):
            links, node_id, node_title = node._links, node.node_id, node.title
            only_site_node = depth == 0 or node.type == 'data'
            for k, item in node.items():
                try:
                    if only_site_node:
                        raise ValueError
                    link = add_items(item, depth=depth, name=node_id)
                except ValueError:  # item is not a dsp object.
                    i = ''.join((node_title, k and '-' or '', k))
                    link = site_node(folder, i, item, item, node_id)
                    append(link)
                links[k] = link

        return folder

    @staticmethod
    def get_dsp_from(item):
        from ..sol import Solution
        from ...dispatcher import Dispatcher
        if isinstance(item, (Solution, SubDispatch)):
            return item.dsp
        elif isinstance(item, Dispatcher):
            return item
        raise ValueError('Type %s not supported.' % type(item).__name__)

    @staticmethod
    def get_sol_from(item):
        from ..sol import Solution
        from ...dispatcher import Dispatcher
        if isinstance(item, (Dispatcher, SubDispatch)):
            return item.solution
        elif isinstance(item, Solution):
            return item
        raise ValueError('Type %s not supported.' % type(item).__name__)

    def app(self, root_path=None, depth=-1, index=True, mute=True, viz_js=False,
            **kw):
        root_path = osp.abspath(root_path or tempfile.mkdtemp())
        generated_files, rendered = [], {}
        cleanup = functools.partial(_cleanup, generated_files, rendered)
        app = basic_app(root_path, cleanup=cleanup, mute=mute, **kw)
        context = self.rules(depth=depth, index=index, viz_js=viz_js)
        for (node, extra), filepath in context.items():
            func = functools.partial(
                site_view, app, node, context, generated_files, rendered, extra,
                viz_js
            )
            app.add_url_rule('/%s' % filepath, filepath, func)

        if context:
            app.add_url_rule('/', next(iter(context.values())))

        return app

    def site(self, root_path=None, depth=-1, index=True, view=False, **kw):
        site = Site(self, root_path=root_path, depth=depth, index=index, **kw)

        if view:
            site.run()
            # noinspection PyArgumentList
            self._view(site.url, 'html')

        return site

    def render(self, depth=-1, directory='static', view=False, index=True,
               viz=False, viz_js=False):
        context = self.rules(depth=depth, index=index, viz_js=viz_js)
        rendered = {}
        for node, extra in context:
            if not extra:
                cached_view(
                    node, directory, context, rendered, viz=viz or viz_js
                )
        fpath = osp.join(directory, next((
            v for (i, j), v in context.items()
            if not isinstance(i, NoView) and j is None
        ), ''))
        if view:
            # noinspection PyArgumentList
            self._view(fpath, osp.splitext(fpath)[1][1:])
        return fpath


def cached_view(node, directory, context, rendered, viz=False):
    n_id = node.view_id
    rend = {k: v for k, v in rendered.items() if k[0] == n_id}
    cnt = {(n_id, e): f for (n, e), f in context.items() if n == node}
    if rend and all(k in rend and osp.isfile(rend[k]) for k in cnt):
        for k, f in cnt.items():
            fpath = uncpath(osp.join(directory, f))
            os.makedirs(osp.dirname(fpath), exist_ok=True)
            parent, child = _compile_subs(rend[k], fpath)
            with open(fpath, 'w') as new_file:
                with open(rend[k]) as old_file:
                    for line in old_file:
                        new_file.write(child(parent(line)))
            rend[k] = fpath
    else:
        rend = node.view(
            osp.join(directory, context[(node, None)]), context=context, viz=viz
        )
        rendered.update(rend)
    return rend


def _compile_subs(o, n):
    bn, dn, st = osp.basename, osp.dirname, osp.splitext
    return _sub(bn(dn(o)), bn(dn(n))), _sub(st(bn(o))[0], st(bn(n))[0])


def _sub(old, new):
    p, repl = r'(href\s*=\s*"[^"]*)(/%s)((.|/)[^"]*")' % old, r'\1/%s\3' % new
    return functools.partial(regex.compile(p, regex.IGNORECASE).sub, repl)
