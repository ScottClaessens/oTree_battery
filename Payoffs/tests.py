from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import Submission
import random


class PlayerBot(Bot):

    def play_round(self):
        # p = self.player.id_in_group
        # file_name = "player{0}.html".format(p)
        # f = open(file_name, 'w')
        # f.write(self.html)
        # f.close()
        yield (pages.Payoffs)
        yield (pages.Payment, {'payment_method': random.randint(1, 3)})
        if self.player.payment_method == 1:
            yield (pages.Method1, {'email': 'scott.claessens@hotmail.co.uk'})
        elif self.player.payment_method == 2:
            yield (pages.Method2, {'name': 'Scott Claessens',
                                   'bank_details': '000-000-000'})
        elif self.player.payment_method == 3:
            yield (pages.Method3, {'name': 'Scott Claessens',
                                   'postal_address': '1 High Street, Auckland, 1010'})
        yield Submission(pages.Final, check_html=False)
