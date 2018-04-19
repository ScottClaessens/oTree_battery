from . import models
from ._builtin import Page, WaitPage


def vars_for_all_templates(self):
    return {'game_number': self.participant.vars['game_number']}


class tgIntro(Page):
    pass


class tgComp(Page):
    form_model = 'player'
    form_fields = ['comprehension']


class tg1(Page):
    form_model = 'player'
    form_fields = ['tg1']


class tg2(Page):
    form_model = 'player'
    form_fields = ['tg2']

    def before_next_page(self):
        self.participant.vars['game_number'] += 1
        self.participant.vars['tg1'] = self.player.tg1
        self.participant.vars['tg2'] = self.player.tg2

page_sequence = [
    tgIntro,
    tgComp,
    tg1,
    tg2
]
