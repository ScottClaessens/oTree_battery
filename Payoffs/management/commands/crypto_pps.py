
'''
INSTRUCTIONS:

first, run this command locally:

    python manage.py crypto_pps keys

This will create 2 files: public_key.der and private_key.der
add 'public_key.der' to the git repo and push it to the server.
When the study is run, participant personal details (IBAN, BIC, name, etc)
will be encrypted using this public key.

On the other hand, keep private_key.der a secret; the only people who should have this file
are those who have permission to decrypt participant info.

When the study is complete, you should put the private key on the same machine with the database
containing the study info. The simplest way is to move the private key to the server,
but you can also export the postgres DB and load it in a local DB running the same version of oTree,
and make sure the DATABASE_URL env var is pointing to that DB

Then run this:

    python manage.py crypto_pps csv

This will create a CSV with participant info like this:

    participant_code	first_name	last_name	street_no	city	iban	bic
    14tbt9y1	        John	    Williamson	123 Elm St  Bonn	DE89 3704 0044 0532 0130 00	23423   23141412

'''

import os
from Cryptodome.PublicKey import RSA
from Cryptodome import Random
from Cryptodome.Cipher import PKCS1_OAEP
from csv import DictWriter
import sys


from Payoffs.models import Player, Constants
from django.core.management import BaseCommand

PUBLIC_KEY_FILE = 'public_key.der'
PRIVATE_KEY_FILE = 'private_key.der'


def get_public_key():
    if os.path.exists(PUBLIC_KEY_FILE):
        with open(PUBLIC_KEY_FILE, 'rb') as f:
            return RSA.importKey(f.read())


def get_private_key():
    if os.path.exists(PRIVATE_KEY_FILE):
        with open(PRIVATE_KEY_FILE, 'rb') as f:
            return RSA.importKey(f.read())


def generate_keys():
    random_generator = Random.new().read
    key = RSA.generate(1024, random_generator)
    with open(PRIVATE_KEY_FILE, 'wb') as f:
        f.write(key.exportKey('DER'))
    with open(PUBLIC_KEY_FILE, 'wb') as f:
        f.write(key.publickey().exportKey('DER'))


def pps_to_csv():

    private_key = get_private_key()
    cipher_priv = PKCS1_OAEP.new(private_key)

    filename = 'pps.csv'

    with open(filename, 'w', encoding='utf8') as f:
        writer = DictWriter(
            f,
            fieldnames=['participant_code', 'participant_label', 'payment_amount'] + Constants.fields_with_encryption,
            lineterminator='\n')
        writer.writeheader()

        for player in Player.objects.all():
            row = {'participant_code': player.participant.code,
                   'participant_label': player.participant.label,
                   'payment_amount': player.total_payment}
            for f in Constants.fields_with_encryption:
                encrypted_value = getattr(player, '{}_encrypted'.format(f))
                if encrypted_value is None:
                    row[f] = ''
                else:
                    decrypted_value = cipher_priv.decrypt(encrypted_value)
                    unicode_value = decrypted_value.decode('utf-8')
                    row[f] = unicode_value
            writer.writerow(row)

    print('wrote {}'.format(filename))


class Command(BaseCommand):
    help = "keys or csv"

    def add_arguments(self, parser):
        parser.add_argument('command')

    def handle(self, *args, **options):
        if options['command'] == 'keys':
            generate_keys()
        if options['command'] == 'csv':
            pps_to_csv()
