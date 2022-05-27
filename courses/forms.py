from django import forms
from django.forms.models import inlineformset_factory
from .models import Unit, Topics

'''A formset is a layer of abstraction to work with multiple forms on the same page.'''
'''TopicsFormset: Used when instructor wants to create multiple Topics at once.'''
TopicsFormSet = inlineformset_factory(Unit, Topics,  # simplify the case of working with related objects via a foreign
                                                     # key.
                                      fields=['title', 'description'],  # fields needed to render
                                      extra=2,  # render two fields set; extra defines the no. of extra iteration the
                                                # formset will render.
                                      can_delete=True)  # boolean to delete extra fields when necessary


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)  # override the widgets to accept passwordinput.
