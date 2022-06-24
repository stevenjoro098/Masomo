from django import forms
from courses.models import Unit
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class UnitEnrollForm(forms.Form):
    unit = forms.ModelChoiceField(queryset=Unit.objects.all(),
                                  widget=forms.HiddenInput)


class RegistrationForm(UserCreationForm):  # inherits properties from auth.forms: UserCreationForm
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class ProfileUpdate(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = Profile
        fields = ['image', 'telephone', 'birth_date', 'bio']
