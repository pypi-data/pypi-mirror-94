from collections import namedtuple
from io import StringIO
import csv
import re
import subprocess

from docutils import nodes


_Cfg = namedtuple('Cfg', ['cmd', 'index_path', 'src_root'])
_Tag = namedtuple('Tag', ['name', 'path', 'line', 'col', 'attrs'])

tagpattern = re.compile('^(.*):([0-9]+)\.([0-9]+)-([0-9]+)$')


# [# test-tag #]


class ClutterException(Exception):
    pass


def _cfg_from_app(appcfg):
    return _Cfg(
        cmd=appcfg.clutter_cmd,
        index_path=appcfg.clutter_index_path,
        src_root=appcfg.clutter_src_root,
    )


def _search(text, cfg, opts=[]):
    cmd = [cfg.cmd, '--index-path', cfg.index_path] + opts + ['s', text]

    proc = subprocess.run(
        cmd,
        cwd=cfg.src_root,
        capture_output=True,
    )

    stderr = proc.stderr.decode('utf-8').strip()

    if proc.returncode != 0:
        raise ClutterException(f'exec {cmd} -> {proc.returncode}\n{stderr}')

    if stderr:
        # TODO: warn
        pass

    stdout = proc.stdout.decode('utf-8')

    r = csv.reader(StringIO(stdout), delimiter=' ')

    tags = []

    for fs in r:
        if len(fs) < 2:
            # TODO: warn
            continue

        name, loc = fs[0], fs[1]

        m = tagpattern.match(loc)
        if not m:
            # TODO: warn
            continue

        fn, lnum, col, endcol = m.groups()

        tags.append(_Tag(name=name, path=fn, line=lnum, col=col, attrs=fs[2:]))

    return tags


def _link_node(title, uri):
    ref = nodes.reference('', '', internal=False, refuri=uri)
    title = nodes.inline('', title)
    ref.append(title)
    return ref


def _make_clutter_role(app):
    def role(role, rawtext, text, lineno, inliner, options={}, content=[]):
        if not app.config.clutter_repo_url_format:
            raise ClutterException('clutter_repo_url_format must be configured')

        tags = _search(text, _cfg_from_app(app.config))

        if not tags:
            raise ClutterException("no tags found")
        elif len(tags) > 1:
            raise ClutterException("multiple tags found")

        tag = tags[0]

        href = app.config.clutter_repo_url_format.format(tag=tag)

        return [_link_node(tag.name, href)], []

    return role


def github_repo_url_format(org, repo, branch='main', base='https://github.com'):
    rest = '{tag.path}#L{tag.line}'
    return f'{base}/{org}/{repo}/blob/{branch}/{rest}'


def setup(app):
    app.add_config_value('clutter_index_path', '', True)
    app.add_config_value('clutter_cmd', 'clutter', True)
    app.add_config_value('clutter_src_root', '.', True)
    app.add_config_value('clutter_repo_url_format', None, True)

    app.add_role('clutter', _make_clutter_role(app))

    return {
        'version': '0.0.2',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }

