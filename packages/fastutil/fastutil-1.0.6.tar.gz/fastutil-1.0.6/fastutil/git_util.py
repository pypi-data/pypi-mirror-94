import datetime as dt
import subprocess

import loguru


def is_git_commit():
    status, res = subprocess.getstatusoutput('git status')
    if status == 0 and 'nothing to commit' in res:
        return True
    return False


def get_git_commit():
    status, res = subprocess.getstatusoutput('git rev-parse HEAD')
    if status != 0:
        loguru.logger.warning('git status return:{},msg:{}'.format(status, res))
        return -1
    if 'Not a git repository' in res:
        loguru.logger.warning('git status return:{},msg:{}'.format(status, res))
        return -1
    return res


def get_ver_id():
    commit_res = get_git_commit()
    if commit_res == -1:
        raise Exception('ver id is None')
    return commit_res[:8]


def get_date_ver_id():
    commit_res = get_git_commit()
    now_date = dt.datetime.now().strftime('%Y%m%d_%H%M%S')
    if commit_res == -1:
        return now_date
    _date_ver_id = now_date + '_' + commit_res[:8]
    return _date_ver_id


def ver_id():
    print(get_ver_id())


def date_ver_id():
    print(get_date_ver_id())
