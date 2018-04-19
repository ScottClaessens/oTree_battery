from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
import random


class PlayerBot(Bot):
    def play_round(self):
        yield (pages.tgIntro)
        yield (pages.tgComp, {'comprehension': 1})
        yield (pages.tg1, {'tg1': random.randint(1,2)})
        yield (pages.tg2, {'tg2': c(random.randint(1,150))})

