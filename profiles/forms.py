from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from django.forms import TextInput, EmailInput, PasswordInput

from profiles.models import Profile

User = get_user_model()


class UserAdminCreationForm(forms.ModelForm):
    '''A form for creating new users. Includes all required fields plus
    repeated password'''
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self): # checking that the two passwords match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match')
        return password2

    def save(self, commit=True): # save he proovided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    ''' A form for updating users, includes all the fields on the user, but
    replaces the password fields with admin's password hash display field. '''

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        ''' Regardless of what the user provides retrun the initial value.
        This is done here rather than on the field, because the field does
        not have access to the initial value. '''
        return self.initial['password']


class SignupForm(forms.Form):
    first_name = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}))
    last_name = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}))
    email = forms.EmailField(widget=EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}))
    password2 = forms.CharField(
        widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        password2 = cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('Passwords did not match', code='invalid password')

    def save(self, commit=True):
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        user = User(email=email)
        user.set_password(password)
        if commit:
            user.save()
            Profile.objects.create(user=user, first_name=first_name, last_name=last_name)
        return user
