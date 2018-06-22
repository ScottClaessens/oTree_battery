from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from Cryptodome.Cipher import PKCS1_OAEP
from Payoffs.management.commands.crypto_pps import get_public_key
import re
import time

public_key = get_public_key()
cipher = PKCS1_OAEP.new(public_key)


class CalculateWaitPage(WaitPage):
    wait_for_all_groups = True
    title_text = "Matching you to other participants... Please wait..."
    body_text = "Thank you for completing all the tasks. We will now randomly match you with other participants. " \
                "Since some participants are slower than others, please be patient while we wait for them to finish " \
                "too. We apologise if this takes some time. However, if anyone takes longer than the allotted hour, " \
                "we will skip them forward to this screen, so you shouldn't have to wait too long. NOTE: YOU MAY " \
                "LEAVE THIS SCREEN OPEN AND COME BACK TO IT LATER - AFTER THIS SCREEN, YOU CAN FINISH THE REST OF THE " \
                "STUDY AT YOUR OWN PACE."

    def after_all_players_arrive(self):
        self.subsession.dropouts_and_simulated()
        self.subsession.shuffle_groups_and_calculate_payoffs()


class Payoffs(Page):
    def is_displayed(self):
        return not self.player.timeout_happened and not self.player.simulated

    def vars_for_template(self):
        return self.player.payoff_vars()


class TimeoutHappened(Page):
    def is_displayed(self):
        return self.player.timeout_happened and not self.player.simulated


class Payment(Page):
    form_model = 'player'
    form_fields = ['first_name_cleartext','last_name_cleartext','bank_details_cleartext']

    def is_displayed(self):
        return not self.player.simulated

    def vars_for_template(self):
        return {'overall_bonus_cash': self.participant.payoff.to_real_world_currency(self.session),
                'payoff_plus_participation_fee': self.participant.payoff_plus_participation_fee()}

    def bank_details_cleartext_error_message(self, value):
        if value is not None:
            pattern = re.compile("^[0-9]{2}-[0-9]{4}-[0-9]{7}-[0-9]{3}$")
            if pattern.match(value) is None:
                return 'Please make sure that your bank details are exactly in the following format, with numbers ' \
                       'and dashes: 00-0000-0000000-000. You may need to add a leading zero to the last three digits.'

    def before_next_page(self):
        self.player.total_payment = self.participant.payoff_plus_participation_fee()


class BankAgain(Page):
    form_model = 'player'
    form_fields = ['correct_details']

    def vars_for_template(self):
        return {'first_name': self.player.first_name_cleartext,
                'last_name': self.player.last_name_cleartext,
                'bank_details': self.player.bank_details_cleartext}

    def is_displayed(self):
        return not self.player.simulated

    def before_next_page(self):
        for f in Constants.fields_with_encryption:
            cleartext_value = getattr(self.player, '{}_cleartext'.format(f))
            # before encrypting, need to encode to bytes
            cleartext_value = cleartext_value.encode('utf-8')
            encrypted_value = cipher.encrypt(cleartext_value)
            setattr(self.player, '{}_encrypted'.format(f), encrypted_value)

            # delete the sensitive cleartext data
            setattr(self.player, '{}_cleartext'.format(f), None)


class Recruitment(Page):
    form_model = 'player'
    form_fields = ['recruitment']

    def is_displayed(self):
        return not self.player.simulated


class Feedback(Page):
    form_model = 'player'
    form_fields = ['feedback']

    def is_displayed(self):
        return not self.player.simulated


class ReEnterLabel(Page):
    form_model = 'player'
    form_fields = ['reenterlabel']

    def is_displayed(self):
        return not self.player.simulated

    def reenterlabel_error_message(self, value):
        if value is not None:
            pattern = re.compile("^[A-Z]{3}[0-9]{2}$")
            if pattern.match(value) is None:
                return "That doesn't look right. Your participant label should be in the format AAA11. " \
                       "Please try again."

    def before_next_page(self):
        self.player.time_spent = time.time() - self.participant.vars['start.time']


class ReEnterLabel2(Page):
    form_model = 'player'
    form_fields = ['reenterlabel2']

    def is_displayed(self):
        return self.player.reenterlabel != self.participant.label and not self.player.simulated

    def reenterlabel2_error_message(self, value):
        if value is not None:
            pattern = re.compile("^[A-Z]{3}[0-9]{2}$")
            if pattern.match(value) is None:
                return "That doesn't look right. Your participant label should be in the format AAA11. " \
                       "Please try again."


class Final(Page):
    pass


page_sequence = [
    CalculateWaitPage,
    Payoffs,
    TimeoutHappened,
    Payment,
    BankAgain,
    Recruitment,
    Feedback,
    ReEnterLabel,
    ReEnterLabel2,
    Final
]
