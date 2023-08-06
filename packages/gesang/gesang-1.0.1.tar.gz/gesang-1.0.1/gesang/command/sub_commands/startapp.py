from gesang.command import base


class Command(base.TemplateCommand):

    def handle(self, *args, **options):
        super().handle("app", **options)
