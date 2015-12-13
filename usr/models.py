import os
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin)
# from django.contrib.auth.models import Group as MasterGroup
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html
from django.utils import timezone
from django.conf import settings
from usr.storage import OverwriteStorage
from usr.validators import national_id_validator
from usr.hooks import ProfilePicturePathHook
from usr.managers import UserManager


# I need to know the reason of having a Group class here, instead of using
# original django.contrib.auth.models.Group ? please explain it, here.
#
# class Group(MasterGroup):
#     pass


class User(AbstractBaseUser, PermissionsMixin):
    """
    main user class which inherit from AbstractBaseUser and implements some
    features.
    """
    national_id = models.CharField(
        _('national ID (username)'),
        max_length=10,
        unique=True,
        validators=[national_id_validator]
    )
    first_name = models.CharField(
        _('first name'),
        max_length=30
    )
    last_name = models.CharField(
        _('last name'),
        max_length=30
    )
    email = models.EmailField(
        _('email address')
    )
    picture = models.ImageField(
        _('profile picture'),
        upload_to=ProfilePicturePathHook("avatars"),
        storage=OverwriteStorage(),
        null=True,
        blank=True
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into staff site.')
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Designates whether this user should be treated as active. '
                    'Unselect this instead of deleting accounts.')
    )
    date_joined = models.DateTimeField(
        _('date joined'),
        default=timezone.now
    )

    objects = UserManager()

    USERNAME_FIELD = 'national_id'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def get_full_name(self):
        """
        :return: the first_name plus the last_name, with a space in between.
        """
        full_name = '{} {}'.format(self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        :return: the short name for the user.
        """
        return self.first_name

    @property
    def picture_url(self):
        """
        :return: the url of image profile for user
        """
        if self.picture:
            return self.picture.url
        else:
            return os.path.join(settings.MEDIA_URL, 'avatars/0.png')

    @property
    def thumbnail(self):
        """
        :return:the thumbnail html for 80x80 picture
        """
        return format_html('<img src="{}" class="img-thumbnail"'
                           ' width="80" height="80">', self.get_image_url)

    # thumbnail.short_description = _("Thumbnail")

    full_name = property(get_full_name)
    short_name = property(get_short_name)

    def __unicode__(self):
        return self.get_full_name()

    def __repr__(self):
        return "<usr.User(" \
               "national_id='{}', " \
               "first_name='{}', " \
               "last_name='{}, " \
               "email='{}', " \
               "picture='{}', " \
               "is_staff='{}', " \
               "is_active='{}', " \
               "date_joined='{}')>".format \
                (
                self.national_id,
                self.first_name,
                self.last_name,
                self.email,
                self.picture,
                self.is_staff,
                self.is_active,
                self.date_joined)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


# admin_user = User.objects.get(is_superuser=True)


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL
    )
    fathers_name = models.CharField(
        _('fathers name'),
        max_length=30,
    )
    birth_date = models.DateField(
        _('birth date')
    )
    phone_number = models.CharField(
        _('phone number'),
        max_length=20,
        null=True,
        blank=False,
    )
    home_phone = models.CharField(
        _('home phone'),
        max_length=20,
        null=True,
        blank=True,
    )
    home_address = models.TextField(
        _('home address'),
        max_length=100,
        null=True,
        blank=False,
    )
    MALE = 1
    FEMALE = 2
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    gender = models.IntegerField(
        _('gender'),
        choices=GENDER_CHOICES,
        null=True,
        blank=False,
    )
    description = models.TextField(
        _('description'),
        null=True,
        blank=True,
        max_length=150,
    )

    WEBSITE = 1
    TRAKT = 2
    FRIENDS = 3
    OTHER = 4
    ACQUAINTANCE_WAY_CHOICES = (
        (WEBSITE, 'Website'),
        (TRAKT, 'Trakt'),
        (FRIENDS, 'Friends'),
        (OTHER, 'Other')
    )
    acquaintance_way = models.IntegerField(
        _('How did you find "ela"?'),
        choices=ACQUAINTANCE_WAY_CHOICES,
        default=WEBSITE,
        null=True,
        blank=True,
    )

    def __unicode__(self):
        return "{}'s Profile".format(self.user.full_name)

    def __repr__(self):
        return "<usr.UserProfile(" \
               "user='{}', " \
               "gender='{}', " \
               "fathers_name='{}', " \
               "birth_date='{}', " \
               "phone_number='{}', " \
               "home_phone='{}', " \
               "home_address='{}', " \
               "acquaintance_way='{}', " \
               "description='{}')>".format \
                (
                self.user,
                dict(
                    UserProfile.GENDER_CHOICES).get(
                    self.gender, "Unknown gender"
                ),
                self.fathers_name,
                self.birth_date,
                self.phone_number,
                self.home_phone,
                self.home_address,
                dict(
                    UserProfile.ACQUAINTANCE_WAY_CHOICES).get(
                    self.acquaintance_way, "Unknown acquaintance_way"
                ),
                self.description)
