import sys
import os
import pkgutil
import functools
from importlib import import_module
from gesang.command import base


def find_commands(command_dir):
    """
    Search all command in dir command_dir

    :param command_dir: Command module dir
    """
    command_dir = os.path.join(command_dir, 'sub_commands')
    return [name for _, name, is_pkg in pkgutil.iter_modules([command_dir])
            if not is_pkg and not name.startswith('_')]


def load_command_class(app_name, name):
    """
    Load sub command class

    :param app_name: [str] App module name
    :param name: [str] Sub command module name
    """
    module = import_module('%s.command.sub_commands.%s' % (app_name, name))
    return module.Command()


@functools.lru_cache(maxsize=None)
def get_commands():
    commands = {name: "gesang" for name in find_commands(os.path.dirname(os.path.abspath(__file__)))}
    return commands


class CommandManagement:

    def __init__(self, argv):
        self.argv = argv

    def _print_help(self):
        """
        Print help
        :return:
        """
        sys.stdout.write("\n\rUsage: frwork [sub_command] [sub command options]")
        sys.stdout.write("\n\rIf check each sub command usage, please use frwork sub_command -h")
        sys.stdout.write("\n\rAvailable sub commands:")
        sub_commands = get_commands()
        for sub_command in sub_commands:
            sys.stdout.write(f"\n\r{sub_command}")
        sys.stdout.write("\n\r")

    def execute_from_argv(self):
        """
        Execute command from system command line arguments
        :return:
        """
        prog_name = self.argv[0]
        try:
            sub_command = self.argv[1]
            app_name = get_commands()[sub_command]
            sub_command_ins = load_command_class(app_name, sub_command)
            if isinstance(sub_command_ins, base.BaseCommand):
                sub_command_ins.run_from_argv(prog_name=prog_name, sub_command=sub_command, argv=self.argv[2:])
            else:
                sys.stdout.write("\n\rCommand not sub class of BaseCommand.")
                sys.exit(-1)
        except IndexError:
            self._print_help()
        except KeyError:
            sys.stdout.write("\n\rCommand not available")
            self._print_help()
