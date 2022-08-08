# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 xiao zhiguo <xiaozhiguo@uniontech.com>
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

from .base_config import BaseConfig


class ManualConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        self.ignored_dir.append('src/web_dist/')
        self.ignored_dir.append('src/web/toSearchMd/common')
        self.ignored_dir.append('debian/missing-sources')
        self.ignored_file_suff.append('json')
