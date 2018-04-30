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
         'payment_method', 'email', 'name', 'bank_details', 'postal_address',
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    payment_method_cleartext = models.IntegerField(
        label="Please specify below which payment method you would prefer.",
        choices=[
            [1, 'PayPal'],
            [2, 'Direct online bank transfer'],
            [3, 'Postal cheque']
        ],
        initial=None,
        widget=widgets.RadioSelect)
    payment_method_encrypted = djmodels.BinaryField(null=True)

    email_cleartext = models.StringField(
        label="Please enter your PayPal registered email address. We will use this email address to process "
              "your PayPal payment, so please make sure it is correct.", initial=None)
    email_encrypted = djmodels.BinaryField(null=True)

    name_cleartext = models.StringField(
        label="Please enter your full name.", initial=None)
    name_encrypted = djmodels.BinaryField(null=True)

    bank_details_cleartext = models.StringField(
        label="Please enter your NZ bank account number. We will transfer your payment into this account, so please "
              "make sure it is correct.", initial=None)
    bank_details_encrypted = djmodels.BinaryField(null=True)

    postal_address_cleartext = models.LongStringField(
        label="Please enter your full NZ postal address, including postcode. We will send your cheque to this address, "
              "so please make sure it is correct.", initial=None)
    postal_address_encrypted = djmodels.BinaryField(null=True)

    timeout_happened = models.BooleanField()
    timeout_game_number = models.IntegerField()
    simulated = models.BooleanField()