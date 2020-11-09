# gitlab_code_stats
A python script for counting gitlab code with python-gitlab

# Environment
```
sudo apt-get install python3 python3-pip
pip3 install argparse python-gitlab openpyxl
```

# Usage
```
$ python3 gitlab_code_stats_thread.py -h
usage: gitlab_code_stats_thread.py [-v] [-h] [-b BRANCH] [--since SINCE]
                                   [--until UNTIL]

A python script for counting gitlab code by xiaozhiguo@uniontech.com.

optional arguments:
  -v, --version         show program's version number and exit
  -h, --help
  -b BRANCH, --branch BRANCH
                        Gitlab branch you want to count, default is master.
  --since SINCE         Date to start counting, just like YYYY-MM-DD, default
                        is at the begin of project built.
  --until UNTIL         Date to stop counting, just like YYYY-MM-DD, default
                        is today.
```
