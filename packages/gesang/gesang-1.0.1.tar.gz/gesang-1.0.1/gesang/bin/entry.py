from gesang.command.manage import CommandManagement
import sys


def execute_from_argv():
    """
    入口方法
    :return:
    """
    return CommandManagement(argv=sys.argv).execute_from_argv()
