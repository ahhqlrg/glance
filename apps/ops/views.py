# ~*~ coding: utf-8 ~*~

from django.utils.translation import ugettext as _
from django.conf import settings
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from django.contrib.messages.views import SuccessMessageMixin

from common.mixins import DatetimeSearchMixin
from .models import Task, AdHoc, AdHocRunHistory, CeleryTask, Script, ScriptSchedule
from common.permissions import AdminUserRequiredMixin
from django.urls import reverse_lazy

from orgs.utils import current_org
from .hands import Node, Asset, SystemUser, User, UserGroup
from .forms import ScriptForm

class ScriptListView(AdminUserRequiredMixin, ListView):
    template_name = 'ops/script_list.html'
    model = Script

    context_object_name = "script_list"

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Ops'),
            'action': _('Script Schedule'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class AnsibleListView(AdminUserRequiredMixin, ListView):
    template_name = 'ops/ansible_list.html'
    model = Script

    context_object_name = "ansible_list"

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Ops'),
            'action': _('Ansible Manager'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class ScriptCreateView(AdminUserRequiredMixin, CreateView):
    model = Script
    form_class = ScriptForm
    template_name = 'ops/script_create_update.html'
    success_url = reverse_lazy('ops:script-list')

    def get_form(self, form_class=None):
        script_form = super().get_form(form_class=form_class)
        return script_form

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Ops'),
            'action': _('Create Script'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)
    '''
    def form_valid(self, form):
        print("================================================================")
        #user = form.save(commit=True)
        #user.created_by = self.request.user.username or 'System'
        #user.save()
        #post_user_create.send(self.__class__, user=user)
        return super().form_valid(form)
    '''



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
