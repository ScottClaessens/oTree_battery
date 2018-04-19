from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
import random
from .models import Constants


class PlayerBot(Bot):
    def play_round(self):
        yield (pages.pggIntro)
        yield (pages.pggComp, {'comprehension': 1})
        yield (pages.pggDecision, {'pgg': c(random.randint(1,100))})