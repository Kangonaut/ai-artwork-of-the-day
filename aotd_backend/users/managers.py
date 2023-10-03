from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password):
        # create user
        user = self.model(username=username)
        user.set_password(password)

        # save user instance
        user.save()
        
        return user
