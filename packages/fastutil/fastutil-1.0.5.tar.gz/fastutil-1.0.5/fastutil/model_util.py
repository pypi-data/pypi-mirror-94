import functools
import subprocess
from loguru import logger
import os
import datetime as dt


def log_module_var(module, ver_dir):
    logger.info('param-----------------------------------------------param')
    param_f = open(os.path.join(ver_dir, 'param.txt'), 'w')
    if isinstance(module, str):
        with open(module) as f:
            for line in f:
                logger.info(line)
                param_f.write(line + '\n')
    else:
        for k, v in vars(module).items():
            if k.startswith('__'):
                continue
            if isinstance(v, (int, float, bool, str, dict, tuple, list, set)):
                logger.info('{}:{}'.format(k, v))
                param_f.write('{}:{}\n'.format(k, v))
    param_f.close()
    logger.info('param-----------------------------------------------param')


def is_git_commit():
    status, res = subprocess.getstatusoutput('git status')
    if status == 0 and 'working tree clean' in res:
        return True
    return False


def get_git_commit():
    status, res = subprocess.getstatusoutput('git rev-parse HEAD')
    if status != 0:
        logger.warning('git status return:{},msg:{}'.format(status, res))
        return -1
    if 'Not a git repository' in res:
        logger.warning('git status return:{},msg:{}'.format(status, res))
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


def log_record(config_module=None, config_file=None, save_dir=None, check_commit=True):
    """
    记录配置文件到日志和保存目录，创建或清理保存的目录
    """

    def wrapper(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            if check_commit and not is_git_commit():
                raise Exception('git is not committed'.format(save_dir))
            if os.path.exists(save_dir):
                raise Exception('save_dir:{} is exist'.format(save_dir))
            logger.info('save_dir:{}'.format(save_dir))
            os.mkdir(save_dir)
            log_module_var(config_module or config_file, save_dir)
            try:
                func(*args, **kwargs)
            except Exception as ex:
                if len(os.listdir(save_dir)) <= 1:
                    os.removedirs(save_dir)
                raise ex

        return wrapped

    return wrapper
