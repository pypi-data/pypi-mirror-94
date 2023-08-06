from argparse import ArgumentParser
import os
import shutil
import stat
from gesang.utils import exc


class BaseCommand:

    def create_parser(self):
        parser = ArgumentParser()
        self.add_argument(parser=parser)
        return parser

    def add_argument(self, parser: ArgumentParser):
        pass

    def run_from_argv(self, prog_name, sub_command, argv):
        parser = self.create_parser()
        options = parser.parse_args(argv)
        cmd_options = vars(options)
        args = cmd_options.pop('args', ())
        self.execute(*args, **cmd_options)

    def execute(self, *args, **kwargs):
        self.handle(*args, **kwargs)

    def handle(self, *args, **options):
        """
        The actual logic of the command. Subclasses must implement
        this method.
        """
        raise NotImplementedError('subclasses of BaseCommand must provide a handle() method')


class TemplateCommand(BaseCommand):

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def add_argument(self, parser):
        parser.add_argument("name", help="Name of the application or project.")
        parser.add_argument("directory", nargs="?", help="Optional destination directory.")

    def handle(self, app_or_project, **options):
        name = options.pop("name")
        directory = options.pop("directory")
        template_dir = os.path.join(self.base_dir, "tmpl", app_or_project)
        work_dir = directory or os.getcwd()
        target_dir = os.path.join(work_dir, name)
        if os.path.exists(target_dir):
            raise exc.CommandError(f"Target dir {target_dir} already exist.")

        prefix_length = len(template_dir) + 1
        # 拷贝到目标文件夹
        for root, dirs, files in os.walk(template_dir):
            relative_dir = root[prefix_length:]
            for dirname in dirs[:]:
                if dirname.startswith(".") or dirname == "__pycache__":
                    dirs.remove(dirname)

            for filename in files:
                if filename.endswith((".pyo", ".pyc", ".py.class")):
                    # Ignore some files as they cause various breakages.
                    continue
                # 模板文件路径拷贝到目标路径中，并且文件以.py结尾
                old_path = os.path.join(root, filename)
                tmpl_suffix = ".py-tmpl"
                new_path = os.path.join(target_dir, relative_dir, filename)
                if new_path.endswith(tmpl_suffix):
                    new_path = new_path[:-len(tmpl_suffix)] + ".py"
                if os.path.exists(os.path.dirname(new_path)) is False:
                    os.makedirs(os.path.dirname(new_path))
                # 拷贝文件
                shutil.copyfile(src=old_path, dst=new_path)
                # 重新设置写的权限
                if not os.access(new_path, os.W_OK):
                    st = os.stat(new_path)
                    new_permissions = stat.S_IMODE(st.st_mode) | stat.S_IWUSR
                    os.chmod(new_path, new_permissions)
