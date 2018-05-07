from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import Submission, Bot, SubmissionMustFail
import random



class PlayerBot(Bot):

    def play_round(self):
        p = self.player.id_in_group
        file_name = "player{0}.html".format(p)
        f = open(file_name, 'w')
        f.write(self.html)
        f.close()
        yield (pages.Payoffs)
        yield SubmissionMustFail(pages.Payment, {'first_name_cleartext': 'Scott',
                                                 'last_name_cleartext': 'Claessens',
                                                 'bank_details_cleartext': '000-000-000'})
        yield (pages.Payment, {'first_name_cleartext': 'Scott',
                               'last_name_cleartext': 'Claessens',
                               'bank_details_cleartext': '12-1234-1234567-001'})
        yield (pages.BankAgain, {'correct_details': 1})
        yield (pages.ReEnterLabel, {'reenterlabel': 'wrong_label'})
        yield (pages.ReEnterLabel2, {'reenterlabel2': 'wrong_label_again'})
        yield Submission(pages.Final, check_html=False)
