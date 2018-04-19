from . import models
from ._builtin import Page, WaitPage


def vars_for_all_templates(self):
    return {'game_number': self.participant.vars['game_number']}


class thirdppIntro(Page):
    pass


class thirdppComp(Page):
    form_model = 'player'
    form_fields = ['comprehension']


class thirdpp1(Page):
    form_model = 'player'
    form_fields = ['thirdpp1']


class thirdpp2(Page):
    form_model = 'player'
    form_fields = ['thirdpp2']

    def before_next_page(self):
        self.participant.vars['game_number'] += 1
        self.participant.vars['thirdpp1'] = self.player.thirdpp1
        self.participant.vars['thirdpp2'] = self.player.thirdpp2


page_sequence = [
    thirdppIntro,
    thirdppComp,
    thirdpp1,
    thirdpp2
]
