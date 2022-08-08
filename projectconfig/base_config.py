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

class BaseConfig(object):
    """
    ignored_file_suff: 需要忽略的文件后缀名
    ignored_dir: 需要忽略的文件夹
    accepted_email: 提交人白名单，忽略所有非匹配的邮箱后缀
    """
    def __init__(self):
        self.ignored_file_suff: list = ['.ts', '.md', 'svg', 'qm']
        self.ignored_dir: list = ['third_party/', 'googletest/']
        self.accepted_email: list = ['@uniontech.com']


if __name__ == '__main__':
    pass
