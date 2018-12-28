# -*- coding: utf-8 -*-
#
from django import forms

from assets.models import SystemUser
from .models import CommandExecution
from django.utils.translation import ugettext_lazy as _

from .models import Script,ScriptSchedule


class CommandExecutionForm(forms.ModelForm):
    class Meta:
        model = CommandExecution
        fields = ['run_as', 'command']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        run_as_field = self.fields.get('run_as')
        run_as_field.queryset = SystemUser.objects.all()


class ScriptForm(forms.ModelForm):
    '''
    users = forms.ModelMultipleChoiceField(
         queryset=User.objects.exclude(role=User.ROLE_APP),
         label=_("User"),
         widget=forms.SelectMultiple(
             attrs={
                 'class': 'select2',
                 'data-placeholder': _('User')
             }
         ),
         required=False,
    )
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'initial' not in kwargs:
            return
        for name, field in self.fields.items():
            if not hasattr(field, 'queryset'):
                continue
            model = field.queryset.model
            field.queryset = model.objects.all()

    class Meta:
        model = Script
        fields = ('task_name', 'users', 'user_groups', 'script_name', 'comment')
        widgets = {
            'users': forms.SelectMultiple(
                attrs={'class': 'select2', 'data-placeholder': _("User")}
            ),
            'user_groups': forms.SelectMultiple(
                attrs={'class': 'select2', 'data-placeholder': _("User group")}
            ),
        }

    def clean_user_groups(self):
        users = self.cleaned_data.get('users')
        user_groups = self.cleaned_data.get('user_groups')
        print("lclean_user_groups ", self.errors)
        if not users and not user_groups:
            raise forms.ValidationError(
                _("User or group at least one required"))
        return self.cleaned_data["user_groups"]

    '''
    def save(self, commit=True):
        print("lirengang ---------------------------------------")
        job = super().save(commit=commit)
        #job.save()

        return job
    '''
