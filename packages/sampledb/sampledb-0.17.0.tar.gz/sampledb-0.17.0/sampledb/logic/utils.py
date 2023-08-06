# coding: utf-8
"""

"""

import smtplib

import flask
import flask_mail

from .. import mail, db
from .security_tokens import generate_token
from ..models import Authentication, AuthenticationType, User


def send_user_invitation_email(email, invitation_id):
    token_data = {
        'email': email,
        'invitation_id': invitation_id
    }
    token = generate_token(
        token_data,
        salt='invitation',
        secret_key=flask.current_app.config['SECRET_KEY']
    )
    confirm_url = flask.url_for('frontend.invitation_route', token=token, _external=True)

    service_name = flask.current_app.config['SERVICE_NAME']
    subject = service_name + " Invitation"
    html = flask.render_template('mails/user_invitation.html', confirm_url=confirm_url)
    text = flask.render_template('mails/user_invitation.txt', confirm_url=confirm_url)
    while '\n\n\n' in text:
        text = text.replace('\n\n\n', '\n\n')
    try:
        mail.send(flask_mail.Message(
            subject,
            sender=flask.current_app.config['MAIL_SENDER'],
            recipients=[email],
            body=text,
            html=html
        ))
    except smtplib.SMTPRecipientsRefused:
        pass


def send_email_confirmation_email(email, user_id, salt):
    token_data = {
        'email': email,
        'user_id': user_id
    }
    token = generate_token(
        token_data,
        salt=salt,
        secret_key=flask.current_app.config['SECRET_KEY']
    )
    confirm_url = flask.url_for("frontend.user_preferences", user_id=user_id, token=token, _external=True)

    service_name = flask.current_app.config['SERVICE_NAME']
    subject = service_name + " Email Confirmation"
    html = flask.render_template('mails/email_confirmation.html', confirm_url=confirm_url)
    text = flask.render_template('mails/email_confirmation.txt', confirm_url=confirm_url)
    while '\n\n\n' in text:
        text = text.replace('\n\n\n', '\n\n')
    try:
        mail.send(flask_mail.Message(
            subject,
            sender=flask.current_app.config['MAIL_SENDER'],
            recipients=[email],
            body=text,
            html=html
        ))
    except smtplib.SMTPRecipientsRefused:
        pass


def send_recovery_email(email):
    users = User.query.filter_by(email=email).all()
    email_authentication = Authentication.query.filter(db.and_(Authentication.login['login'].astext == email, Authentication.type == AuthenticationType.EMAIL)).first()
    if email_authentication is not None and email_authentication.user not in users:
        users.append(email_authentication.user)

    if not users:
        return

    password_reset_urls = {}
    for user in users:
        for authentication_method in user.authentication_methods:
            if authentication_method.type != AuthenticationType.LDAP:
                password_reset_urls[authentication_method] = build_confirm_url(authentication_method)

    service_name = flask.current_app.config['SERVICE_NAME']
    subject = service_name + " Account Recovery"
    html = flask.render_template('mails/account_recovery.html', email=email, users=users, password_reset_urls=password_reset_urls)
    text = flask.render_template('mails/account_recovery.txt', email=email, users=users, password_reset_urls=password_reset_urls)
    while '\n\n\n' in text:
        text = text.replace('\n\n\n', '\n\n')
    try:
        mail.send(flask_mail.Message(
            subject,
            sender=flask.current_app.config['MAIL_SENDER'],
            recipients=[email],
            body=text,
            html=html
        ))
    except smtplib.SMTPRecipientsRefused:
        pass


def build_confirm_url(authentication_method, salt='password'):
    assert authentication_method.type != AuthenticationType.LDAP

    user_id = authentication_method.user_id
    token = generate_token(authentication_method.id, salt=salt,
                           secret_key=flask.current_app.config['SECRET_KEY'])
    return flask.url_for("frontend.user_preferences", user_id=user_id, token=token, _external=True)
