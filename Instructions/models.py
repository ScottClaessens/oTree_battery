from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import time
# from otree.models.session import Session as BaseSession
author = 'Scott Claessens'

doc = """
General Instructions & Randomising App Sequence
"""


class Constants(BaseConstants):
    name_in_url = 'instructions'
    players_per_group = 4
    num_rounds = 1


class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players():
            # Timer = 1 hour (60 * 60 secs)
            p.participant.vars['expiry'] = time.time() + (self.session.config['timer'] * 60)
            p.participant.vars['timeout_happened'] = None
            # Set game number
            p.participant.vars['game_number'] = 0
            #
            # Set empty participant vars
            #
            # Dictator Game
            p.participant.vars['matching_dg_role'] = None
            p.participant.vars['matching_dg_transfer_to_me'] = None
            p.participant.vars['matching_dg_payoff'] = None
            p.participant.vars['dg'] = None
            # Ultimatum Game
            p.participant.vars['matching_ug_role'] = None
            p.participant.vars['matching_ug_mao'] = None
            p.participant.vars['matching_ug_offer'] = None
            p.participant.vars['matching_ug_reject'] = None
            p.participant.vars['matching_ug_payoff'] = None
            p.participant.vars['ug1'] = None
            p.participant.vars['ug2'] = None
            # Trust Game
            p.participant.vars['matching_tg_role'] = None
            p.participant.vars['matching_tg_give'] = None
            p.participant.vars['matching_tg_return'] = None
            p.participant.vars['matching_tg_payoff'] = None
            p.participant.vars['tg1'] = None
            p.participant.vars['tg2'] = None
            # Second-Party Punishment Game
            p.participant.vars['matching_2pp_pd'] = None
            p.participant.vars['matching_2pp_puncoop'] = None
            p.participant.vars['matching_2pp_pundef'] = None
            p.participant.vars['matching_2pp_payoff'] = None
            p.participant.vars['secondpp1'] = None
            p.participant.vars['secondpp2'] = None
            p.participant.vars['secondpp3'] = None
            # Third-Party Punishment Game
            p.participant.vars['matching_3pp_role'] = None
            p.participant.vars['matching_3pp_take'] = None
            p.participant.vars['matching_3pp_punishment'] = None
            p.participant.vars['matching_tg_payoff'] = None
            p.participant.vars['thirdpp1'] = None
            p.participant.vars['thirdpp2'] = None
            # Public Goods Game
            p.participant.vars['matching_pgg_cont1'] = None
            p.participant.vars['matching_pgg_cont2'] = None
            p.participant.vars['matching_pgg_cont3'] = None
            p.participant.vars['matching_pgg_payoff'] = None
            p.participant.vars['pgg'] = None
            # Stag Hunt Game with Punishment
            p.participant.vars['matching_staghunt_action'] = None
            p.participant.vars['matching_staghunt_pun1'] = None
            p.participant.vars['matching_staghunt_pun2'] = None
            p.participant.vars['matching_staghunt_payoff'] = None
            p.participant.vars['staghunt1'] = None
            p.participant.vars['staghunt2'] = None
            p.participant.vars['staghunt3'] = None
            # Stag Hunt (no punishment)
            p.participant.vars['matching_sh_count'] = None
            p.participant.vars['matching_sh_payoff'] = None
            p.participant.vars['sh'] = None


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    sequence_of_apps = models.LongStringField()
    reenterlabel = models.StringField(label='Please re-enter your participant label below. '
                                            'This can be found in your original email.')
