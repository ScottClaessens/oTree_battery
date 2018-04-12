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


class secondppIntro(Page):
    pass


class secondppComp(Page):
    form_model = 'player'
    form_fields = ['comprehension']


class secondpp1(Page):
    form_model = 'player'
    form_fields = ['secondpp1']


class secondpp2(Page):
    form_model = 'player'
    form_fields = ['secondpp2','secondpp3']

    def before_next_page(self):
        self.participant.vars['game_number'] += 1


page_sequence = [
    secondppIntro,
    secondppComp,
    secondpp1,
    secondpp2
]
