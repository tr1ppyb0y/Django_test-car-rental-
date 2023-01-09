import time

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from psycopg2 import OperationalError as PsycopgOperationalError


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write('Waiting for database...')
        db_up = False
        while not db_up:
            try:
                self.check(databases=['default'])
                db_up = True
            except (PsycopgOperationalError, OperationalError):
                self.stdout.write('Database unavailable, waiting for 1 second...')
                time.sleep(1)

        self.stdout.write('Database available!')
