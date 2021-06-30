from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):

    def create_user(self, email, phone, password=None, **extra_fields):

        if not phone:
            raise ValueError(_('The phone must be set'))

        if not email:
            raise ValueError(_('The email must be set'))

        user = self.model(
            email=self.normalize_email(email),
            phone=phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, password=None, name=None):

        user = self.create_user(
            email,
            password=password,
            phone=phone,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
