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
    name_in_url = 'staghuntpun'
    players_per_group = None
    num_rounds = 1

    staghuntInstructions = 'StagHuntGamewithPunishment/staghuntpunInstructions.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    comprehension = models.IntegerField(
        label="If you transfer 30 points to the group project, but the other person does not, how many points will "
              "you have at the end of the transfer phase?",
        choices=[
            [1, '130 points (100 start + 30)'],
            [2, '100 points (100 start + 0)'],
            [3, '70 points (100 start - 30)']],
        widget=widgets.RadioSelect
    )

    staghunt1 = models.IntegerField(
        label="Will you transfer 30 points to the group project?",
        choices=[
            [1, 'Transfer 30 points'],
            [0, 'No transfer']],
        widget=widgets.RadioSelect
    )

    staghunt2 = models.CurrencyField(
        label="If the other DOES TRANSFER, I will remove this many points... [0 - 50]",
        min=0,
        max=50
    )

    staghunt3 = models.CurrencyField(
        label="If the other DOESN'T TRANSFER, I will remove this many points... [0 - 50]",
        min=0,
        max=50
    )