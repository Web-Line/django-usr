from django.dispatch import receiver
from account.signals import user_logged_in
from usr.views import LoginView
import logging

logger = logging.getLogger("ela")

# @receiver(post_save, sender=User)
# def handle_user_save(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)


@receiver(user_logged_in, sender=LoginView)
def handle_user_logged_in(sender, **kwargs):
    logger.debug("kwargs={}".format(kwargs))