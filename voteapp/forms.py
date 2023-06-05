from django.forms import ModelForm
from django import forms
from .models import User, UserProfile

class ProfileForm(ModelForm):
    name = forms.CharField(
        label='',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'name',
            'placeholder':'new name'
        })
    )

    description = forms.Textarea(
        attrs={
        'class':'description',
        'placeholder':'description'
    }
    )

    class Meta:
        model = UserProfile
        fields = ['name', 'description', 'picture']