from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.utils.translation import ugettext_lazy as _
from usr.models import UserProfile
from django.core.validators import RegexValidator
import account.forms
from usr.validators import national_id_validator


class SignupForm(account.forms.SignupForm):
    photo = forms.ImageField(
        required=False
    )
    first_name = forms.CharField(
        required=True,
        max_length=30
    )
    last_name = forms.CharField(
        required=True,
        max_length=30
    )
    fathers_name = forms.CharField()
    gender = forms.ChoiceField(
        label=_('gender'),
        choices=UserProfile.GENDER_CHOICES,
        required=True
    )
    birth_date = forms.DateField(
        widget=SelectDateWidget(years=range(1910, 1991))
    )
    phone_number = forms.CharField(
        label=_('Phone number'),
        validators=[RegexValidator(
            regex='^\d*$',
            message=_('not correct, only numbers'))
        ],
        max_length=20,
        required=True
    )
    home_phone = forms.CharField(
        label=_('home phone'),
        validators=[RegexValidator(
            regex='^\d*$', message=_('not correct, only numbers'))
        ],
        max_length=20
    )
    home_address = forms.CharField(
        label=_('home address'),
        max_length=100
    )
    acquaintance_way = forms.ChoiceField(
        label=_('acquaintance way'),
        choices=UserProfile.ACQUAINTANCE_WAY_CHOICES,
        required=True
    )
    description = forms.CharField(
        label=_('description'),
        max_length=150
    )

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "National ID"
