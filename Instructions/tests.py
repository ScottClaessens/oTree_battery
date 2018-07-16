from . import pages
from otree.api import Bot, SubmissionMustFail


class PlayerBot(Bot):
    def play_round(self):
        yield SubmissionMustFail(pages.ReEnterLabel, {'reenterlabel': '0'})
        yield (pages.ReEnterLabel, {'reenterlabel': 'AAA11'})
        yield(pages.Consent)
        yield(pages.Instructions)