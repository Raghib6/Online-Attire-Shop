from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self,first_name,last_name,username,email,password=None):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have an username')
        
        user = self.model(
            first_name = first_name,
            last_name  = last_name,
            username   = username,
            email      = self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,first_name,last_name,username,email,password=None):
        user = self.create_user(
        first_name = first_name,
        last_name  = last_name,
        username   = username,
        email      = self.normalize_email(email),
        password   = password,
        )

        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.is_active = True

        user.save(using=self._db)
        return user