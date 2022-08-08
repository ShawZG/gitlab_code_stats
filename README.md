# gitlab_code_stats

A python script for counting gitlab code with python-gitlab

# Environment
```
sudo apt-get install python3 python3-pip
pip3 install argparse python-gitlab openpyxl bs4
```

# Usage
1. Config your gitlab private access tokens and github url in function CommitWebParse.\_\_init\_\_ which in file commit_web_parse.py.

[https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html#personal-access-tokens](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html#personal-access-tokens)

```python
class CommitWebParse:
    def __init__(self, branch: str = 'master', since: str = None, until: str = None):
        self._gitlab_url: str = "gitlab_url"
        self._gitlab_access_token: str = "private_access_tokens"

```

2. Save your gitlab account in function CommitWebParse._login_gitlab which in file commit_web_parse.py. 
```python
class CommitWebParse:
    def _login_gitlab(self):
        CommitWebParse.login_session = session()
        CommitWebParse.login_data['utf8'] = '✓'
        CommitWebParse.login_data['username'] = 'ut000591'
        CommitWebParse.login_data['password'] = 'your_ldap_password'
        CommitWebParse.login_data['authenticity_token'] = ''
```

3. Make sure the dirs, files or commiters that you do not want to stats, and this is an optional operation. You can add the config in base cofig or specified project config.

```python
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
            
class EditorConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        self.ignored_dir.append('third/')
        self.ignored_dir.append('encodes/include/')
```

4. Run the python script followed below help and a excel file will be generated in the directory where the script is run.

```python
$ ~/workspace/gitlab_code_stats$ python3 gitlab_project_stats.py -h
usage: gitlab_project_stats.py [-v] [-h] [-p PROJECT] [-b BRANCH]
                               [--since SINCE] [--until UNTIL]

A python script for counting gitlab code by xiaozhiguo@uniontech.com.

optional arguments:
  -v, --version         show program's version number and exit.
  -h, --help
  -p PROJECT, --project PROJECT
                        One gitlab project you want to count.
  -b BRANCH, --branch BRANCH
                        Gitlab branch you want to count, default is master.
  --since SINCE         Date to start counting, just like YYYY-MM-DD, default
                        is at the begin of project built.
  --until UNTIL         Date to stop counting, excluding the deadline, just
                        like YYYY-MM-DD, default is today.
```
