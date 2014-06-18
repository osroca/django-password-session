from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from hashlib import md5

PASSWORD_HASH_KEY = getattr(settings, 'PASSWORD_SESSION_PASSWORD_HASH_KEY', 'password_session_password_hash_key')


def get_password_hash(user):
    """Returns a string of crypted password hash"""
    return md5(
        md5(user.password.encode()).hexdigest().encode() + settings.SECRET_KEY.encode()
    ).hexdigest()


def update_session_auth_hash(request, user):
    """Updates crypted password hash to session"""
    if request.user == user:
        request.session[PASSWORD_HASH_KEY] = get_password_hash(user)


@receiver(user_logged_in)
def on_login(sender, user, request, **kwargs):
    """Saves password hash in session"""
    update_session_auth_hash(request, user)