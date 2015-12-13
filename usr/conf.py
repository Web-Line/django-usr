from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
import logging

logger = logging.getLogger("ela")


def create_notice_types(sender, **kwargs):
    """
    define NoticeType for this app
    """
    if "pinax.notifications" in settings.INSTALLED_APPS:
        from pinax.notifications.models import NoticeType
        logger.debug("Creating notices for ela")
        NoticeType.create(
            "signup_user",
            _("User Signup"),
            _("an user join to ela")
        )
    # ... for more notice type
    else:
        logger.debug("Skipping creation of NoticeTypes as notification app not "
                     "found")


def handle_post_migrate(sender, **kwargs):
    """
    documentation is needed here.
    :param sender:
    :param kwargs:
    :return:
    """

    create_notice_types(sender)


class UsrAppConfig(AppConfig):
    name = 'usr'
    verbose_name = _("Authentication")

    def ready(self):
        post_migrate.connect(handle_post_migrate)
        from usr.signals import handle_user_logged_in
