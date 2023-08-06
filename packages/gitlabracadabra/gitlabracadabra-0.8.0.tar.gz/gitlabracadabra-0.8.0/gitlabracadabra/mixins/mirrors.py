#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2020 Mathieu Parent <math.parent@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import os
import re
import subprocess  # noqa: S404
from urllib.request import getproxies, proxy_bypass
try:
    from urllib import quote, urlparse  # Python 2.X
except ImportError:
    from urllib.parse import quote, urlparse  # Python 3+

from pygit2 import (
    GIT_FETCH_PRUNE,
    GitError,
    LIBGIT2_VER,
    Passthrough,
    RemoteCallbacks,
    Repository,
    UserPass,
    init_repository,
)

import gitlabracadabra.manager
import gitlabracadabra.utils

logger = logging.getLogger(__name__)


class PyGit2Callbacks(RemoteCallbacks):
    def __init__(self, use_token):
        self._use_token = use_token

    """credentials()

    Authenticate using OAuth2 token
    """
    def credentials(self, url, username_from_url, allowed_types):
        if self._use_token:
            mgr = gitlabracadabra.manager.get_manager()
            return UserPass('oauth2', mgr.private_token)
        else:
            raise Passthrough


class MirrorsMixin(object):
    """_init_repo()

    Init the cache repository
    """
    def _init_repo(self):
        repo_dir = gitlabracadabra.utils.gitlabracadabra_cache_dir(quote(self.web_url(), safe=''))
        if not os.path.isdir(repo_dir):
            logger.debug('[%s] Creating cache repository in %s',
                                    self._name, repo_dir)
            self._repo = init_repository(repo_dir, bare=True)
        else:
            self._repo = Repository(repo_dir)
        try:
            self._repo.remotes['gitlab']
        except KeyError:
            self._repo.remotes.create('gitlab', self.web_url(), '+refs/heads/*:refs/remotes/gitlab/heads/*')
            self._repo.remotes.add_fetch('gitlab', '+refs/tags/*:refs/remotes/gitlab/tags/*')
            self._repo.remotes.add_push('gitlab', '+refs/heads/*:refs/heads/*')
            self._repo.remotes.add_push('gitlab', '+refs/tags/*:refs/tags/*')
            self._repo.config['remote.gitlab.mirror'] = True

    """_fetch_remote()

    Fetch the repo with the given name
    """
    def _fetch_remote(self, name):
        url = self._repo.config['remote.{name}.url'.format(name=name)]
        libgit2_workaround = False
        if url.startswith('https://') and LIBGIT2_VER < (0, 28, 0):
            try:
                http_proxy = self._repo.config['http.proxy']
            except KeyError:
                http_proxy = None
            try:
                http_proxy = self._repo.config['remote.{name}.proxy'.format(name=name)]
            except KeyError:
                pass
            if http_proxy is None:  # '' being explicitly disabled
                proxies = getproxies()
                parsed = urlparse(url)
                http_proxy = proxies.get(parsed.scheme) or proxies.get('any')
                if proxy_bypass(parsed.hostname):
                    http_proxy = None
            if http_proxy:
                libgit2_workaround = True
        if libgit2_workaround:
            # libgit2 >= 0.28 required for proper HTTP proxy support
            # https://github.com/libgit2/libgit2/pulls/4870
            # https://github.com/libgit2/libgit2/pulls/5052
            logger.warning('[%s] Using git command to fetch remote %s', self._name, name)
            subprocess.run(['git', 'fetch', '--quiet', '--prune', name], cwd=self._repo.path)  # noqa: S603,S607
        else:
            pygit2_callbacks = PyGit2Callbacks(use_token=name == 'gitlab')
            self._repo.remotes[name].fetch(refspecs=self._repo.remotes[name].fetch_refspecs,
                                           callbacks=pygit2_callbacks, prune=GIT_FETCH_PRUNE)

    """_push_remote()

    Push to the repo with the given name
    """
    def _push_remote(self, name, refs):
        pygit2_callbacks = PyGit2Callbacks(use_token=name == 'gitlab')
        try:
            self._repo.remotes[name].push(refs, callbacks=pygit2_callbacks)
        except GitError as e:
            logger.error('[%s] Unable to push remote=%s refs=%s: %s',  # noqa: G200
                         self._name, name, ','.join(refs), e)

    """_sync_ref()

    Synchronize the given branch or tag
    """
    def _sync_ref(self, mirror, ref, skip_ci, dry_run):
        if ref.name.startswith('refs/heads/'):
            ref_type = 'head'
            ref_type_human = 'branch'
            ref_type_human_plural = 'branches'
            shorthand = ref.name[11:]
        elif ref.name.startswith('refs/tags/'):
            ref_type = 'tag'
            ref_type_human = 'tag'
            ref_type_human_plural = 'tags'
            shorthand = ref.name[10:]
        else:
            return

        # Ref mapping
        dest_shortand = shorthand
        if ref_type_human_plural in mirror:
            dest_shortand = None
            for mapping in mirror[ref_type_human_plural]:
                from_param = mapping.get('from', '')
                if from_param.startswith('/'):
                    flags_str = from_param[from_param.rindex('/') + 1:]
                    flags = 0
                    for flag in flags_str:
                        if flag == 'i':
                            flags |= re.IGNORECASE
                        else:
                            logger.warning('[%s] %s %s. Invalid regular expression flag %s in %s',
                                           self._name, mirror['url'], ref_type_human_plural, flag, from_param)
                    try:
                        from_regex = re.compile('^' + from_param[1:from_param.rindex('/')] + '$', flags)
                        match = from_regex.match(shorthand)
                        if match:
                            to_param = mapping.get('to', shorthand)
                            dest_shortand = match.expand(to_param)
                            break
                    except re.error as e:
                        logger.info('[%s] %s %s. Invalid regular expression: %s',  # noqa: G200
                                    self._name, mirror['url'], ref_type_human_plural, from_param, str(e))
                elif from_param == shorthand:
                    dest_shortand = mapping.get('to', shorthand)
                    break

        if dest_shortand is None:
            return

        if skip_ci:
            # FIXME Ignored by libgit2/PyGit2
            # https://github.com/libgit2/libgit2/issues/5335
            self._repo.config['push.pushOption'] = 'ci.skip'
        else:
            self._repo.config['push.pushOption'] = ''

        pull_commit = ref.peel().id
        gitlab_ref = self._repo.references.get('refs/remotes/gitlab/{ref_type}s/{ref}'.format(ref_type=ref_type,
                                                                                              ref=dest_shortand))
        try:
            gitlab_commit = gitlab_ref.peel().id
        except AttributeError:
            gitlab_commit = None
        if pull_commit != gitlab_commit:
            if dry_run:
                logger.info('[%s] %s NOT Pushing %s %s to %s: %s -> %s (dry-run)',
                            self._name, mirror['url'],
                            ref_type_human, shorthand, dest_shortand,
                            gitlab_commit, str(pull_commit))
            else:
                logger.info('[%s] %s Pushing %s %s to %s: %s -> %s',
                            self._name, mirror['url'],
                            ref_type_human, shorthand, dest_shortand,
                            gitlab_commit, str(pull_commit))
                self._push_remote('gitlab', [ref.name + ':' + 'refs/{ref_type}s/{ref}'.format(ref_type=ref_type,
                                                                                              ref=dest_shortand)])

    """_pull_mirror()

    Pull from the given mirror and push
    """
    def _pull_mirror(self, mirror, direction, skip_ci, dry_run):
        try:
            self._repo.remotes['pull']
        except KeyError:
            self._repo.remotes.create('pull', mirror['url'], '+refs/heads/*:refs/heads/*')
            self._repo.remotes.add_fetch('pull', '+refs/tags/*:refs/tags/*')
            self._repo.config['remote.pull.mirror'] = True
        self._fetch_remote('pull')
        for ref in self._repo.references.objects:
            self._sync_ref(mirror, ref, skip_ci, dry_run)

    """_process_mirrors()

    Process the mirrors param.
    """
    def _process_mirrors(self, param_name, param_value, dry_run=False, skip_save=False):
        assert param_name == 'mirrors'  # noqa: S101
        assert not skip_save  # noqa: S101

        pull_mirror_count = 0
        self._init_repo()
        self._fetch_remote('gitlab')
        for mirror in param_value:
            direction = mirror.get('direction', 'pull')
            skip_ci = mirror.get('skip_ci', True)
            if direction == 'pull':
                if pull_mirror_count > 0:
                    logger.warning('[%s] NOT Pulling mirror: %s (Only first pull mirror is processed)',
                                   self._name, mirror['url'])
                    continue
                self._pull_mirror(mirror, direction, skip_ci, dry_run)
                pull_mirror_count += 1
            else:
                logger.warning('[%s] NOT Push mirror: %s (Not supported yet)',
                                self._name, mirror['url'])
                continue
