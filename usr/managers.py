import logging

from django.contrib.auth.models import BaseUserManager
from django.utils import timezone

logger = logging.getLogger("ela")


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, national_id, first_name, last_name, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given national_id, email and password.
        """
        logger.debug(
            "national_id='{}', "
            "first_name='{}', "
            "last_name='{}', "
            "email='{}', "
            "is_staff='{}', "
            "is_superuser='{}', "
            "kwargs='{}'".format(
                national_id,
                first_name,
                last_name,
                email,
                is_staff,
                is_superuser,
                extra_fields,
            )
        )
        now = timezone.now()
        if not national_id:
            raise ValueError('The given national_id must be set')
        email = self.normalize_email(email)
        user = self.model(national_id=str(national_id), email=email,
                          is_staff=is_staff, is_active=False,
                          is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, national_id, first_name, last_name, email, password,
                    **extra_fields):

        return self._create_user(national_id, first_name, last_name,
                                 email, password, False, False, **extra_fields)

    def create_superuser(self, national_id, first_name, last_name, email,
                         password, **extra_fields):

        return self._create_user(national_id, first_name, last_name,
                                 email, password, True, True, **extra_fields)
