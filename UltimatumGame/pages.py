from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
import json
import random
from random import sample, choice
import time

from otree.models_concrete import ParticipantToPlayerLookup, RoomToSession


def vars_for_all_templates(self):
    return {'game_number': self.participant.vars['game_number']}


class BasePage(Page):
    timer_text = 'Time left to complete the study:'

    def get_timeout_seconds(self):
        return self.participant.vars['expiry'] - time.time()

    def is_displayed(self):
        return self.participant.vars['expiry'] \
               - time.time() > 3 and not self.participant.vars[
            'timeout_happened'] and not self.participant.vars[
            'simulated']

    def before_next_page(self):
        if self.timeout_happened:
            self.participant.vars['timeout_happened'] = True
            self.participant.vars['timeout_game_number'] = self.participant.vars['game_number']


class ugIntro(BasePage):
    pass


class ugComp(BasePage):
    form_model = 'player'
    form_fields = ['comprehension']


class ug1(BasePage):
    form_model = 'player'
    form_fields = ['ug1']


class ug2(BasePage):
    form_model = 'player'
    form_fields = ['ug2']

    def before_next_page(self):
        self.participant.vars['game_number'] += 1
        self.participant.vars['ug1'] = self.player.ug1
        self.participant.vars['ug2'] = self.player.ug2


page_sequence = [
    ugIntro,
    ugComp,
    ug1,
    ug2
]
