from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
import random


class PlayerBot(Bot):
    def play_round(self):
        yield (pages.thirdppIntro)
        if random.uniform(0, 1) < 0.9:
            yield (pages.thirdppComp, {'comprehension': 1})
        else:
            yield (pages.thirdppComp, {'comprehension': 2})
        yield (pages.thirdpp1, {'thirdpp1': random.randint(1,2)})
        yield (pages.thirdpp2, {'thirdpp2': c(random.randint(1,100))})

