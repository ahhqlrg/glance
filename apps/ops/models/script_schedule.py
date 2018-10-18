# -*- coding: utf-8 -*-
#

import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from common.utils import date_expired_default, set_or_append_attr_bulk
from orgs.mixins import OrgModelMixin, OrgManager

__all__ = ["ScriptSchedule"]



class ScriptSchedule(OrgModelMixin):

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    task_name = models.ForeignKey("ops.Script",on_delete=models.CASCADE,related_name='task_name_by_schedule',verbose_name=_("Task name"))
    users = models.ForeignKey("ops.Script",on_delete=models.CASCADE,verbose_name=_("User"))
    assets = models.ManyToManyField('assets.Asset', related_name='schedule_by_permissions', blank=True,verbose_name=_("Asset"))
    nodes = models.ManyToManyField('assets.Node', related_name='schedule_by_permissions', blank=True,verbose_name=_("Nodes"))

    result = models.BooleanField(default=False, verbose_name=_('Result'))
    log = models.TextField(blank=True, null=True, verbose_name=_("Schedule log"))
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, verbose_name=_('Date created')
    )

    @classmethod
    def get_queryset_group_by_task_name(cls):
        names = cls.objects.values_list('task_name', flat=True)
        for name in names:
            yield name, cls.objects.filter(name=name)

    def __str__(self):
        return self.task_name

    class Meta:
        db_table = "ops_script_schedule"
        ordering = ['task_name']

    @property
    def id_str(self):
        return str(self.id)

    def get_all_assets(self):
        assets = set(self.assets.all())
        for node in self.nodes.all():
            _assets = node.get_all_assets()
            set_or_append_attr_bulk(_assets, 'inherit', node.value)
            assets.update(set(_assets))
        return assets