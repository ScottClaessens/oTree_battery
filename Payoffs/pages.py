from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from Cryptodome.Cipher import PKCS1_OAEP
from Payoffs.management.commands.crypto_pps import get_public_key
import re

public_key = get_public_key()
cipher = PKCS1_OAEP.new(public_key)


class GroupingWaitPage(WaitPage):
    group_by_arrival_time = True

    title_text = "Matching you to other participants... Please wait..."
    body_text = "Thank you for completing all the tasks. We will now match you with other participants. Since " \
                "some participants are slower than others, please be patient while we wait for them to finish too. " \
                "We apologise if this takes some time. However, if anyone takes longer than the allotted hour, we " \
                "will skip them forward to this screen, so you shouldn't have to wait too long."

    def after_all_players_arrive(self):
        self.group.dropouts_and_simulated()


class CalculateWaitPage(WaitPage):
    title_text = "Matching you to other participants... Please wait..."
    body_text = "Thank you for completing all the tasks. We will now match you with other participants. Since " \
                "some participants are slower than others, please be patient while we wait for them to finish too. " \
                "We apologise if this takes some time. However, if anyone takes longer than the allotted hour, we " \
                "will skip them forward to this screen, so you shouldn't have to wait too long."

    def after_all_players_arrive(self):
        self.group.calculate_payoffs()


class Payoffs(Page):
    def is_displayed(self):
        return not self.player.timeout_happened and not self.player.simulated

    def vars_for_template(self):
        return {'sequence_of_apps': self.participant.vars['sequence_of_apps'][1:8],
                # Dictator Game
                'matching_dg_role': self.participant.vars['matching_dg_role'],
                'matching_dg_transfer_to_me': self.participant.vars['matching_dg_transfer_to_me'],
                'matching_dg_payoff': self.participant.vars['matching_dg_payoff'],
                'dg': self.participant.vars['dg'],
                # Ultimatum Game
                'matching_ug_role': self.participant.vars['matching_ug_role'],
                'matching_ug_mao': self.participant.vars['matching_ug_mao'],
                'matching_ug_offer': self.participant.vars['matching_ug_offer'],
                'matching_ug_reject': self.participant.vars['matching_ug_reject'],
                'matching_ug_payoff': self.participant.vars['matching_ug_payoff'],
                'ug1': self.participant.vars['ug1'],
                'ug2': self.participant.vars['ug2'],
                # Trust Game
                'matching_tg_role': self.participant.vars['matching_tg_role'],
                'matching_tg_give': self.participant.vars['matching_tg_give'],
                'matching_tg_return': self.participant.vars['matching_tg_return'],
                'matching_tg_payoff': self.participant.vars['matching_tg_payoff'],
                'tg1': self.participant.vars['tg1'],
                'tg2': self.participant.vars['tg2'],
                # Second-Party Punishment Game
                'matching_2pp_pd': self.participant.vars['matching_2pp_pd'],
                'matching_2pp_puncoop': self.participant.vars['matching_2pp_puncoop'],
                'matching_2pp_pundef': self.participant.vars['matching_2pp_pundef'],
                'matching_2pp_payoff': self.participant.vars['matching_2pp_payoff'],
                'secondpp1': self.participant.vars['secondpp1'],
                'secondpp2': self.participant.vars['secondpp2'],
                'secondpp2_cost': self.participant.vars['secondpp2'] / 5,
                'secondpp3': self.participant.vars['secondpp3'],
                'secondpp3_cost': self.participant.vars['secondpp3'] / 5,
                # Third-Party Punishment Game
                'matching_3pp_role': self.participant.vars['matching_3pp_role'],
                'matching_3pp_take': self.participant.vars['matching_3pp_take'],
                'matching_3pp_punishment': self.participant.vars['matching_3pp_punishment'],
                'matching_3pp_payoff': self.participant.vars['matching_3pp_payoff'],
                'thirdpp1': self.participant.vars['thirdpp1'],
                'thirdpp2': self.participant.vars['thirdpp2'],
                'thirdpp2_cost': self.participant.vars['thirdpp2'] / 5,
                # Public Goods Game
                'matching_pgg_cont1': self.participant.vars['matching_pgg_cont1'],
                'matching_pgg_cont2': self.participant.vars['matching_pgg_cont2'],
                'matching_pgg_cont3': self.participant.vars['matching_pgg_cont3'],
                'matching_pgg_payoff': self.participant.vars['matching_pgg_payoff'],
                'pgg': self.participant.vars['pgg'],
                # Stag Hunt Game with Punishment
                'matching_staghunt_action': self.participant.vars['matching_staghunt_action'],
                'matching_staghunt_pun1': self.participant.vars['matching_staghunt_pun1'],
                'matching_staghunt_pun2': self.participant.vars['matching_staghunt_pun2'],
                'matching_staghunt_payoff': self.participant.vars['matching_staghunt_payoff'],
                'staghunt1': self.participant.vars['staghunt1'],
                'staghunt2': self.participant.vars['staghunt2'],
                'staghunt2_cost': self.participant.vars['staghunt2'] / 5,
                'staghunt3': self.participant.vars['staghunt3'],
                'staghunt3_cost': self.participant.vars['staghunt3'] / 5,
                # Overall
                'overall_payoff': self.player.dg_payoff + self.player.pgg_payoff + self.player.secondpp_payoff + \
                                  self.player.staghunt_payoff + self.player.tg_payoff + self.player.thirdpp_payoff + \
                                  self.player.ug_payoff,
                'overall_bonus_cash': self.participant.payoff.to_real_world_currency(self.session)
                }


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


class Attention(Page):
    form_model = 'player'
    form_fields = ['attention']

    def is_displayed(self):
        return not self.player.simulated


class Recruitment(Page):
    form_model = 'player'
    form_fields = ['recruitment']

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
    GroupingWaitPage,
    CalculateWaitPage,
    Payoffs,
    TimeoutHappened,
    Payment,
    BankAgain,
    Attention,
    Recruitment,
    ReEnterLabel,
    ReEnterLabel2,
    Final
]
