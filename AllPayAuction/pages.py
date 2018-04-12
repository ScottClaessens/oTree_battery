from . import models
from ._builtin import Page, WaitPage


def vars_for_all_templates(self):
    return {'game_number': self.participant.vars['game_number']}


class apaIntro(Page):
    pass


class apaComp(Page):
    form_model = 'player'
    form_fields = ['comprehension']


class apaDecision(Page):
    form_model = 'player'
    form_fields = ['apa']

    def before_next_page(self):
        self.participant.vars['game_number'] += 1


page_sequence = [
    apaIntro,
    apaComp,
    apaDecision
]
