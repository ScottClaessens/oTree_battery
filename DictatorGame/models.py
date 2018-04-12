from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

# from otree.models.session import Session as BaseSession
author = 'Scott Claessens'

doc = """
Dictator Game
"""


class Constants(BaseConstants):
    name_in_url = 'dg'
    players_per_group = None
    num_rounds = 1

    dgInstructions = 'DictatorGame/dgInstructions.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    comprehension = models.IntegerField(
        label="What happens if person A transfers 20 points?",
        choices=[
            [1, 'A keeps 80 points and B gets 20 points'],
            [2, 'Both get 20 points']],
        widget=widgets.RadioSelect
    )

    dg = models.CurrencyField(
        label="If you are person A in the interaction, how much will you transfer to person B?",
        min=0,
        max=100,
    )