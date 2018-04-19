from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class GroupingWaitPage(WaitPage):
    group_by_arrival_time = True

    def after_all_players_arrive(self):
        for p in self.group.get_players():
            #
            #
            # Dictator Game
            #
            #
            if p.id_in_group in (1, 3, 5, 7):
                # Player A
                p.participant.vars['matching_dg_role'] = 'Player A'
                p.participant.vars['matching_dg_payoff'] = c(100) - c(p.participant.vars['dg'])
                p.participant.payoff += c(100) - c(p.participant.vars['dg'])
            else:
                # Player B
                p.participant.vars['matching_dg_role'] = 'Player B'
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
                # Player A
                p.participant.vars['matching_ug_role'] = 'Player A'
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
                # Player B
                p.participant.vars['matching_ug_role'] = 'Player B'
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
                # Player A
                p.participant.vars['matching_tg_role'] = 'Player A'
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
                # Player B
                p.participant.vars['matching_tg_role'] = 'Player B'
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
            p.participant.vars['matching_2pp_payoff'] = temppayoff
            p.participant.payoff += temppayoff
            #
            #
            # Third-Party Punishment
            #
            #
            if p.id_in_group in (2, 4, 6, 8):
                # Player A
                p.participant.vars['matching_3pp_role'] = 'Player A'
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
                # Player C
                p.participant.vars['matching_3pp_role'] = 'Player C'
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


class Payoffs(Page):
    def vars_for_template(self):
        return {'sequence_of_apps': self.participant.vars['sequence_of_apps'][1:7],
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
                'overall_payoff': self.participant.payoff,
                }


page_sequence = [
    GroupingWaitPage,
    Payoffs
]
