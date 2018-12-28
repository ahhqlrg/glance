# ~*~ coding: utf-8 ~*~

from django.utils.translation import ugettext as _
from django.views.generic import ListView, CreateView

from ..models import Script
from common.permissions import AdminUserRequiredMixin
from django.urls import reverse_lazy
from ..forms import ScriptForm



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
