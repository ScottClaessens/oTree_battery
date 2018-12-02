from . import pages
from otree.api import Submission, Bot, SubmissionMustFail
import random


class PlayerBot(Bot):
    def play_round(self):
        # p = self.participant.id_in_session
        # file_name = "player{0}.html".format(p)
        # f = open(file_name, 'w')
        # f.write(self.html)
        # f.close()
        yield (pages.ThanksForWaiting)
        yield (pages.Payoffs)
        yield SubmissionMustFail(pages.Payment, {'first_name_cleartext': 'Scott',
                                                 'last_name_cleartext': 'Claessens',
                                                 'bank_details_cleartext': '000-000-000'})
        yield (pages.Payment, {'first_name_cleartext': 'Scott',
                               'last_name_cleartext': 'Claessens',
                               'bank_details_cleartext': '12-1234-1234567-001'})
        correct = random.choice([1,0])
        yield (pages.BankAgain, {'correct_details': correct})
        if correct == 0:
            yield (pages.BankWrong)
        yield (pages.Feedback, {'feedback': "No feedback",
                                'understand': random.randint(1, 7)})
        yield (pages.Recruitment, {'recruitment': 1})
        yield SubmissionMustFail(pages.ReEnterLabel, {'reenterlabel': '0'})
        yield (pages.ReEnterLabel, {'reenterlabel': 'AAA11'})
        yield SubmissionMustFail(pages.ReEnterLabel2, {'reenterlabel2': '0'})
        yield (pages.ReEnterLabel2, {'reenterlabel2': 'AAA11'})
        yield Submission(pages.Final, check_html=False)
