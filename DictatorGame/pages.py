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
    timer_text = 'Time remaining in session:'

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


class dgIntro(BasePage):
    pass


class dgComp(BasePage):
    form_model = 'player'
    form_fields = ['comprehension']


class dgComp2(BasePage):
    def vars_for_template(self):
        return {'comp': self.player.comprehension}


class dgDecision(BasePage):
    form_model = 'player'
    form_fields = ['dg']

    def before_next_page(self):
        self.participant.vars['game_number'] += 1
        self.participant.vars['dg'] = self.player.dg
        if self.participant.vars['game_number'] == 9:
            self.participant.vars['game_only_time_spent'] = time.time() - self.participant.vars['start.time']


page_sequence = [
    dgIntro,
    dgComp,
    dgComp2,
    dgDecision
]
