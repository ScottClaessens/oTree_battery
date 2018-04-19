from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
import random
from .models import Constants


class PlayerBot(Bot):
    def play_round(self):
        yield(pages.dgIntro)
        yield(pages.dgComp, {'comprehension': 1})
        yield(pages.dgDecision, {'dg': c(random.randint(1,100))})