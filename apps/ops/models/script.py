# -*- coding: utf-8 -*-
#

import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from common.utils import date_expired_default, set_or_append_attr_bulk
from orgs.mixins import OrgModelMixin, OrgManager

__all__ = ["Script"]




class Script(OrgModelMixin):

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    task_name = models.CharField(max_length=512, verbose_name=_("Task name"))

    users = models.ManyToManyField('users.User', related_name='script_permissions', blank=True, verbose_name=_("User"))
    user_groups = models.ManyToManyField('users.UserGroup', related_name='script_permissions', blank=True,
                                         verbose_name=_("User group"))
    script_name = models.CharField(max_length=128, verbose_name=_("Script name"))
    comment = models.TextField(blank=True, null=True, verbose_name=_("Comment"))
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, verbose_name=_('Date created')
    )


    @classmethod
    def get_queryset_group_by_task_name(cls):
        names = cls.objects.values_list('task_name', flat=True)
        for name in names:
            yield name, cls.objects.filter(name=name)
            cls.objects.filter()

    def __str__(self):
        return self.task_name

    class Meta:
        db_table = "ops_script"
        ordering = ['task_name']

    @property
    def id_str(self):
        return str(self.id)

    def get_all_users(self):
        users = set(self.users.all())
        for group in self.user_groups.all():
            _users = group.users.all()
            set_or_append_attr_bulk(_users, 'inherit', group.name)
            users.update(set(_users))
        return users