from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

# from otree.models.session import Session as BaseSession
author = 'Scott Claessens'

doc = """
Public Goods Game
"""


class Constants(BaseConstants):
    name_in_url = 'pgg'
    players_per_group = None
    num_rounds = 1

    pggInstructions = 'PublicGoodsGame/pggInstructions.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    comprehension = models.IntegerField(
        label="What contribution BY YOU maximises payoffs for the GROUP? What about for yourself?",
        choices=[
            [1, 'Contributing 100 maximises payoffs for both the group and myself'],
            [2, 'Contributing 0 maximises payoffs for both the group and myself'],
            [3, 'Contributing 100 maximises payoffs for the group but contributing 0 maximises my own payoff']],
        widget=widgets.RadioSelect
    )

    pgg = models.CurrencyField(
        label="How many points do you wish to contribute to the group project? [0 - 100]",
        min=0,
        max=100,
    )