# ~*~ coding: utf-8 ~*~

from django.utils.translation import ugettext as _
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin

from ..models import Script
from common.permissions import AdminUserRequiredMixin
from django.urls import reverse_lazy
from ..forms import ScriptForm



class ScriptListView( ListView):
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


class AnsibleListView(ListView):
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

class ScriptCreateView(CreateView):
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

class ScriptUpdateView(SuccessMessageMixin, UpdateView):
    model = Script
    form_class = ScriptForm
    template_name = 'ops/script_create_update.html'
    # context_object_name = 'Script Update'
    success_url = reverse_lazy('ops:script-list')
    #success_message = update_success_msg

    def get_form(self, form_class=None):
        script_form = super().get_form(form_class=form_class)
        return script_form

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Ops'),
            'action': _('Update Script'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    # def get_context_data(self, **kwargs):
    #     check_rules = get_password_check_rules()
    #     context = {
    #         'app': _('Users'),
    #         'action': _('Update user'),
    #         'password_check_rules': check_rules,
    #     }
    #     kwargs.update(context)
    #     return super().get_context_data(**kwargs)
    #
    # def form_valid(self, form):
    #     password = form.cleaned_data.get('password')
    #     if not password:
    #         return super().form_valid(form)
    #
    #     is_ok = check_password_rules(password)
    #     if not is_ok:
    #         form.add_error(
    #             "password", _("* Your password does not meet the requirements")
    #         )
    #         return self.form_invalid(form)
    #     return super().form_valid(form)
    #
    # def get_form_kwargs(self):
    #     kwargs = super(UserUpdateView, self).get_form_kwargs()
    #     data = {'request': self.request}
    #     kwargs.update(data)
    #     return kwargs