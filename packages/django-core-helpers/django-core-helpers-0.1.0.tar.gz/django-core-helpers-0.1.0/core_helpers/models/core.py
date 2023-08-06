import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core_helpers.managers import ActiveDeleteManager, ActiveManager, DeletedManager


class UUIDModel(models.Model):
    """Abstract `UUID` model."""

    id = models.UUIDField(_("ID"), default=uuid.uuid4, primary_key=True, editable=False)

    class Meta:
        abstract = True


class ActiveUUIDModel(UUIDModel):
    """Abstract `Active UUID` model."""

    is_active = models.BooleanField(_("Is active?"), default=True)

    class Meta:
        abstract = True


class CreatedModel(models.Model):
    """Abstract `Created` model."""

    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)

    class Meta:
        abstract = True


class DeletedModel(models.Model):
    """Abstract `Deleted` model."""

    deleted_at = models.DateTimeField(_("Deleted at"), null=True, blank=True, editable=False)

    objects = DeletedManager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False, force=False):
        """Delete the current instance."""
        if force:
            return super().delete(using=using, keep_parents=keep_parents)
        else:
            self.deleted_at = timezone.now()
            self.save()


class CreatedDeletedModel(CreatedModel, DeletedModel):
    """Abstract `Created, Deleted` mixin model."""

    class Meta:
        abstract = True


class UUIDCreatedDeletedModel(UUIDModel, CreatedModel, DeletedModel):
    """Abstract `Created, Deleted, UUID` mixin model."""

    class Meta:
        abstract = True


class UUIDActiveCreatedDeletedModel(ActiveUUIDModel, CreatedModel, DeletedModel):
    """Abstract `Active, Created, Deleted` mixin model."""

    objects = DeletedManager()
    active = ActiveDeleteManager()

    class Meta:
        abstract = True


class UUIDActiveCreatedModel(ActiveUUIDModel, CreatedModel):
    """Abstract `Active, Created` mixin model."""

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        abstract = True
