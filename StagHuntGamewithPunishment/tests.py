from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
import random
from .models import Constants


class PlayerBot(Bot):
    def play_round(self):
        yield (pages.staghuntpunIntro)
        yield (pages.staghuntpunComp, {'comprehension': 1})
        yield (pages.staghuntpun1, {'staghunt1': random.randint(1, 2)})
        yield (pages.staghuntpun2, {'staghunt2': random.randint(1, 50),
                                 'staghunt3': random.randint(1, 50),
                                 })
