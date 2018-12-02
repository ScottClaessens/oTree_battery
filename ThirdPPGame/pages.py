from . import models
from ._builtin import Page, WaitPage
import time


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


class thirdppIntro(BasePage):
    pass


class thirdppComp(BasePage):
    form_model = 'player'
    form_fields = ['comprehension']


class thirdppComp2(BasePage):
    def vars_for_template(self):
        return {'comp': self.player.comprehension}


class thirdpp1(BasePage):
    form_model = 'player'
    form_fields = ['thirdpp1']


class thirdpp2(BasePage):
    form_model = 'player'
    form_fields = ['thirdpp2']


class thirdppFinal(BasePage):
    def before_next_page(self):
        self.participant.vars['game_number'] += 1
        self.participant.vars['thirdpp1'] = self.player.thirdpp1
        self.participant.vars['thirdpp2'] = self.player.thirdpp2
        if self.participant.vars['game_number'] == 9:
            self.participant.vars['game_only_time_spent'] = int(time.time() - self.participant.vars['start.time'])


page_sequence = [
    thirdppIntro,
    thirdppComp,
    thirdppComp2,
    thirdpp1,
    thirdpp2,
    thirdppFinal
]
