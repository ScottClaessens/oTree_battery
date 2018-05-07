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
    pass


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
        label="Please enter your NZ bank account number. We will transfer your payment into this account, so please "
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

    reenterlabel  = models.StringField(label='Please re-enter your participant label below. '
                                             'This can be found in your original email.')
    reenterlabel2 = models.StringField(label='The participant label you entered does not match the one you entered at '
                                             'the start of the study. Please double-check your email, and try entering '
                                             'the participant label one more time. It is very important that you enter '
                                             'the correct participant label, as we will use this to match your '
                                             'responses here with your previous NZAVS responses.')

    total_payment = models.FloatField()
    timeout_happened = models.BooleanField()
    timeout_game_number = models.IntegerField()
    simulated = models.BooleanField()
