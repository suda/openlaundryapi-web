# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    debug = forms.BooleanField(label="Debug mode", required=False)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'debug']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    def save(self, *args, **kwargs):
        kwargs['commit'] = False
        user = super(UserForm, self).save(*args, **kwargs)
        profile = user.get_profile()
        profile.debug = self.cleaned_data['debug']
        profile.save()
        user.save()
        return user


