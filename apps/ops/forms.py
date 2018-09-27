# ~*~ coding: utf-8 ~*~

from __future__ import absolute_import, unicode_literals
from django import forms
from django.utils.translation import ugettext_lazy as _


from .hands import User
from .models import Job,Schedule


class JobForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.exclude(role=User.ROLE_APP),
        label=_("User"),
        widget=forms.SelectMultiple(
            attrs={
                'class': 'select2',
                'data-placeholder': _('Select users')
            }
        ),
        required=False,
    )
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
        model = Job

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

        if not users and not user_groups:
            raise forms.ValidationError(
                _("User or group at least one required"))
        return self.cleaned_data["user_groups"]
