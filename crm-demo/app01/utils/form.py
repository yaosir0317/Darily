from django import forms
from django.db import models
from app01.models import UserInfo, Customer, ConsultRecord, Student, ClassStudyRecord, StudentStudyRecord
from django.forms import widgets as wid
from django.core.exceptions import ValidationError


class UserInfoModelForm(forms.ModelForm):
    r_pwd = forms.CharField(
        max_length=32,
        label='请再次输入密码',
        error_messages={
            'required': '密码不能为空'},
        widget=wid.PasswordInput(
            attrs={
                "class": "form-control"}),
    )

    class Meta:
        model = UserInfo
        fields = ['username', 'email', 'password', 'r_pwd']
        labels = {
            'username': '用户名',
            'email': '邮箱',
            'password': '密码',
        }
        error_messages = {
            'username': {'required': '用户名不能为空'},
            'email': {'required': '邮箱不能为空'},
            'password': {'required': '密码不能为空'},
        }
        widgets = {
            'password': wid.TextInput(attrs={'type': 'password'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_username(self):
        val = self.cleaned_data.get('username')
        ret = UserInfo.objects.filter(username=val).first()
        if not ret:
            return val
        else:
            raise ValidationError('该用户名已存在!')

    def clean_password(self):
        val = self.cleaned_data.get('password')
        if val.isdigit():
            raise ValidationError('密码不能是纯数字!')
        else:
            return val

    def clean(self):
        password = self.cleaned_data.get('password')
        r_pwd = self.cleaned_data.get('r_pwd')
        if password and r_pwd:
            print(password, r_pwd)
            if password == r_pwd:
                print(self.cleaned_data)
                return self.cleaned_data
            else:
                print(111)
                raise ValidationError('两次密码不一致')
        else:
            return self.cleaned_data


class CustomerModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            from multiselectfield.forms.fields import MultiSelectFormField
            if not isinstance(field, MultiSelectFormField):
                field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Customer
        fields = '__all__'


class ConsultRecordModelForm(forms.ModelForm):

    def __init__(self, request, edit_record, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 根据所实例的编辑记录所属客户id进行过滤
        if edit_record:
            self.fields['customer'].queryset = Customer.objects.filter(pk=edit_record)
            self.fields['consultant'].queryset = UserInfo.objects.filter(pk=request.user.id)
        else:
            self.fields['customer'].queryset = Customer.objects.filter(consultant=request.user.id)
            self.fields['consultant'].queryset = UserInfo.objects.filter(pk=request.user.id)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = ConsultRecord
        exclude = ["delete_status"]
        error_messages = {
            'customer': {'required': '客户名不能为空'},
            'note': {'required': '内容不能为空'},
            'status': {'required': '内容不能为空'},
            'consultant': {'required': '内容不能为空'},
        }


class ClassStudyRecordModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            from multiselectfield.forms.fields import MultiSelectFormField
            if not isinstance(field, MultiSelectFormField):
                field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = ClassStudyRecord
        fields = '__all__'


class StudentStudyRecordModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            from multiselectfield.forms.fields import MultiSelectFormField
            if not isinstance(field, MultiSelectFormField):
                field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = StudentStudyRecord
        fields = ["score", "homework_note"]
