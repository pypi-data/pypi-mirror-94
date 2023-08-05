import os
import argparse


def kill_task():
    parser = argparse.ArgumentParser(description='使用示例：taskkill train.py')
    parser.add_argument('signal', default='', help='信号')
    parser.add_argument('name', nargs='*', help='进程grep标记')
    args = parser.parse_args()
    name = ' '.join(args.name)
    cmd = """
    if ps aux | grep '%s' |grep -v 'grep';then
        ps aux | grep '%s' |grep -v 'grep' | awk '{print $2}' | xargs kill %s
    fi
    """ % (name, name, args.signal)
    os.system(cmd)
