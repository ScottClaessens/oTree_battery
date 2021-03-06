from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
import random
from .models import Constants


class PlayerBot(Bot):
    def play_round(self):
        yield (pages.secondppIntro)
        if random.uniform(0, 1) < 0.9:
            yield (pages.secondppComp, {'comprehension': 2})
        else:
            yield (pages.secondppComp, {'comprehension': 1})
        yield (pages.secondppComp2)
        yield (pages.secondpp1, {'secondpp1': random.randint(0, 1)})
        yield (pages.secondpp2, {'secondpp2': random.randint(1, 50), 'secondpp3': random.randint(1, 50)})
        yield (pages.secondppFinal)

