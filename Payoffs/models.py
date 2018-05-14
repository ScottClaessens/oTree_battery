from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from django.db import models as djmodels

author = 'Scott Claessens'

doc = """
Payoffs, Matching and Payment
"""


class Constants(BaseConstants):
    name_in_url = 'Payoffs'
    players_per_group = 8
    num_rounds = 1

    fields_with_encryption = [
         'first_name', 'last_name', 'bank_details'
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    def dropouts_and_simulated(self):
        for p in self.get_players():
            # For drop outs and simulated players, set average responses
            #
            # any None in this list means either timeout or simulated player
            l = [p.participant.vars['dg'], p.participant.vars['ug1'], p.participant.vars['ug2'],
                 p.participant.vars['tg1'], p.participant.vars['tg2'], p.participant.vars['secondpp1'],
                 p.participant.vars['secondpp2'], p.participant.vars['secondpp3'], p.participant.vars['thirdpp1'],
                 p.participant.vars['thirdpp2'], p.participant.vars['pgg'], p.participant.vars['staghunt1'],
                 p.participant.vars['staghunt2'], p.participant.vars['staghunt3']]
            # if participant has any missing values (means they MUST have timed out) then we set new
            # values for the group matching process - based on previous data (Rand et al.)
            if any(i is None for i in l) and not p.participant.vars['simulated']:
                p.timeout_happened = True
            elif any(i is None for i in l) and p.participant.vars['simulated']:
                p.simulated = True
            if any(i is None for i in l):
                print("TIMEOUT / SIMULATED PARTICIPANT")  # change these back!!
                p.participant.vars['dg'] = c(0)         # 25
                p.participant.vars['ug1'] = c(0)        # 40
                p.participant.vars['ug2'] = c(100)        # 25
                p.participant.vars['tg1'] = 1            # 2
                p.participant.vars['tg2'] = c(0)        # 75
                p.participant.vars['secondpp1'] = 2      # 1
                p.participant.vars['secondpp2'] = c(50)   # 0
                p.participant.vars['secondpp3'] = c(50)  # 30
                p.participant.vars['thirdpp1'] = 2       # 1
                p.participant.vars['thirdpp2'] = c(100)   # 30
                p.participant.vars['pgg'] = c(0)        # 30
                p.participant.vars['staghunt1'] = 2      # 1
                p.participant.vars['staghunt2'] = c(50)   # 0
                p.participant.vars['staghunt3'] = c(50)  # 30
            else:
                print("COMPLETED PARTICIPANT")

    def calculate_payoffs(self):
        for p in self.get_players():
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
                matching_dg_transfer_to_me = c(self.get_player_by_id(p.id_in_group - 1).participant.vars['dg'])
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
                matching_ug_mao = c(self.get_player_by_id(p.id_in_group + 2).participant.vars['ug2'])
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
                matching_ug_offer = c(self.get_player_by_id(p.id_in_group - 2).participant.vars['ug1'])
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
                    matching_tg_return = c(self.get_player_by_id(p.id_in_group + 2).participant.vars['tg2'])
                else:
                    matching_tg_return = c(self.get_player_by_id(p.id_in_group - 6).participant.vars['tg2'])
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
                    matching_tg_give = self.get_player_by_id(p.id_in_group + 6).participant.vars['tg1']
                elif p.id_in_group in (5, 6):
                    matching_tg_give = self.get_player_by_id(p.id_in_group - 2).participant.vars['tg1']
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
                matching_2pp_pd = self.get_player_by_id(p.id_in_group + 4).participant.vars['secondpp1']
            else:
                matching_2pp_pd = self.get_player_by_id(p.id_in_group - 4).participant.vars['secondpp1']
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
                matching_2pp_puncoop = c(self.get_player_by_id(p.id_in_group + 4).participant.vars['secondpp2'])
                matching_2pp_pundef = c(self.get_player_by_id(p.id_in_group + 4).participant.vars['secondpp3'])
            else:
                matching_2pp_puncoop = c(self.get_player_by_id(p.id_in_group - 4).participant.vars['secondpp2'])
                matching_2pp_pundef = c(self.get_player_by_id(p.id_in_group - 4).participant.vars['secondpp3'])
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
                        self.get_player_by_id(p.id_in_group + 1).participant.vars['thirdpp2'])
                else:
                    matching_3pp_punishment = c(
                        self.get_player_by_id(1).participant.vars['thirdpp2'])
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
                        self.get_player_by_id(p.id_in_group - 1).participant.vars['thirdpp1'])
                else:
                    matching_3pp_take = c(
                        self.get_player_by_id(8).participant.vars['thirdpp1'])
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
                    self.get_player_by_id(q).participant.vars['pgg'])
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
            # Contribute stage
            if p.id_in_group in (1, 3, 5, 7):
                matching_staghunt_action = self.get_player_by_id(((p.id_in_group + 2) % 8) + 1).participant.vars['staghunt1']
            else:
                matching_staghunt_action = self.get_player_by_id((p.id_in_group - 3) % 8).participant.vars['staghunt1']
            p.participant.vars['matching_staghunt_action'] = matching_staghunt_action
            if p.participant.vars['staghunt1'] == 1:
                if matching_staghunt_action == 1:
                    temppayoff = c(130)
                else:
                    temppayoff = c(70)
            else:
                if matching_staghunt_action == 1:
                    temppayoff = c(100)
                else:
                    temppayoff = c(100)
            # Punishment Stage
            if p.id_in_group in (1, 3, 5, 7):
                matching_staghunt_pun1 = self.get_player_by_id(((p.id_in_group + 2) % 8) + 1).participant.vars['staghunt2']
                matching_staghunt_pun2 = self.get_player_by_id(((p.id_in_group + 2) % 8) + 1).participant.vars['staghunt3']
            else:
                matching_staghunt_pun1 = self.get_player_by_id((p.id_in_group - 3) % 8).participant.vars['staghunt2']
                matching_staghunt_pun2 = self.get_player_by_id((p.id_in_group - 3) % 8).participant.vars['staghunt3']
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
            # Set minimum payment to $10 (10.00 * points_conversion) for everyone else
            #
            #
            if p.simulated or p.timeout_happened:
                p.participant.payoff = c(0)
            else:
                if p.participant.payoff.to_real_world_currency(self.session) < 10.00:
                    p.participant.payoff = 10.00 / self.session.config['real_world_currency_per_point']
            #
            #
            # If real participant, save each game payoff from participant.vars directly into models
            # USE THESE to display payoffs to participants on screen (participant.payoff may be more)
            #
            #
            if not p.simulated and not p.timeout_happened:
                p.dg_payoff = p.participant.vars['matching_dg_payoff']
                p.ug_payoff = p.participant.vars['matching_ug_payoff']
                p.tg_payoff = p.participant.vars['matching_tg_payoff']
                p.secondpp_payoff = p.participant.vars['matching_2pp_payoff']
                p.thirdpp_payoff = p.participant.vars['matching_3pp_payoff']
                p.pgg_payoff = p.participant.vars['matching_pgg_payoff']
                p.staghunt_payoff = p.participant.vars['matching_staghunt_payoff']


