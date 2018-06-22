from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
import random
from .models import Constants


class PlayerBot(Bot):
    def play_round(self):
        yield (pages.shIntro)
        if random.uniform(0, 1) < 0.9:
            yield (pages.shComp, {'comprehension': 3})
        else:
            yield (pages.shComp, {'comprehension': 1})
        yield (pages.shDecision, {'sh': c(random.randint(0, 1))})
