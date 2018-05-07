from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

# from otree.models.session import Session as BaseSession
author = 'Scott Claessens'

doc = """
Stag Hunt Game with Punishment
"""


class Constants(BaseConstants):
    name_in_url = 'staghunt'
    players_per_group = None
    num_rounds = 1

    staghuntInstructions = 'StagHuntGame/staghuntInstructions.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    comprehension = models.IntegerField(
        label="If you choose Action 1, and the other person chooses Action 2, how many points will you have at the "
              "end of the action phase?",
        choices=[
            [1, '100 points (100 start + 0)'],
            [2, '150 points (100 start + 50)'],
            [3, '180 points (100 start + 80)']],
        widget=widgets.RadioSelect
    )

    staghunt1 = models.IntegerField(
        label="Which action will you choose?",
        choices=[
            [1, 'Action 1'],
            [2, 'Action 2']],
        widget=widgets.RadioSelect
    )

    staghunt2 = models.CurrencyField(
        label="If the other chooses ACTION 1, I will remove this many points... [0 - 50]",
        min=0,
        max=50
    )

    staghunt3 = models.CurrencyField(
        label="If the other chooses ACTION 2, I will remove this many points... [0 - 50]",
        min=0,
        max=50
    )