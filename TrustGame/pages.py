from . import models
from ._builtin import Page, WaitPage
import time


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


class tgIntro(BasePage):
    pass


class tgComp(BasePage):
    form_model = 'player'
    form_fields = ['comprehension']


class tgComp2(BasePage):
    def vars_for_template(self):
        return {'comp': self.player.comprehension}


class tg1(BasePage):
    form_model = 'player'
    form_fields = ['tg1']


class tg2(BasePage):
    form_model = 'player'
    form_fields = ['tg2']

    def before_next_page(self):
        self.participant.vars['game_number'] += 1
        self.participant.vars['tg1'] = self.player.tg1
        self.participant.vars['tg2'] = self.player.tg2
        if self.participant.vars['game_number'] == 9:
            self.participant.vars['game_only_time_spent'] = int(time.time() - self.participant.vars['start.time'])


page_sequence = [
    tgIntro,
    tgComp,
    tgComp2,
    tg1,
    tg2
]
