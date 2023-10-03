from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        # create user
        user = self.model(username=username, **extra_fields)
        user.set_password(password)

        # save user instance
        user.save()

        return user
