import re
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _
from blacklist.models import ListEntry
from blacklist.validators import validate_CPF


class Command(BaseCommand):
    help = _('Import a file containing one CPF per line')

    def add_arguments(self, parser):
        parser.add_argument('file', type=str)

    def handle(self, *args, **options):
        b_list = options['file']
        try:
            lines = []
            with open(b_list, 'r') as r:
                lines = r.readlines()

        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'File not found. ({b_list})')
            )
        for cpf in lines:
            cpf_line = cpf.strip("\n")
            cpf = re.sub("[-\.]", "", cpf_line)
            try:
                validate_CPF(cpf)
                ListEntry.objects.create(cpf=cpf)
                self.stdout.write(
                    self.style.SUCCESS(f'Imported ({cpf}).')
                )
            except IntegrityError:
                self.stdout.write(
                    self.style.WARNING(f'{cpf}: Already in list.')
                )
            except ValidationError as e:
                self.stdout.write(
                    self.style.ERROR(f'{cpf}: {",".join(e)}')
                )
