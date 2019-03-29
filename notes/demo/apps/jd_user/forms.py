#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2019/2/2


from django.contrib.auth.forms import AuthenticationForm
from django import forms


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='手机号', max_length=100)
    password = forms.CharField(
        label='密码', widget=forms.PasswordInput,
        max_length=128, strip=False
    )
