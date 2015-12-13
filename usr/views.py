from account.views import (SignupView as AccountSignupView,
                           LoginView as AccountLoginView)
from usr.forms import SignupForm
from usr.models import UserProfile, User
from account import signals
from pinax.notifications.models import send
import logging

logger = logging.getLogger("ela")


class SignupView(AccountSignupView):
    form_class = SignupForm

    def create_user(self, form, commit=True, **kwargs):
        logger.debug(
            "form='{}', commit='{}', kwargs='{}'".format(form, commit, kwargs))

        user = super(SignupView, self).create_user(form, commit=False, **kwargs)
        user.national_id = form.cleaned_data['username']
        if commit:
            user.save()
        return user

    def update_profile(self, form):
        logger.debug("form={}".format(form))

        UserProfile.objects.create(
            user=self.created_user,
            birth_date=form.cleaned_data["birth_date"],
            fathers_name=form.cleaned_data["fathers_name"],
        )

    def after_signup(self, form):
        logger.debug("form={}".format(form))

        self.update_profile(form)
        admin = User.objects.filter(is_superuser=True)
        # send([admin], "signup_user")
        super(SignupView, self).after_signup(form)


class LoginView(AccountLoginView):
    """
    Currently extending "AccountLoginView" on wuser/views.py "Loginview" is not
    really meaningful.

    Idea of using signals appears better, but i feel there gonna be use cases
    of extending "AccountLoginView" in future, so i left the implementation here
    """

    def after_login(self, form):
        logger.debug("form={}".format(form))

        signals.user_logged_in.send(sender=LoginView, user=form.user, form=form)
