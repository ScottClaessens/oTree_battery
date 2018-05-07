from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

# from otree.models.session import Session as BaseSession
author = 'Scott Claessens'

doc = """
Second Party Punishment Game
"""


class Constants(BaseConstants):
    name_in_url = 'secondpp'
    players_per_group = None
    num_rounds = 1

    secondppInstructions = 'SecondPPGame/secondppInstructions.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    comprehension = models.IntegerField(
        label="If Person B transfers and Person A doesn't, how many points will they each have at the end of the "
              "transfer phase?",
        choices=[
            [1, 'A will have 100 (100 start  - 0 transferred), B will have 130 (100 start - 30 transferred + 60 gotten)'],
            [2, 'A will have 160 (100 start + 60 gotten - 0 transferred), B will have 70 (100 start - 30 transferred)'],
            [3, 'Both will have 130']],
        widget=widgets.RadioSelect
    )

    secondpp1 = models.IntegerField(
        label="Will you transfer 30 points to the other person?",
        choices=[
            [1, 'Transfer'],
            [2, "Don't transfer"]],
        widget=widgets.RadioSelect
    )

    secondpp2 = models.CurrencyField(
        label="If the other DOES TRANSFER, I will remove this many points... [0 - 50]",
        min=0,
        max=50
    )

    secondpp3 = models.CurrencyField(
        label="If the other DOESN'T TRANSFER, I will remove this many points... [0 - 50]",
        min=0,
        max=50
    )