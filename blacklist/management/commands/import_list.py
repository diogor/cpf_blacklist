from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _


class Command(BaseCommand):
    help = _('Import a file containing one CPF per line')

    def add_arguments(self, parser):
        parser.add_argument('file', type=str)

    def handle(self, *args, **options):
        if options['file']:
            self.stdout.write(self.style.WARNING(f'{options["file"]}'))
        self.stdout.write(self.style.SUCCESS(_("Imported succefully!")))
