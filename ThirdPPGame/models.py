from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
author = 'Scott Claessens'

doc = """
    Third Party Punishment Game
"""


class Constants(BaseConstants):
    name_in_url = 'thirdpp'
    players_per_group = None
    num_rounds = 1

    thirdppInstructions = 'ThirdPPGame/thirdppInstructions.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    comprehension = models.IntegerField(
        label="When can Person C remove points from Person A?",
        choices=[
            [1, 'C can only choose to remove points from A if A chooses to take'],
            [2, 'C can always remove points from A'],
            [3, 'C can never remove points from A']],
        widget=widgets.RadioSelect
        )

    thirdpp1 = models.IntegerField(
        label="If you are Person A, will you take from Person B?",
        choices=[
            [1, "Don't Take"],
            [2, 'Take']],
        widget=widgets.RadioSelect
    )

    thirdpp2 = models.CurrencyField(
        label="If you are Person C, how many points will you remove from Person A if they take? [0 - 100] "
              "(Reminder: if A chooses to take, B loses 50 points and A gains 30 points.)",
        min=0,
        max=100,
    )
