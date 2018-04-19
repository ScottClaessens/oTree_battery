from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import Submission


class PlayerBot(Bot):

    def play_round(self):
        p = self.player.id_in_group
        file_name = "html{0}.html".format(p)
        f = open(file_name, 'w')
        f.write(self.html)
        f.close()
        with open('file.name', 'w') as f:
            f.write('some stuff')
        yield (pages.Payoffs)
