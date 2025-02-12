from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.services.audit_service import AuditService

User = get_user_model()


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Created at")
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Updated at")
    )

    class Meta:
        abstract = True


class AuditMixin(TimeStampedModel):
    """
    Abstract model to track creation and update timestamps,
    along with the user who created or last modified the record.
    """

    created_by = models.ForeignKey(
        get_user_model(),
        related_name="%(class)s_created",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
        verbose_name=_("Created by"),
    )

    updated_by = models.ForeignKey(
        get_user_model(),
        related_name="%(class)s_updated",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
        verbose_name=_("Updated by"),
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        audit_service = AuditService(self)
        audit_service.set_audit_fields()
        super().save(*args, **kwargs)
