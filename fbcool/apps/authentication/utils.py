from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import login, logout, user_logged_in, user_logged_out
from rest_framework.authtoken.models import Token
#from rest_framework_simplejwt.tokens import RefreshToken
import uuid
def login_user(request, user):
    token, _ = Token.objects.get_or_create(user=user)
    login(request, user)
    user_logged_in.send(sender=user.__class__, request=request, user=user)