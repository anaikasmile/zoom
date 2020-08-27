from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import login, authenticate
from .models import User
class LoginBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
          if '@' in username:
              kwargs = {'email': username}
          else:
              kwargs = {'tel': username}
          try:
              user = User.objects.get(**kwargs)
              if user.check_password(password):
                  return user
          except User.DoesNotExist:
              return None

    def get_user(self, username):
        try:
            return User.objects.get(pk=username)
        except User.DoesNotExist:
            return None