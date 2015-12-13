from __future__ import unicode_literals
from django import forms
from usr.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from ela.sites import main_admin_site
from account.models import Account, SignupCode, AccountDeletion, EmailAddress


class UserCreationForm(forms.ModelForm):
    """
    form for user creation and only get necessary fields
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput,
                                help_text=_(
                                    "Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ("national_id", "first_name", "last_name", "email")

    def clean_password2(self):
        """
        check both password fields to be same
        :return: password
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            "Raw passwords are not stored, so there is no way to see "
            "this user's password, but you can change the password "
            "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = User
        fields = '__all__'

    def clean_password(self):
        """
        Regardless of what the user provides, return the initial value.
        This is done here, rather than on the field, because the
        field does not have access to the initial value
        """
        return self.initial["password"]


class UsrAdmin(UserAdmin):
    # change_user_password_template = None  # TODO: add reset user password feature
    form = UserChangeForm
    add_form = UserCreationForm

    suit_form_tabs = (('general', 'General'),
                      ('personal-info', 'Personal info'),
                      ('permissions', 'Permissions'))

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('national_id', 'first_name', 'last_name', 'email',
                       'password1', 'password2'),
        }),
    )
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general',),
            'fields': ('last_login', 'national_id', 'password')
        }),
        (_('Personal info'), {
            'classes': ('suit-tab', 'suit-tab-personal-info',),
            'fields': ('photo', 'first_name', 'last_name', 'email')
        }),
        (_('Permissions'), {
            'classes': ('suit-tab', 'suit-tab-permissions',),
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups',
                       'user_permissions')
        }),
        # (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    # change_password_form = AdminPasswordChangeForm
    list_display = ('national_id', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('first_name', 'last_name', 'national_id')
    ordering = ('date_joined',)
    filter_horizontal = ()
    readonly_fields = ['last_login']


class SignupCodeAdmin(admin.ModelAdmin):
    list_display = ["code", "max_uses", "use_count", "expiry", "created"]
    search_fields = ["code", "email"]
    list_filter = ["created"]
    raw_id_fields = ["inviter"]


class AccountAdmin(admin.ModelAdmin):
    raw_id_fields = ["user"]


class AccountDeletionAdmin(AccountAdmin):
    list_display = ["email", "date_requested", "date_expunged"]


class EmailAddressAdmin(AccountAdmin):
    list_display = ["user", "email", "verified", "primary"]
    search_fields = ["email", "user__username"]
    list_filter = ["user"]


main_admin_site.register(User, UsrAdmin)
main_admin_site.register(Account, AccountAdmin)
main_admin_site.register(SignupCode, SignupCodeAdmin)
main_admin_site.register(AccountDeletion, AccountDeletionAdmin)
main_admin_site.register(EmailAddress, EmailAddressAdmin)
