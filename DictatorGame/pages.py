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


class dgIntro(Page):
    pass


class dgComp(Page):
    form_model = 'player'
    form_fields = ['comprehension']


class dgDecision(Page):
    form_model = 'player'
    form_fields = ['dg']

    def before_next_page(self):
        self.participant.vars['game_number'] += 1


page_sequence = [
    dgIntro,
    dgComp,
    dgDecision
]
