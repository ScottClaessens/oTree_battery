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


class pggIntro(BasePage):
    pass


class pggComp(BasePage):
    form_model = 'player'
    form_fields = ['comprehension']


class pggComp2(BasePage):
    def vars_for_template(self):
        return {'comp': self.player.comprehension}


class pggDecision(BasePage):
    form_model = 'player'
    form_fields = ['pgg']


class pggFinal(BasePage):
    def before_next_page(self):
        self.participant.vars['game_number'] += 1
        self.participant.vars['pgg'] = self.player.pgg
        if self.participant.vars['game_number'] == 9:
            self.participant.vars['game_only_time_spent'] = int(time.time() - self.participant.vars['start.time'])


page_sequence = [
    pggIntro,
    pggComp,
    pggComp2,
    pggDecision,
    pggFinal
]
