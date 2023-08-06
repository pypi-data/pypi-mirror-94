"""   Installable manage.py command

      When executed without arguments, it will search for the QUICK_MIGRATE setting in settings.py,
      make migrations for every app in it and migrate.
      Otherwise, it will do the same only upon apps given as arguments.

      Prompt
      />>/$ py manage.py quickmigrate -h
      for more details """

import importlib.util
import os
import re
from io import StringIO

from django.core.management import base, call_command, CommandError
from django.conf import settings
from django.apps import apps as installed_apps

from ...apps import DjangoUtilConfig


def _is_config(app: str) -> bool:
    """ Checks whether the given path points to an AppConfig or not """

    if re.search(r'\.[a-zA-Z][\w-]+Config$', app):
        return True
    else:
        return False


def _resolve_config(config_path: str) -> str:
    """ Resolves path to an AppConfig and returns app name defined inside of it """

    module_name, config_name = config_path.rsplit('.', 1)
    module_path = os.path.join(*module_name.split('.'))
    spec = importlib.util.spec_from_file_location(module_name, module_path + '.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, config_name).name.rsplit('.', 1)[-1]


def _get_specified_apps() -> set[str]:
    """ Gets apps from QUICK_MIGRATE setting """

    apps = set()
    try:
        for app in settings.QUICK_MIGRATE:
            if _is_config(app):
                app = _resolve_config(app)
            apps.add(app)
        return apps
    except AttributeError:
        raise AttributeError('QUICK_MIGRATE wasn\'t provided by your project settings.'
                             ' Please specify apps to be processed either adding them'
                             ' to settings or providing as arguments.')


def _get_installed_apps() -> set[str]:
    """ Gets apps from INSTALLED_APPS except self """

    app_names = set(config.label for config in installed_apps.get_app_configs())
    app_names.remove(DjangoUtilConfig.name.rsplit('.', 1)[-1])
    return app_names


def _can_migrate(app: str) -> bool:
    """ Checks whether given app supports migrations or not """

    fake_io = StringIO()
    try:
        call_command('migrate', app, '--fake', stdout=fake_io)
    except CommandError as e:
        if 'not have migrations' in str(e):
            return False
        else:
            raise
    return True


class Command(base.BaseCommand):

    help = 'Makemigrations and migrate upon apps specified either as arguments or as QUICK_MIGRATE items' \
           ' (if no arguments were passed)'

    def add_arguments(self, parser) -> None:
        exclusive = parser.add_mutually_exclusive_group()
        exclusive.add_argument('-i', '--inst',
                               nargs='?',
                               choices=['base', 'all'],
                               const='all',
                               help='Look inside INSTALLED_APPS.'
                                    ' Prompt "base" to imitate makemigrations and migrate w/o arguments.'
                                    ' Prompt "all" to make migrations upon all apps in INSTALLED_APPS.'
                                    ' If optional argument isn\'t provided, defaults to "all"')
        exclusive.add_argument('-a', '--apps',
                               nargs='+',
                               help='Look for prompted apps only. Requires at least one app name')

    def _quickmigrate(self, apps: set[str] = None) -> None:
        """ Calls makemigrations and migrate upon every given app or just once w/o arguments if not given any apps"""

        if apps:
            for app in apps:
                if _can_migrate(app):
                    call_command('makemigrations', app)
                    call_command('migrate', app)
                else:
                    self.stdout.write(f'App {app} does not support migrations')

        else:
            call_command('makemigrations')
            call_command('migrate')

    def handle(self, *args, **options) -> None:
        """ Makes and calls migrations for either every app in QUICK_MIGRATE or every app given as argument """

        apps = set()

        if options['apps']:
            apps = set(options['apps'])

        elif opt := options['inst']:
            if opt == 'all':
                apps = _get_installed_apps()

        else:
            apps = _get_specified_apps()

        self._quickmigrate(apps)
