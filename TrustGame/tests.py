from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
import random


class PlayerBot(Bot):
    def play_round(self):
        yield (pages.tgIntro)
        if random.uniform(0, 1) < 0.9:
            yield (pages.tgComp, {'comprehension': 1})
        else:
            yield (pages.tgComp, {'comprehension': 2})
        yield (pages.tg1, {'tg1': random.randint(0, 1)})
        yield (pages.tg2, {'tg2': c(random.randint(1, 150))})

