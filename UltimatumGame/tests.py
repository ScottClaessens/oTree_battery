from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
import random
from .models import Constants


class PlayerBot(Bot):
    def play_round(self):
        yield (pages.ugIntro)
        if random.uniform(0, 1) < 0.9:
            yield (pages.ugComp, {'comprehension': 3})
        else:
            yield (pages.ugComp, {'comprehension': 1})
        yield (pages.ugComp2)
        yield (pages.ug1, {'ug1': c(random.randint(1, 100))})
        yield (pages.ug2, {'ug2': random.randint(1, 100)})
        yield (pages.ugFinal)
