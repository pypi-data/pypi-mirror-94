from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    agreement_granted = models.DateTimeField(_("time of agreement"), editable=False, auto_now=True)
    verified = models.DateTimeField(_("time of verification"), editable=False, null=True)
    verified_by = models.ForeignKey(
        "self",
        editable=False,
        null=True,
        on_delete=models.PROTECT,
        related_name="+",
        verbose_name=_("verified by"),
    )

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
