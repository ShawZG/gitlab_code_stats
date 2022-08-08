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

from commit_web_parse import CommitWebParse
from projectconfig.config_factory import ConfigFactory


class GitLabProjectManager:
    """
    Args:
        project: 指定统计的项目
        branch(str): 设置统计项目的分支，默认为master
        since(str): 设置统计的开始时间，格式YYYY-MM-DD
        until(str): 设置统计的结束时间，不包括该时间，格式YYYY-MM-DD
    """
    def __init__(self, project=None, branch: str = None, since: str = None, until: str = None):
        self._project = project
        self._branch: str = branch
        self._since: str = since
        self._until: str = until
        self._project_authors: set = set()
        self._project_commit_data: list = []
        self._config = ConfigFactory.get_config(self._project.name)

    def _filter_one_commit(self, author_email: str, commit_files: list):
        """
        根据对应项目的配置self._config，过滤掉不需要统计的文件

        Args:
            author_email: 提交人的邮箱
            commit_files: 提交的文件
        """
        print('================================================================================')
        print("project config:", self._config)
        for accepted_email in self._config.accepted_email:
            if not (accepted_email in author_email):
                continue

            author_commit: dict = {'author_email': author_email, 'add': 0, 'del': 0}
            for commit_file in commit_files:
                file_result = [ignored_file_suff in commit_file['file'] for ignored_file_suff in self._config.ignored_file_suff]
                if any(file_result):
                    print('abandon commit file', commit_file['file'], commit_file['add'], commit_file['del'])
                    continue
                dir_result = [ignored_dir in commit_file['file'] for ignored_dir in self._config.ignored_dir]
                if any(dir_result):
                    print('abandon commit file', commit_file['file'], commit_file['add'], commit_file['del'])
                    continue

                print("accept commit file", commit_file['file'], commit_file['add'], commit_file['del'])
                author_commit['add'] += commit_file['add']
                author_commit['del'] += commit_file['del']

            print("add commit", author_commit)
            self._project_commit_data.append(author_commit)

    def _get_project_commit(self):
        """
        获取项目指定分支，指定时间内的所有提交信息
        """
        print("================================================================================")
        print("project: ", self._project.web_url)
        print("branch:  ", self._branch)
        print("since:   ", self._since)
        print("until:   ", self._until)

        commits = self._project.commits.list(all=True, query_parameters={'since': self._since, 'until': self._until, 'ref_name': self._branch})
        print("================================================================================")
        if len(commits) is 0:
            print("there is no commit, please check the since/until date you input just now.".format(len(commits)))
        else:
            print("there are {} commit(s) needed to be parsed, please wait for moments.".format(len(commits)))

        for commit in commits:
            if ('Merge' in commit.title) or ('Merge' in commit.message):
                continue
            commit_detail = self._project.commits.get(commit.id)
            self._project_authors.add(commit_detail.author_email)
            # commit_file['file']:str
            # commit_file['add']:int
            # commit_file['del']:int
            commit_files: list = CommitWebParse.parse_commit_page(commit_detail.web_url)
            self._filter_one_commit(commit_detail.author_email, commit_files)

    def _calculate_project_commit(self):
        """
        处理经过_filter_one_commit过滤后的数据
        Returns: 项目指定分支的统计数据
        """
        committer_statistics_code: dict = {}
        committer_statistics_codes: list = []
        for author_email in self._project_authors:
            committer_statistics_code[author_email] = {"commits": 0, "add": 0, "del": 0, "total": 0}
        for author_commit in self._project_commit_data:
            author = author_commit['author_email']
            committer_statistics_code[author]["commits"] += 1
            committer_statistics_code[author]["add"] += author_commit["add"]
            committer_statistics_code[author]["del"] += author_commit["del"]
            committer_statistics_code[author]["total"] += (author_commit["add"] + author_commit["del"])
        # 整理数据
        for author_email in self._project_authors:
            tmp_committer_statistics_code: dict = dict()
            tmp_committer_statistics_code['project'] = self._project.web_url
            tmp_committer_statistics_code['branch'] = self._branch
            tmp_committer_statistics_code['author_email'] = author_email
            tmp_committer_statistics_code['commits'] = committer_statistics_code[author_email]["commits"]
            tmp_committer_statistics_code['add'] = committer_statistics_code[author_email]["add"]
            tmp_committer_statistics_code["del"] = committer_statistics_code[author_email]["del"]
            tmp_committer_statistics_code["total"] = committer_statistics_code[author_email]["total"]
            committer_statistics_codes.append(tmp_committer_statistics_code)
        print('================================================================================')
        for author_commit_code in committer_statistics_codes:
            print(author_commit_code)
        return committer_statistics_codes

    def calculate_project_branch_commit_data(self):
        """
        统计项目指定分支的提交数据入口函数
        """
        self._get_project_commit()
        project_commit_stats_data: list = self._calculate_project_commit()
        return project_commit_stats_data
