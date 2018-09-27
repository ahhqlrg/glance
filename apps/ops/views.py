# ~*~ coding: utf-8 ~*~

from django.utils.translation import ugettext as _
from django.conf import settings
from django.views.generic import ListView, DetailView, TemplateView, CreateView

from common.mixins import DatetimeSearchMixin
from .models import Task, AdHoc, AdHocRunHistory, CeleryTask, Job, Schedule
from common.permissions import AdminUserRequiredMixin
from django.urls import reverse_lazy

from orgs.utils import current_org
from .hands import Node, Asset, SystemUser, User, UserGroup
#from .forms import AssetPermissionForm

class JobListView(AdminUserRequiredMixin, ListView):
    template_name = 'ops/job_list.html'
    model = Job
    context_object_name = "job_list"

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Ops'),
            'action': _('Job List'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class JobCreateView(AdminUserRequiredMixin, CreateView):
    model = Job
    template_name = 'ops/job_create_update.html'
    success_url = reverse_lazy('ops:job-list')
    fields = ["users","user_groups","name","script","comment"]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Ops'),
            'action': _('Create Job'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class TaskListView(AdminUserRequiredMixin, DatetimeSearchMixin, ListView):
    paginate_by = settings.DISPLAY_PER_PAGE
    model = Task
    ordering = ('-date_created',)
    context_object_name = 'task_list'
    template_name = 'ops/task_list.html'
    keyword = ''

    def get_queryset(self):
        self.queryset = super().get_queryset()
        self.keyword = self.request.GET.get('keyword', '')
        self.queryset = self.queryset.filter(
            date_created__gt=self.date_from,
            date_created__lt=self.date_to
        )

        if self.keyword:
            self.queryset = self.queryset.filter(
                name__icontains=self.keyword,
            )
        return self.queryset

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Ops'),
            'action': _('Task list'),
            'date_from': self.date_from,
            'date_to': self.date_to,
            'keyword': self.keyword,
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class TaskDetailView(AdminUserRequiredMixin, DetailView):
    model = Task
    template_name = 'ops/task_detail.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Ops'),
            'action': _('Task detail'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class TaskAdhocView(AdminUserRequiredMixin, DetailView):
    model = Task
    template_name = 'ops/task_adhoc.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Ops'),
            'action': _('Task versions'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class TaskHistoryView(AdminUserRequiredMixin, DetailView):
    model = Task
    template_name = 'ops/task_history.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Ops'),
            'action': _('Task run history'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class AdHocDetailView(AdminUserRequiredMixin, DetailView):
    model = AdHoc
    template_name = 'ops/adhoc_detail.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Ops'),
            'action': 'Task version detail',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class AdHocHistoryView(AdminUserRequiredMixin, DetailView):
    model = AdHoc
    template_name = 'ops/adhoc_history.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Ops'),
            'action': _('Version run history'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class AdHocHistoryDetailView(AdminUserRequiredMixin, DetailView):
    model = AdHocRunHistory
    template_name = 'ops/adhoc_history_detail.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Ops'),
            'action': _('Run history detail'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class CeleryTaskLogView(AdminUserRequiredMixin, DetailView):
    template_name = 'ops/celery_task_log.html'
    model = CeleryTask
