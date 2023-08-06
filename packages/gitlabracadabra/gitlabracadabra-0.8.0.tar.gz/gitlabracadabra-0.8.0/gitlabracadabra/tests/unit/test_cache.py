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

from unittest import TestCase

from gitlab import Gitlab

import gitlabracadabra.manager
from gitlabracadabra.cache import GroupCache
from gitlabracadabra.tests.utils import my_vcr


class TestGroupCache(TestCase):
    def setUp(self):
        gitlabracadabra.manager._gitlab = Gitlab(  # noqa: S106
            'http://localhost',
            private_token='DKkdC5JmKWWZgXZGzg83',
        )

    def tearDown(self):
        gitlabracadabra.manager._gitlab = None

    @my_vcr.use_cassette
    def test_get_id_from_full_path(self, cass):
        # Clean up
        GroupCache._GROUPS_PATH2ID = {}
        GroupCache._GROUPS_ID2PATH = {}
        ret = GroupCache.get_id_from_full_path('test/group_mapping')
        self.assertEqual(ret, 9)
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_get_full_path_from_id(self, cass):
        # Clean up
        GroupCache._GROUPS_PATH2ID = {}
        GroupCache._GROUPS_ID2PATH = {}
        ret = GroupCache.get_full_path_from_id(9)
        self.assertEqual(ret, 'test/group_mapping')
        self.assertTrue(cass.all_played)
