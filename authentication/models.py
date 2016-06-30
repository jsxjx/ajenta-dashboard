from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class DashboardUser(models.Model):
    user = models.OneToOneField(User)

    class Meta:
        permissions = (
            ("can_view_stats", "Can see all stats"),
        )

    def __unicode__(self):
        return unicode(self.user)
