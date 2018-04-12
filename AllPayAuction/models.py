from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

# from otree.models.session import Session as BaseSession
author = 'Scott Claessens'

doc = """
All Pay Auction
"""


class Constants(BaseConstants):
    name_in_url = 'apa'
    players_per_group = None
    num_rounds = 1

    apaInstructions = 'AllPayAuction/apaInstructions.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    comprehension = models.IntegerField(
        label="If person A spends 50 points to try to win and person B spends 30 points, how many points do they "
              "each earn?",
        choices=[
            [1, 'A gets 150 (100 start - 50 spent + 100 for prize), B gets 70 (100 start - 30 spent)'],
            [2, 'Both get 100 points'],
            [3, 'A gets 180 (100 start - 30 spent + 100 for prize), B gets 100 (100 start)']],
        widget=widgets.RadioSelect
    )

    apa = models.CurrencyField(
        label="How many points do you want to spend to try and get the 100 point prize?",
        min=0,
        max=100,
    )