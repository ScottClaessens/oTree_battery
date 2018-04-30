from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

# from otree.models.session import Session as BaseSession
author = 'Scott Claessens'

doc = """
Ultimatum Game
"""


class Constants(BaseConstants):
    name_in_url = 'ug'
    players_per_group = None
    num_rounds = 1

    ugInstructions = 'UltimatumGame/ugInstructions.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    comprehension = models.IntegerField(
        label="What happens if Person B accepts an offer of 20 points? What happens if Person B rejects this offer?",
        choices=[
            [1, 'If B accepts this offer then A gets 80 and B gets 20, if B rejects then A gets 80 and B gets 0'],
            [2, 'If B accepts this offer than A gets 0 and B gets 0, if B rejects then A gets 0 and B gets 0'],
            [3, 'If B accepts this offer then A gets 80 and B gets 20, if B rejects then both get 0']],
        widget=widgets.RadioSelect
    )

    ug1 = models.CurrencyField(
        label="If you are Person A, what amount will you offer to Person B? [0 - 100]",
        min=0,
        max=100,
    )

    ug2 = models.CurrencyField(
        label="If you are Person B, what is your minimum acceptable offer? That is, if the offer that Person A gives "
              "you is below this, you would reject and if the offer A gives you is "
              "above or equal to this, you would accept. [0 - 100]",
        min=0,
        max=100
    )