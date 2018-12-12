from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from django.db import models as djmodels
import random

author = 'Scott Claessens'

doc = """
Payoffs, Matching and Payment
"""


class Constants(BaseConstants):
    name_in_url = 'Payoffs'
    players_per_group = None
    num_rounds = 1

    fields_with_encryption = [
         'first_name', 'last_name', 'bank_details'
    ]


class Subsession(BaseSubsession):
    def dropouts_and_simulated(self):
        for p in self.get_players():
            # For drop outs and simulated players, set average responses
            #
            # any None in this list means either timeout or simulated player
            l = [p.participant.vars['dg'], p.participant.vars['ug1'], p.participant.vars['ug2'],
                 p.participant.vars['tg1'], p.participant.vars['tg2'], p.participant.vars['secondpp1'],
                 p.participant.vars['secondpp2'], p.participant.vars['secondpp3'], p.participant.vars['thirdpp1'],
                 p.participant.vars['thirdpp2'], p.participant.vars['pgg'], p.participant.vars['staghunt1'],
                 p.participant.vars['staghunt2'], p.participant.vars['staghunt3'], p.participant.vars['sh']]
            # if participant has any missing values (means they MUST have timed out) then we set new
            # values for the matching process - based on previous data (Rand et al.)
            if any(i is None for i in l) and not p.participant.vars['simulated']:
                p.timeout_happened = True
            elif any(i is None for i in l) and p.participant.vars['simulated']:
                p.simulated = True
            if any(i is None for i in l):
                print("TIMEOUT / SIMULATED PARTICIPANT")
                p.participant.vars['dg'] = c(25)         # 25
                p.participant.vars['ug1'] = c(40)        # 40
                p.participant.vars['ug2'] = c(25)        # 25
                p.participant.vars['tg1'] = 1            # 1
                p.participant.vars['tg2'] = c(75)        # 75
                p.participant.vars['secondpp1'] = 1      # 1
                p.participant.vars['secondpp2'] = c(0)   # 0
                p.participant.vars['secondpp3'] = c(30)  # 30
                p.participant.vars['thirdpp1'] = 1       # 1
                p.participant.vars['thirdpp2'] = c(30)   # 30
                p.participant.vars['pgg'] = c(30)        # 30
                p.participant.vars['staghunt1'] = 1      # 1
                p.participant.vars['staghunt2'] = c(0)   # 0
                p.participant.vars['staghunt3'] = c(30)  # 30
                p.participant.vars['sh'] = 1             # 1
            else:
                print("COMPLETED PARTICIPANT")

    def shuffle_groups_and_calculate_payoffs(self):
        functions = [
            self.calculate_shpun_payoffs,
            self.calculate_sh_payoffs,
            self.calculate_tg_payoffs,
            self.calculate_pgg_payoffs,
            self.calculate_ug_payoffs,
            self.calculate_dg_payoffs,
            self.calculate_3pp_payoffs,
            self.calculate_2pp_payoffs,
        ]
        # initial groups of 4
        m = self.get_group_matrix()
        random.shuffle(m[0])
        m = [m[0][x:x+4] for x in range(0, len(m[0]), 4)]
        self.set_group_matrix(m)
        # shuffling
        shuffle_list = []
        for f in functions:
            self.group_randomly()
            matrix = self.get_group_matrix()
            shuffle_list.append(f)
            shuffle_list.append(matrix)
            f()
        p = self.get_players()[0]
        p.shuffle_list = str(shuffle_list)
        for p in self.get_players():
            #
            # Set payoffs back to zero for simulated players and timeouts
            # Set minimum payment to $10 (10.00 * points_conversion) for everyone else
            #
            if p.simulated or p.timeout_happened:
                p.participant.payoff = c(0)
            else:
                if p.participant.payoff.to_real_world_currency(self.session) < 10.00:
                    p.participant.payoff = 10.00 / self.session.config['real_world_currency_per_point']
            #
            # If real participant, save each game payoff from participant.vars directly into models
            # USE THESE to display payoffs to participants on screen (participant.payoff may be more)
            #
            if not p.simulated and not p.timeout_happened:
                p.dg_payoff = p.participant.vars['matching_dg_payoff']
                p.ug_payoff = p.participant.vars['matching_ug_payoff']
                p.tg_payoff = p.participant.vars['matching_tg_payoff']
                p.secondpp_payoff = p.participant.vars['matching_2pp_payoff']
                p.thirdpp_payoff = p.participant.vars['matching_3pp_payoff']
                p.pgg_payoff = p.participant.vars['matching_pgg_payoff']
                p.staghunt_payoff = p.participant.vars['matching_staghunt_payoff']
                p.sh_payoff = p.participant.vars['matching_sh_payoff']

    def calculate_dg_payoffs(self):
        # DICTATOR GAME
        for g in self.get_groups():
            for p in g.get_players():
                if p.id_in_group in (1, 3):
                    # Person A
                    p.participant.vars['matching_dg_role'] = 'Person A'
                    p.participant.vars['matching_dg_payoff'] = c(100) - c(p.participant.vars['dg'])
                    p.participant.payoff += c(100) - c(p.participant.vars['dg'])
                else:
                    # Person B
                    p.participant.vars['matching_dg_role'] = 'Person B'
                    matching_dg_transfer_to_me = c(g.get_player_by_id(p.id_in_group - 1).participant.vars['dg'])
                    p.participant.vars['matching_dg_transfer_to_me'] = matching_dg_transfer_to_me
                    p.participant.vars['matching_dg_payoff'] = matching_dg_transfer_to_me
                    p.participant.payoff += matching_dg_transfer_to_me

    def calculate_ug_payoffs(self):
        # ULTIMATUM GAME
        for g in self.get_groups():
            for p in g.get_players():
                if p.id_in_group in (1, 3):
                    # Person A
                    p.participant.vars['matching_ug_role'] = 'Person A'
                    matching_ug_mao = c(g.get_player_by_id(p.id_in_group + 1).participant.vars['ug2'])
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
                    matching_ug_offer = c(g.get_player_by_id(p.id_in_group - 1).participant.vars['ug1'])
                    p.participant.vars['matching_ug_offer'] = matching_ug_offer
                    if matching_ug_offer < p.participant.vars['ug2']:
                        p.participant.vars['matching_ug_reject'] = True
                        p.participant.vars['matching_ug_payoff'] = c(0)
                        p.participant.payoff += c(0)
                    else:
                        p.participant.vars['matching_ug_reject'] = False
                        p.participant.vars['matching_ug_payoff'] = matching_ug_offer
                        p.participant.payoff += matching_ug_offer

    def calculate_tg_payoffs(self):
        # TRUST GAME
        for g in self.get_groups():
            for p in g.get_players():
                if p.id_in_group in (1, 3):
                    # Person A
                    p.participant.vars['matching_tg_role'] = 'Person A'
                    matching_tg_return = c(g.get_player_by_id(p.id_in_group + 1).participant.vars['tg2'])
                    p.participant.vars['matching_tg_return'] = matching_tg_return
                    if p.participant.vars['tg1'] == 0:
                        p.participant.vars['matching_tg_payoff'] = c(50)
                        p.participant.payoff += c(50)
                    else:
                        p.participant.vars['matching_tg_payoff'] = matching_tg_return
                        p.participant.payoff += matching_tg_return
                else:
                    # Person B
                    p.participant.vars['matching_tg_role'] = 'Person B'
                    matching_tg_give = g.get_player_by_id(p.id_in_group - 1).participant.vars['tg1']
                    p.participant.vars['matching_tg_give'] = matching_tg_give
                    if matching_tg_give == 0:
                        p.participant.vars['matching_tg_payoff'] = c(50)
                        p.participant.payoff += c(50)
                    else:
                        p.participant.vars['matching_tg_payoff'] = c(200) - p.participant.vars['tg2']
                        p.participant.payoff += c(200) - p.participant.vars['tg2']

    def calculate_2pp_payoffs(self):
        # SECOND PARTY PUNISHMENT GAME
        for g in self.get_groups():
            for p in g.get_players():
                # Partner?
                if p.id_in_group in (1, 3):
                    partner = g.get_player_by_id(p.id_in_group + 1)
                else:
                    partner = g.get_player_by_id(p.id_in_group - 1)
                # Transfer stage
                matching_2pp_pd = partner.participant.vars['secondpp1']
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
                matching_2pp_puncoop = c(partner.participant.vars['secondpp2'])
                matching_2pp_pundef = c(partner.participant.vars['secondpp3'])
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

    def calculate_3pp_payoffs(self):
        # THIRD PARTY PUNISHMENT GAME
        for g in self.get_groups():
            for p in g.get_players():
                if p.id_in_group in (1, 3):
                    # Person A
                    p.participant.vars['matching_3pp_role'] = 'Person A'
                    matching_3pp_punishment = c(g.get_player_by_id(p.id_in_group + 1).participant.vars['thirdpp2'])
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
                    matching_3pp_take = c(g.get_player_by_id(p.id_in_group - 1).participant.vars['thirdpp1'])
                    p.participant.vars['matching_3pp_take'] = matching_3pp_take
                    if matching_3pp_take == 1:
                        p.participant.vars['matching_3pp_payoff'] = c(100)
                        p.participant.payoff += c(100)
                    else:
                        p.participant.vars['matching_3pp_payoff'] = c(100) - (p.participant.vars['thirdpp2'] / 5)
                        p.participant.payoff += c(100) - (p.participant.vars['thirdpp2'] / 5)

    def calculate_pgg_payoffs(self):
        # PUBLIC GOODS GAME
        for g in self.get_groups():
            for p in g.get_players():
                others = p.get_others_in_group()
                i = 0
                for q in others:
                    i += 1
                    p.participant.vars['matching_pgg_cont%i' % i] = c(q.participant.vars['pgg'])
                total = p.participant.vars['matching_pgg_cont1'] + \
                         p.participant.vars['matching_pgg_cont2'] + \
                         p.participant.vars['matching_pgg_cont3'] + \
                         p.participant.vars['pgg']
                p.participant.vars['matching_pgg_payoff'] = c(100) - p.participant.vars['pgg'] + c(total / 2)
                p.participant.payoff += c(100) - p.participant.vars['pgg'] + c(total / 2)

    def calculate_sh_payoffs(self):
        # STAG HUNT
        for g in self.get_groups():
            i = 0
            for p in g.get_players():
                if p.participant.vars['sh'] == 1:
                    i += 1
            for p in g.get_players():
                p.participant.vars['matching_sh_count'] = i
                if i == 4:
                    payoff = c(80)
                else:
                    if p.participant.vars['sh'] == 1:
                        payoff = c(20)
                    else:
                        payoff = c(50)
                p.participant.vars['matching_sh_payoff'] = payoff
                p.participant.payoff += payoff

    def calculate_shpun_payoffs(self):
        # STAG HUNT WITH PUNISHMENT
        for g in self.get_groups():
            for p in g.get_players():
                # Partner?
                if p.id_in_group in (1, 3):
                    partner = g.get_player_by_id(p.id_in_group + 1)
                else:
                    partner = g.get_player_by_id(p.id_in_group - 1)
                # Contribute stage
                matching_staghunt_action = partner.participant.vars['staghunt1']
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
                matching_staghunt_pun1 = partner.participant.vars['staghunt2']
                matching_staghunt_pun2 = partner.participant.vars['staghunt3']
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


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    shuffle_list = models.LongStringField()
    dg_payoff = models.CurrencyField()
    ug_payoff = models.CurrencyField()
    tg_payoff = models.CurrencyField()
    secondpp_payoff = models.CurrencyField()
    thirdpp_payoff = models.CurrencyField()
    pgg_payoff = models.CurrencyField()
    staghunt_payoff = models.CurrencyField()
    sh_payoff = models.CurrencyField()

    first_name_cleartext = models.StringField(
        label="Please enter your first name:")
    first_name_encrypted = djmodels.BinaryField(null=True)

    last_name_cleartext = models.StringField(
        label="Please enter your last name:")
    last_name_encrypted = djmodels.BinaryField(null=True)

    bank_details_cleartext = models.StringField(
        label="Please enter your NZ bank account number. We will transfer your reimbursement into this account, so please "
              "make sure it is correct. Please enter it in the following format: 00-0000-0000000-000. This is two "
              "numbers, followed by four numbers, followed by seven numbers, followed by three numbers. Dashes are "
              "required between the numbers. If your bank account number ends with two digits, you will need to add "
              "a leading zero (for example, 12 becomes 012).")
    bank_details_encrypted = djmodels.BinaryField(null=True)

    correct_details = models.IntegerField(
        label="Are these details correct? If not, please let us know and we will get in touch.",
        choices=[
            [1, 'Yes, these details are correct'],
            [0, 'No, these details are not correct']
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

    understand = models.IntegerField(
        label="How clear were the instructions for the tasks?",
        choices=[
            [7, 'Extremely clear'],
            [6, 'Moderately clear'],
            [5, 'Slightly clear'],
            [4, 'Neither clear or unclear'],
            [3, 'Slightly unclear'],
            [2, 'Moderately unclear'],
            [1, 'Extremely unclear']
        ],
        widget=widgets.RadioSelect
    )

    feedback = models.LongStringField(
        blank=True,
        label="If you would like to leave us any feedback about this study, please do so below"
    )

    reenterlabel = models.StringField(label='Please re-enter your participant label below. '
                                             'This can be found in your original email.')
    reenterlabel2 = models.StringField(label='The participant label you entered does not match the one you entered at '
                                             'the start of the study. Please double-check your email, and try entering '
                                             'the participant label one more time. It is very important that you enter '
                                             'the correct participant label, as we will use this to match your '
                                             'responses here with your previous NZAVS responses.')

    total_payment = models.CurrencyField()
    overall_time_spent = models.IntegerField()
    game_only_time_spent = models.IntegerField()
    timeout_happened = models.BooleanField(initial=False)
    simulated = models.BooleanField(initial=False)

    def payoff_vars(self):
        return {'sequence_of_apps': self.participant.vars['sequence_of_apps'][1:9],
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
                # Stag Hunt Game
                'matching_sh_count': self.participant.vars['matching_sh_count'],
                'matching_sh_payoff': self.participant.vars['matching_sh_payoff'],
                'sh': self.participant.vars['sh'],
                # Overall
                'overall_payoff': self.dg_payoff + self.pgg_payoff + self.secondpp_payoff + \
                                  self.staghunt_payoff + self.tg_payoff + self.thirdpp_payoff + \
                                  self.ug_payoff + self.sh_payoff,
                'overall_bonus_cash': self.participant.payoff.to_real_world_currency(self.session),
                'payoff_plus_participation_fee': self.participant.payoff_plus_participation_fee()
                }
