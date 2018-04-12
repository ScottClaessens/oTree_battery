from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
# from otree.models.session import Session as BaseSession
author = 'Scott Claessens'

doc = """
General Instructions & Randomising App Sequence
"""


class Constants(BaseConstants):
    name_in_url = 'instructions'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    sequence_of_apps = models.LongStringField()
