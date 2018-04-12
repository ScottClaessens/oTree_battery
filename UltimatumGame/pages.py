from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
import json
import random
from random import sample, choice

from otree.models_concrete import ParticipantToPlayerLookup, RoomToSession


def vars_for_all_templates(self):
    return {'game_number': self.participant.vars['game_number']}


class ugIntro(Page):
    pass


class ugComp(Page):
    form_model = 'player'
    form_fields = ['comprehension']


class ug1(Page):
    form_model = 'player'
    form_fields = ['ug1']


class ug2(Page):
    form_model = 'player'
    form_fields = ['ug2']

    def before_next_page(self):
        self.participant.vars['game_number'] += 1


page_sequence = [
    ugIntro,
    ugComp,
    ug1,
    ug2
]
