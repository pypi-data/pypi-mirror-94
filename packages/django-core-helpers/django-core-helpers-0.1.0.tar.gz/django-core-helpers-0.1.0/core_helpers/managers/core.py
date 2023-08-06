from django.db import models
from django.utils import timezone


class DeletedQuerySet(models.query.QuerySet):
    """Custom `Deleted` QuerySet."""

    def delete(self, force: bool = False):
        """Delete the records in the current QuerySet."""
        if force:
            return super().delete()
        else:
            return self.count(), self.update(deleted_at=timezone.now())  # noqa


class DeletedManager(models.Manager):
    """Custom `Deleted` manager."""

    def get_queryset(self):
        """Return a new `DeletedQuerySet` object."""
        return DeletedQuerySet(self.model, using=self._db).filter(deleted_at__isnull=True)

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class ActiveManager(models.Manager):
    """Return records with an `is_active` flag set as `True`."""

    def get_queryset(self):
        """Return custom queryset with filter `is_active=True`."""
        return super().get_queryset().filter(is_active=True)

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class ActiveDeleteManager(models.Manager):
    """Return records with an `is_active` flag set as `True` and deleted_at is null."""

    def get_queryset(self):
        """Return custom queryset with filter `is_active=True`."""
        return super().get_queryset().filter(is_active=True).filter(deleted_at__isnull=True)

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None
