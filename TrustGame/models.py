from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
author = 'Scott Claessens'

doc = """
    Trust Game
"""


class Constants(BaseConstants):
    name_in_url = 'tg'
    players_per_group = None
    num_rounds = 1

    tgInstructions = 'TrustGame/tgInstructions.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    comprehension = models.IntegerField(
        label="What happens if Person A transfers 50 points and Person B transfers back 25 points?",
        choices=[
            [1, 'Person A earns 25 points, person B earns 175 points'],
            [2, 'Person A earns 50 points, person B earns 50 points'],
            [3, 'Person A earns 100 points, person B earns 100 points']],
        widget=widgets.RadioSelect
        )

    tg1 = models.IntegerField(
        label="If you are person A, do you want to transfer your 50 points to B?",
        choices=[
            [1, 'No transfer'],
            [2, 'Transfer 50 points']],
        widget=widgets.RadioSelect
    )

    tg2 = models.CurrencyField(
        label="If you are person B and person A transfers you 50 points (which is multiplied to 150), "
              "how many points do you want to transfer back to A?",
        min=0,
        max=150,
    )
