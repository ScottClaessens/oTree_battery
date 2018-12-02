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
    timer_text = 'Please complete all 8 tasks within this time:'

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


class staghuntpunIntro(BasePage):
    pass


class staghuntpunComp(BasePage):
    form_model = 'player'
    form_fields = ['comprehension']


class staghuntpunComp2(BasePage):
    def vars_for_template(self):
        return {'comp': self.player.comprehension}


class staghuntpun1(BasePage):
    form_model = 'player'
    form_fields = ['staghunt1']


class staghuntpun2(BasePage):
    form_model = 'player'
    form_fields = ['staghunt2', 'staghunt3']


class staghuntpunFinal(BasePage):
    def before_next_page(self):
        self.participant.vars['game_number'] += 1
        self.participant.vars['staghunt1'] = self.player.staghunt1
        self.participant.vars['staghunt2'] = self.player.staghunt2
        self.participant.vars['staghunt3'] = self.player.staghunt3
        if self.participant.vars['game_number'] == 9:
            self.participant.vars['game_only_time_spent'] = int(time.time() - self.participant.vars['start.time'])


page_sequence = [
    staghuntpunIntro,
    staghuntpunComp,
    staghuntpunComp2,
    staghuntpun1,
    staghuntpun2,
    staghuntpunFinal
]
