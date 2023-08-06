# Python
import logging
from io import StringIO

# Django
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.apps import apps
from django.db import connection


class Command(BaseCommand):

    help = 'Reset databases sequences for all apps.'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', default=False,
                            help='Just show the SQL that would be executed; '
                            'don\'t actually execute it.')

    def init_logging(self):
        log_levels = dict(enumerate([logging.ERROR, logging.INFO,
                                     logging.DEBUG, 0]))
        logging.getLogger('iso8601').setLevel(logging.WARNING)
        logging.getLogger('django.db.backends').setLevel(log_levels.get(self.verbosity, 0) + 10)
        self.logger = logging.getLogger()
        self.logger.setLevel(log_levels.get(self.verbosity, 0))
        handler = logging.StreamHandler(self.stderr)
        handler.setFormatter(logging.Formatter('%(levelname)-8s %(message)s'))
        handler.terminator = ''
        self.logger.addHandler(handler)
        self.logger.propagate = False

    def handle(self, *args, **options):
        self.verbosity = int(options.get('verbosity', 1))
        self.dry_run = bool(options.get('dry_run', False))
        self.init_logging()
        sql_output = StringIO()
        cursor = connection.cursor()
        for app in apps.get_app_configs():
            call_command('sqlsequencereset', app.label, stdout=sql_output,
                         no_color=True)
        sql_commands = []
        sql_commit = None
        for n, sql_command in enumerate(sql_output.getvalue().splitlines()):
            if sql_command.upper().startswith('BEGIN'):
                if n == 0:
                    sql_commands.append(sql_command)
            elif sql_command.upper().startswith('COMMIT'):
                if not sql_commit:
                    sql_commit = sql_command
            else:
                sql_commands.append(sql_command)
        if sql_commit:
            sql_commands.append(sql_commit)

        if self.dry_run:
            for sql_command in sql_commands:
                self.logger.info('would execute: %s', sql_command)
        else:
            for sql_command in sql_commands:
                self.logger.info('executing: %s', sql_command)
                cursor.execute(sql_command)
