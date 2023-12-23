from dataclasses import fields
import imp
from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django.forms.widgets import PasswordInput
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm, PasswordChangeForm
from .models import *
from django.core.mail import send_mail

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'autofocus':False})
    """
    A Custom form for creating new users.
    """
    USER_TYPE = [('P/G', 'Parent/Guardian'),
                ('BHW', 'Barangay Health Worker')]
                 
    BARANGAYS = [('Select Barangay', 'Select Barangay'),
                 ('Burol', 'Burol'),
                 ('Burol I', 'Burol I'),
                 ('Burol II', 'Burol II'),
                 ('Burol III', 'Burol III'),
                 ('Datu Esmael', 'Datu Esmael'),
                 ('Emmanuel Begado I', 'Emmanuel Begado I'),
                 ('Emmanuel Begado II', 'Emmanuel Begado II'),]
    
    user_type = forms.CharField(required=True, label="User Type:", widget=forms.Select(choices=USER_TYPE, attrs={'class' : 'custom-select', 'id' : 'userTypeSelect'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'type': 'text', 'placeholder': 'First Name', 'id' : 'firstname'}))
    middle_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'type': 'text', 'placeholder': 'Middle Name', 'id' : 'middlename'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'type': 'text', 'placeholder': 'Last Name', 'id' : 'lastname'}))
    suffix_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'type': 'text', 'placeholder': 'Suffix', 'id' : 'suffixname'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'name' : 'email', 'type' : 'email', 'id' : 'email', 'placeholder': 'Enter your email address'}))
    password1 = forms.CharField(required=True,widget=PasswordInput(attrs={'type' : 'password', 'id' : 'password', 'aria-describeby' : 'passwordHelpBlock', 'placeholder':'Enter your Password', 'data-toggle': 'password'}))
    password2 = forms.CharField(required=True,widget=PasswordInput(attrs={'type' : 'password', 'id' : 'cpassword', 'placeholder':'Confirm Your Password','data-toggle': 'password'}))
    barangay = forms.ModelChoiceField(required=True, queryset=Barangay.objects.all(), widget=forms.Select(attrs={'class' : 'fstdropdown-select', 'id' : 'brgy'}))
    phone_num = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'type': 'number', 'placeholder': 'Phone Number', 'id' : 'phonenum'}))
    class Meta:
        model = get_user_model()
        fields = ['user_type', 'first_name', 'last_name', 'email', 'phone_num', 'password1', 'password2']
    
    def save(self):
        user = super().save(commit=False)
        user.user_type = self.cleaned_data.get('user_type')
        user.first_name = self.cleaned_data.get('first_name')
        user.middle_name = self.cleaned_data.get('middle_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.suffix_name = self.cleaned_data.get('suffix_name')
        user.email = self.cleaned_data.get('email')
        user.phone_num = self.cleaned_data.get('phone_num')
        user.save()

        if self.cleaned_data.get('user_type') == 'BHW':
            selected_brgy = Barangay.objects.get(brgy_name=self.cleaned_data.get('barangay'))
            bhw = BarangayHealthWorker.objects.create(user=user, bhw_barangay=selected_brgy)
            bhw.save()
        
        if self.cleaned_data.get('user_type') == 'P/G':
            selected_brgy = Barangay.objects.get(brgy_name=self.cleaned_data.get('barangay'))
            png = Parent.objects.create(user=user, barangay=selected_brgy)
            png.save()
        return user

class Validate_BHW(ModelForm):
    class Meta:
        model = BarangayHealthWorker
        fields = ['is_validated']
        widgets = {'is_validated' : forms.CheckboxInput(attrs={'class' : 'form-check-input', 'type' : 'checkbox'})}
    
    def save(self):
        user = super().save(commit=False)
        user.is_validated = True
        user.save()
        
        return user

class UpdatePreschooler(ModelForm):
    height = forms.FloatField(required=True, min_value=1, widget=forms.NumberInput(attrs={'class' : 'form-control', 'step': '0.01','placeholder': '45cm - 120cm'}))
    weight = forms.FloatField(required=True, min_value=0.1, widget=forms.NumberInput(attrs={'class' : 'form-control', 'step': '0.01', 'placeholder': '1kg - 28kg'}))
    date_measured = forms.DateField(required=True,widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id' : "data_count"}))
    health_problem = forms.CharField(required=False, widget=forms.Textarea(attrs={'class' : 'form-control', 'type': 'text', 'id' : 'health_problem', 'placeholder': 'N/A'}))

    class Meta:
        model = Preschooler
        fields = ['height', 'weight', 'date_measured', 'health_problem']

class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']

class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['old_password', 'new_password1', 'new_password2']

class AddBarangay(ModelForm):
    brgy_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class' : "form-control", 'type': 'text', 'id' : 'brgy_name'}))
    brgy_phone = forms.CharField(required=True, widget=forms.TextInput(attrs={'class' : "form-control", 'type': 'text', 'id' : 'brgy_phone'}))
    brgy_address = forms.CharField(required=True, widget=forms.TextInput(attrs={'class' : "form-control", 'type': 'text', 'id' : 'brgy_address'}))
    
    class Meta:
        model = Barangay
        fields = ['brgy_name', 'brgy_phone', 'brgy_address']

class ChangePicture(ModelForm):
    class Meta:
        model = Preschooler
        fields = ['ps_image']