class Player(BasePlayer):
    dg_payoff = models.CurrencyField()
    ug_payoff = models.CurrencyField()
    tg_payoff = models.CurrencyField()
    secondpp_payoff = models.CurrencyField()
    thirdpp_payoff = models.CurrencyField()
    pgg_payoff = models.CurrencyField()
    staghunt_payoff = models.CurrencyField()

    first_name_cleartext = models.StringField(
        label="Please enter your first name:")
    first_name_encrypted = djmodels.BinaryField(null=True)

    last_name_cleartext = models.StringField(
        label="Please enter your last name:")
    last_name_encrypted = djmodels.BinaryField(null=True)

    bank_details_cleartext = models.StringField(
        label="Please enter your NZ bank account number. We will transfer your reimbursement into this account, so please "
              "make sure it is correct. Please enter it in the following format: 00-0000-0000000-000. You may need to "
              "add a leading zero to the last three digits.")
    bank_details_encrypted = djmodels.BinaryField(null=True)

    correct_details = models.IntegerField(
        label="Are these payment details correct? If not, please let us know and we will get in touch.",
        choices=[
            [1, 'Yes, these details are correct'],
            [0, 'No, these details are not correct']
        ],
        widget=widgets.RadioSelect
    )

    attention = models.IntegerField(
        label="Research shows that people may not pay attention when answering questions. If you are reading this "
              "question, please select the last choice - the one at the very bottom of the list. Thank you for "
              "participating and taking the time to read through the questions carefully. What is this study about?",
        choices=[
            [1, 'Risk taking'],
            [2, 'Economic decisions'],
            [3, 'Managing resources'],
            [4, 'Issues of religion'],
            [5, 'Issues of society'],
            [6, 'Issues of geography']
        ],
        widget=widgets.RadioSelect
    )

    recruitment = models.IntegerField(
        label="Would you like to be contacted about future studies similar to this one?",
        choices=[
            [1, 'Yes'],
            [0, 'No']
        ],
        widget=widgets.RadioSelect
    )

    reenterlabel  = models.StringField(label='Please re-enter your participant label below. '
                                             'This can be found in your original email.')
    reenterlabel2 = models.StringField(label='The participant label you entered does not match the one you entered at '
                                             'the start of the study. Please double-check your email, and try entering '
                                             'the participant label one more time. It is very important that you enter '
                                             'the correct participant label, as we will use this to match your '
                                             'responses here with your previous NZAVS responses.')

    total_payment = models.FloatField()
    timeout_happened = models.BooleanField()
    simulated = models.BooleanField()
