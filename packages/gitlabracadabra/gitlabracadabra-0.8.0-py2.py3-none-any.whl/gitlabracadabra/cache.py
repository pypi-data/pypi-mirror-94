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


from gitlab.exceptions import GitlabGetError

import gitlabracadabra.manager


class GroupCache(object):
    """Groups mapping

    indexed by id and full path.
    """
    _GROUPS_PATH2ID = {}
    _GROUPS_ID2PATH = {}

    """Map group id and full path
    """
    @classmethod
    def map_group(cls, group_id, group_full_path):
        cls._GROUPS_ID2PATH[group_id] = group_full_path
        cls._GROUPS_PATH2ID[group_full_path] = group_id

    """Get group full path from id
    """
    @classmethod
    def get_full_path_from_id(cls, group_id):
        if group_id not in cls._GROUPS_ID2PATH:
            try:
                obj_manager = gitlabracadabra.manager.get_manager().groups
                group = obj_manager.get(group_id)
                cls._GROUPS_ID2PATH[group.id] = group.full_path
                cls._GROUPS_PATH2ID[group.full_path] = group.id
            except GitlabGetError as e:
                if e.response_code != 404:
                    pass
                cls._GROUPS_ID2PATH[group_id] = None
        return cls._GROUPS_ID2PATH[group_id]

    """Get group id from full path
    """
    @classmethod
    def get_id_from_full_path(cls, group_full_path):
        if group_full_path not in cls._GROUPS_PATH2ID:
            try:
                obj_manager = gitlabracadabra.manager.get_manager().groups
                group = obj_manager.get(group_full_path)
                cls._GROUPS_ID2PATH[group.id] = group.full_path
                cls._GROUPS_PATH2ID[group.full_path] = group.id
            except GitlabGetError as e:
                if e.response_code != 404:
                    pass
                cls._GROUPS_PATH2ID[group_full_path] = None
        return cls._GROUPS_PATH2ID[group_full_path]
