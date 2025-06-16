from flask_mail import Message
from flask import url_for
from app import mail
import random

def send_reset_email(user):
    token = user.get_reset_token()
    reset_url = url_for('main.reset_password', token=token, _external=True)

    msg = Message('Réinitialisation de votre mot de passe',
                  sender='noreply@monsite.com',
                  recipients=[user.email])

    msg.body = f'''Bonjour {user.name},

Pour réinitialiser votre mot de passe, veuillez cliquer sur le lien suivant :

{reset_url}

Si vous n'avez pas demandé cette réinitialisation, ignorez cet email.

Cordialement,
L'équipe de support
'''
    mail.send(msg)

def generate_otp():
    return str(random.randint(100000, 999999))