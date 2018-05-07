from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
import random
from .models import Constants


class PlayerBot(Bot):
    def play_round(self):
        yield (pages.secondppIntro)
        yield (pages.secondppComp, {'comprehension': 1})
        yield (pages.secondpp1, {'secondpp1': random.randint(1,2)})
        yield (pages.secondpp2, {'secondpp2': random.randint(1,50), 'secondpp3': random.randint(1,50)})
