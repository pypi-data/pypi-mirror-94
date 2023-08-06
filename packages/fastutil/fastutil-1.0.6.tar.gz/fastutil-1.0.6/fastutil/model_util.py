import functools
import os

from loguru import logger
from fastutil import git_util


def log_module_var(module):
    print('param-----------------------------------------------param')
    param_list = []
    if isinstance(module, str):
        with open(module) as f:
            for line in f:
                print(line)
                param_list.append(line)
    else:
        for k, v in vars(module).items():
            if k.startswith('__'):
                continue
            if isinstance(v, (int, float, bool, str, dict, tuple, list, set)):
                print('{}:{}'.format(k, v))
                param_list.append('{}:{}'.format(k, v))
    print('param-----------------------------------------------param')
    return param_list


def log_record(config_module=None, config_file=None, save_dir=None, check_commit=True):
    """
    记录配置文件到日志和保存目录，创建或清理保存的目录
    """

    def wrapper(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            if check_commit and not git_util.is_git_commit():
                raise Exception('git is not committed'.format(save_dir))
            if os.path.exists(save_dir) and len(os.listdir(save_dir)) > 0:
                raise Exception('save_dir:{} is not empty'.format(save_dir))
            logger.info('save_dir:{}'.format(save_dir))
            os.mkdir(save_dir)
            try:
                param_list = log_module_var(config_module or config_file)
                func(*args, **kwargs)
                with open(os.path.join(save_dir, 'param.txt'), 'w') as param_f:
                    param_f.write('\n'.join(param_list))
            except Exception as ex:
                if len(os.listdir(save_dir)) == 0:
                    os.removedirs(save_dir)
                raise ex

        return wrapped

    return wrapper
