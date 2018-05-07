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
    body_text = "Thank you for completing all the decisions. We will now match you with other participants. Since " \
                "some participants are slower than others, please be patient. When we have successfully matched " \
                "you with other participants, you will see a screen with the results of all the interactions, and " \
                "your earnings."

    def after_all_players_arrive(self):
        for p in self.group.get_players():
            # For drop outs and simulated players, set average responses
            if p.participant.vars['timeout_happened'] or p.participant.vars['simulated']:
                print("MEDIAN RESPONSES BEING SAVED")
                p.participant.vars['dg'] = c(25)
                p.participant.vars['ug1'] = c(40)
                p.participant.vars['ug2'] = c(25)
                p.participant.vars['tg1'] = 2
                p.participant.vars['tg2'] = c(75)
                p.participant.vars['secondpp1'] = 1
                p.participant.vars['secondpp2'] = c(0)
                p.participant.vars['secondpp3'] = c(30)
                p.participant.vars['thirdpp1'] = 1
                p.participant.vars['thirdpp2'] = c(30)
                p.participant.vars['pgg'] = c(30)
                p.participant.vars['staghunt1'] = 1
                p.participant.vars['staghunt2'] = c(0)
                p.participant.vars['staghunt3'] = c(30)
                p.participant.vars['staghunt4'] = c(0)
                p.participant.vars['staghunt5'] = c(0)
            else:
                print("NO TIMEOUT")
            if p.participant.vars['timeout_happened']:
                p.timeout_happened = True
                p.timeout_game_number = p.participant.vars['timeout_game_number']
            elif p.participant.vars['simulated']:
                p.simulated = True


