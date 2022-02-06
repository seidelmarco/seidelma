'''
The closepoll.py module has only one requirement – it must define a class
Command that extends BaseCommand or one of its subclasses.

The new custom command can be called using python manage.py closepoll <poll_ids>.
Achtung! Bash-Console $ nehmen, KEIN Run>>>
Das wird auch die Lösung für mein scraping_keydata script sein :-)
'''


from django.core.management.base import BaseCommand, CommandError
from polls.models import Question as Poll

class Command(BaseCommand):

    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('poll_ids', nargs='+', type=int)


    def handle(self, *args, **options):
        for poll_id in options['poll_ids']:
            try:
                poll = Poll.objects.get(pk=poll_id)
            except Poll.DoesNotExist:
                raise CommandError('Poll "%s" does not exist' % poll_id)

            poll.opened = False
            poll.save()

            self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"'
            % poll_id ))









