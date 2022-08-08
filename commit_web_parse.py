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

from requests import session
from bs4 import BeautifulSoup, SoupStrainer


class CommitWebParse:
    is_logged_in: bool = False
    login_session = None
    login_data: dict = dict()

    def __init__(self):
        self._gitlab_access_token_url = ''
        self._gitlab_login_url_callback = ''

    def _login_gitlab(self):
        CommitWebParse.login_session = session()
        CommitWebParse.login_data['utf8'] = '✓'
        CommitWebParse.login_data['username'] = ''
        CommitWebParse.login_data['password'] = ''
        CommitWebParse.login_data['authenticity_token'] = ''

        # 通过访问_gitlab_access_token_url，获取到session
        # 利用此session登陆_gitlab_login_url_callback，更新token
        # 完成后，后续爬虫时，可以利用这个session直接访问commit_url
        token_page = CommitWebParse.login_session.get(url=self._gitlab_access_token_url)
        if token_page.ok:
            html = BeautifulSoup(token_page.text, 'html.parser')
            authenticity_token = html.find_all(name='input', attrs={'type': 'hidden', 'name': "authenticity_token"})

            CommitWebParse.login_data['authenticity_token'] = authenticity_token[0]['value']
            login_page = CommitWebParse.login_session.post(url=self._gitlab_login_url_callback, data=CommitWebParse.login_data)

            if login_page.ok:
                login_token_page = BeautifulSoup(login_page.text, "html.parser")
                private_token = login_token_page.find_all(name='input', attrs={'type': 'hidden', 'name': "authenticity_token"})

                if private_token:
                    CommitWebParse.login_session.headers.update({'Private-Token': private_token[0]['value']})
                    CommitWebParse.is_logged_in = True
                    return True
        return False

    @classmethod
    def parse_commit_page(cls, commit_url: str = None):
        if not CommitWebParse.is_logged_in:
            print("================================================================================")
            login_result: bool = cls._login_gitlab(cls())
            if not login_result:
                print('login failure', "https://gitlabnj.uniontech.com/users/auth/ldapmain/callback")
                raise BaseException
            print('login successfully', "https://gitlabnj.uniontech.com/users/auth/ldapmain/callback")
        commit_page = CommitWebParse.login_session.get(url=commit_url)
        # 加快爬取速度，只分析关注部分
        parse_only = SoupStrainer('div', attrs={'class': 'dropdown-content'})
        soup = BeautifulSoup(commit_page.text, 'html.parser', parse_only=parse_only)
        table_tags = soup.find_all(name="a", attrs={'class': 'diff-changed-file'}, recursive=True)

        print("================================================================================")
        print("parse commit url:", commit_url)
        commit_files: list = []
        for table_tag in table_tags:
            changed_file_name = table_tag.find(name="strong", attrs={'class': 'diff-changed-file-name'})
            changed_file_add = table_tag.find(name='span', attrs={'class': 'cgreen'})
            changed_file_del = table_tag.find(name='span', attrs={'class': 'cred'})
            # print(table_tag)

            commit_file: dict = dict()
            commit_file['file'] = changed_file_name.text.strip()
            commit_file['add'] = int(changed_file_add.text)
            commit_file['del'] = abs(int(changed_file_del.text))
            print(commit_file)
            commit_files.append(commit_file)

        return commit_files


# if __name__ == "__main__":
#     test_url1: str = "https://gitlabnj.uniontech.com/nanjing/deepin-terminal/-/commit/9e05b6d1bc4976215d4bec9356f078d1e466ac76"
#     test_url2: str = 'https://gitlabnj.uniontech.com/nanjing/deepin_reader/-/commit/77d0e029293dcf979e96cd91e0466f86a088131a'
#     # commit_parse = CommitWebParse()
#     commit1 = CommitWebParse.parse_commit_page(commit_url=test_url1)
#     commit2 = CommitWebParse.parse_commit_page(commit_url=test_url2)