class CalculateWaitPage(WaitPage):
    title_text = "Matching you to other participants... Please wait..."
    body_text = "Thank you for completing all the decisions. We will now match you with other participants. Since " \
                "some participants are slower than others, please be patient. When we have successfully matched " \
                "you with other participants, you will see a screen with the results of all the interactions, and " \
                "your earnings."

    def after_all_players_arrive(self):
        for p in self.group.get_players():
            print("BEGINNING CALCULATIONS")
            #
            #
            # Dictator Game
            #
            #
            if p.id_in_group in (1, 3, 5, 7):
                # Person A
                p.participant.vars['matching_dg_role'] = 'Person A'
                p.participant.vars['matching_dg_payoff'] = c(100) - c(p.participant.vars['dg'])
                p.participant.payoff += c(100) - c(p.participant.vars['dg'])
            else:
                # Person B
                p.participant.vars['matching_dg_role'] = 'Person B'
                matching_dg_transfer_to_me = c(self.group.get_player_by_id(p.id_in_group - 1).participant.vars['dg'])
                p.participant.vars['matching_dg_transfer_to_me'] = matching_dg_transfer_to_me
                p.participant.vars['matching_dg_payoff'] = matching_dg_transfer_to_me
                p.participant.payoff += matching_dg_transfer_to_me
            #
            #
            # Ultimatum Game
            #
            #
            if p.id_in_group in (1, 2, 5, 6):
                # Person A
                p.participant.vars['matching_ug_role'] = 'Person A'
                matching_ug_mao = c(self.group.get_player_by_id(p.id_in_group + 2).participant.vars['ug2'])
                p.participant.vars['matching_ug_mao'] = matching_ug_mao
                if p.participant.vars['ug1'] < matching_ug_mao:
                    p.participant.vars['matching_ug_reject'] = True
                    p.participant.vars['matching_ug_payoff'] = c(0)
                    p.participant.payoff += c(0)
                else:
                    p.participant.vars['matching_ug_reject'] = False
                    p.participant.vars['matching_ug_payoff'] = c(100) - c(p.participant.vars['ug1'])
                    p.participant.payoff += c(100) - c(p.participant.vars['ug1'])
            else:
                # Person B
                p.participant.vars['matching_ug_role'] = 'Person B'
                matching_ug_offer = c(self.group.get_player_by_id(p.id_in_group - 2).participant.vars['ug1'])
                p.participant.vars['matching_ug_offer'] = matching_ug_offer
                if matching_ug_offer < p.participant.vars['ug2']:
                    p.participant.vars['matching_ug_reject'] = True
                    p.participant.vars['matching_ug_payoff'] = c(0)
                    p.participant.payoff += c(0)
                else:
                    p.participant.vars['matching_ug_reject'] = False
                    p.participant.vars['matching_ug_payoff'] = matching_ug_offer
                    p.participant.payoff += matching_ug_offer
            #
            #
            # Trust Game
            #
            #
            if p.id_in_group in (3, 4, 7, 8):
                # Person A
                p.participant.vars['matching_tg_role'] = 'Person A'
                if p.id_in_group in (3, 4):
                    matching_tg_return = c(self.group.get_player_by_id(p.id_in_group + 2).participant.vars['tg2'])
                else:
                    matching_tg_return = c(self.group.get_player_by_id(p.id_in_group - 6).participant.vars['tg2'])
                p.participant.vars['matching_tg_return'] = matching_tg_return
                if p.participant.vars['tg1'] == 1:
                    p.participant.vars['matching_tg_payoff'] = c(50)
                    p.participant.payoff += c(50)
                else:
                    p.participant.vars['matching_tg_payoff'] = matching_tg_return
                    p.participant.payoff += matching_tg_return
            elif p.id_in_group in (1, 2, 5, 6):
                # Person B
                p.participant.vars['matching_tg_role'] = 'Person B'
                if p.id_in_group in (1, 2):
                    matching_tg_give = self.group.get_player_by_id(p.id_in_group + 6).participant.vars['tg1']
                elif p.id_in_group in (5, 6):
                    matching_tg_give = self.group.get_player_by_id(p.id_in_group - 2).participant.vars['tg1']
                p.participant.vars['matching_tg_give'] = matching_tg_give
                if matching_tg_give == 1:
                    p.participant.vars['matching_tg_payoff'] = c(50)
                    p.participant.payoff += c(50)
                else:
                    p.participant.vars['matching_tg_payoff'] = c(200) - p.participant.vars['tg2']
                    p.participant.payoff += c(200) - p.participant.vars['tg2']
            #
            #
            # Second-Party Punishment Game
            #
            #
            # Transfer stage
            if p.id_in_group in (1, 2, 3, 4):
                matching_2pp_pd = self.group.get_player_by_id(p.id_in_group + 4).participant.vars['secondpp1']
            else:
                matching_2pp_pd = self.group.get_player_by_id(p.id_in_group - 4).participant.vars['secondpp1']
            p.participant.vars['matching_2pp_pd'] = matching_2pp_pd
            if p.participant.vars['secondpp1'] == 1:
                if matching_2pp_pd == 1:
                    temppayoff = c(130)
                else:
                    temppayoff = c(70)
            else:
                if matching_2pp_pd == 1:
                    temppayoff = c(160)
                else:
                    temppayoff = c(100)
            # Punishment Stage
            if p.id_in_group in (1, 2, 3, 4):
                matching_2pp_puncoop = c(self.group.get_player_by_id(p.id_in_group + 4).participant.vars['secondpp2'])
                matching_2pp_pundef = c(self.group.get_player_by_id(p.id_in_group + 4).participant.vars['secondpp3'])
            else:
                matching_2pp_puncoop = c(self.group.get_player_by_id(p.id_in_group - 4).participant.vars['secondpp2'])
                matching_2pp_pundef = c(self.group.get_player_by_id(p.id_in_group - 4).participant.vars['secondpp3'])
            p.participant.vars['matching_2pp_puncoop'] = matching_2pp_puncoop
            p.participant.vars['matching_2pp_pundef'] = matching_2pp_pundef
            # Deal punishment
            if matching_2pp_pd == 1:
                temppayoff -= c(p.participant.vars['secondpp2'] / 5)
            else:
                temppayoff -= c(p.participant.vars['secondpp3'] / 5)
            # Receive punishment
            if p.participant.vars['secondpp1'] == 1:
                temppayoff -= matching_2pp_puncoop
            else:
                temppayoff -= matching_2pp_pundef
            # Set payoffs
            p.participant.vars['matching_2pp_payoff'] = temppayoff
            p.participant.payoff += temppayoff
            #
            #
            # Third-Party Punishment
            #
            #
            if p.id_in_group in (2, 4, 6, 8):
                # Person A
                p.participant.vars['matching_3pp_role'] = 'Person A'
                if p.id_in_group in (2, 4, 6):
                    matching_3pp_punishment = c(
                        self.group.get_player_by_id(p.id_in_group + 1).participant.vars['thirdpp2'])
                else:
                    matching_3pp_punishment = c(
                        self.group.get_player_by_id(1).participant.vars['thirdpp2'])
                p.participant.vars['matching_3pp_punishment'] = matching_3pp_punishment
                if p.participant.vars['thirdpp1'] == 1:
                    p.participant.vars['matching_3pp_payoff'] = c(100)
                    p.participant.payoff += c(100)
                else:
                    p.participant.vars['matching_3pp_payoff'] = c(130) - matching_3pp_punishment
                    p.participant.payoff += c(130) - matching_3pp_punishment
            else:
                # Person C
                p.participant.vars['matching_3pp_role'] = 'Person C'
                if p.id_in_group in (3, 5, 7):
                    matching_3pp_take = c(
                        self.group.get_player_by_id(p.id_in_group - 1).participant.vars['thirdpp1'])
                else:
                    matching_3pp_take = c(
                        self.group.get_player_by_id(8).participant.vars['thirdpp1'])
                p.participant.vars['matching_3pp_take'] = matching_3pp_take
                if matching_3pp_take == 1:
                    p.participant.vars['matching_3pp_payoff'] = c(100)
                    p.participant.payoff += c(100)
                else:
                    p.participant.vars['matching_3pp_payoff'] = c(100) - (p.participant.vars['thirdpp2'] / 5)
                    p.participant.payoff += c(100) - (p.participant.vars['thirdpp2'] / 5)
            #
            #
            # Public Goods Game
            #
            #
            if p.id_in_group in (1, 3, 6, 8):
                group = [1, 3, 6, 8]
            else:
                group = [2, 4, 5, 7]
            group.remove(p.id_in_group)
            the_rest = group
            i = 0
            for q in the_rest:
                i += 1
                p.participant.vars['matching_pgg_cont%i' % i] = c(
                    self.group.get_player_by_id(q).participant.vars['pgg'])
            total = p.participant.vars['matching_pgg_cont1'] + \
                     p.participant.vars['matching_pgg_cont2'] + \
                     p.participant.vars['matching_pgg_cont3'] + \
                     p.participant.vars['pgg']
            p.participant.vars['matching_pgg_payoff'] = c(100) - p.participant.vars['pgg'] + c(total / 2)
            p.participant.payoff += c(100) - p.participant.vars['pgg'] + c(total / 2)
            #
            #
            # Stag-Hunt Punishment
            #
            #
            # Transfer stage
            if p.id_in_group in (1, 3, 5, 7):
                matching_staghunt_action = self.group.get_player_by_id(((p.id_in_group + 2) % 8) + 1).participant.vars['staghunt1']
            else:
                matching_staghunt_action = self.group.get_player_by_id((p.id_in_group - 3) % 8).participant.vars['staghunt1']
            p.participant.vars['matching_staghunt_action'] = matching_staghunt_action
            if p.participant.vars['staghunt1'] == 1:
                if matching_staghunt_action == 1:
                    temppayoff = c(180)
                else:
                    temppayoff = c(100)
            else:
                if matching_staghunt_action == 1:
                    temppayoff = c(150)
                else:
                    temppayoff = c(150)
            # Punishment Stage
            if p.id_in_group in (1, 3, 5, 7):
                matching_staghunt_pun1 = self.group.get_player_by_id(((p.id_in_group + 2) % 8) + 1).participant.vars['staghunt2']
                matching_staghunt_pun2 = self.group.get_player_by_id(((p.id_in_group + 2) % 8) + 1).participant.vars['staghunt3']
            else:
                matching_staghunt_pun1 = self.group.get_player_by_id((p.id_in_group - 3) % 8).participant.vars['staghunt2']
                matching_staghunt_pun2 = self.group.get_player_by_id((p.id_in_group - 3) % 8).participant.vars['staghunt3']
            p.participant.vars['matching_staghunt_pun1'] = matching_staghunt_pun1
            p.participant.vars['matching_staghunt_pun2'] = matching_staghunt_pun2
            # Deal punishment
            if p.participant.vars['matching_staghunt_action'] == 1:
                temppayoff -= c(p.participant.vars['staghunt2'] / 5)
            else:
                temppayoff -= c(p.participant.vars['staghunt3'] / 5)
            # Receive punishment
            if p.participant.vars['staghunt1'] == 1:
                temppayoff -= c(p.participant.vars['matching_staghunt_pun1'])
            else:
                temppayoff -= c(p.participant.vars['matching_staghunt_pun2'])
            # Set payoffs
            p.participant.vars['matching_staghunt_payoff'] = temppayoff
            p.participant.payoff += temppayoff
            #
            #
            # Set payoffs back to zero for simulated players and timeouts
            #
            #
            if p.simulated or p.timeout_happened:
                p.participant.payoff = c(0)
            #
            #
            # Save each game payoff from participant.vars directly into models
            #
            #
            p.dg_payoff = p.participant.vars['matching_dg_payoff']
            p.ug_payoff = p.participant.vars['matching_ug_payoff']
            p.tg_payoff = p.participant.vars['matching_tg_payoff']
            p.secondpp_payoff = p.participant.vars['matching_2pp_payoff']
            p.thirdpp_payoff = p.participant.vars['matching_3pp_payoff']
            p.pgg_payoff = p.participant.vars['matching_pgg_payoff']
            p.staghunt_payoff = p.participant.vars['matching_staghunt_payoff']

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
                'overall_payoff': self.participant.payoff,
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


class ReEnterLabel(Page):
    form_model = 'player'
    form_fields = ['reenterlabel']

    def is_displayed(self):
        return not self.player.simulated


class ReEnterLabel2(Page):
    form_model = 'player'
    form_fields = ['reenterlabel2']

    def is_displayed(self):
        return self.player.reenterlabel != self.participant.label and not self.player.simulated


class Final(Page):
    pass


page_sequence = [
    GroupingWaitPage,
    CalculateWaitPage,
    Payoffs,
    TimeoutHappened,
    Payment,
    BankAgain,
    ReEnterLabel,
    ReEnterLabel2,
    Final
]
