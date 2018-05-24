from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

# from otree.models.session import Session as BaseSession
author = 'Scott Claessens'

doc = """
Stag Hunt Game
"""


class Constants(BaseConstants):
    name_in_url = 'staghunt'
    players_per_group = None
    num_rounds = 1

    shInstructions = 'StagHuntGame/shInstructions.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    comprehension = models.IntegerField(
        label="If you contribute 30 points to the group project, but no one else does, how many points do you end "
              "this game with?",
        choices=[
            [1, '130 points'],
            [2, '100 points'],
            [3, '70 points']],
        widget=widgets.RadioSelect
    )

    sh = models.IntegerField(
        label="Will you contribute 30 points to the group project?",
        choices=[
            [1, 'Contribute 30 points'],
            [2, 'Do not contribute 30 points']],
        widget=widgets.RadioSelect
    )