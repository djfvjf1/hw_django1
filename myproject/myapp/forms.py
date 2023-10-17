from django import forms
from django.contrib.auth.models import User  # Импортируйте модель User

from .models import Problem


class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['name', 'phone', 'email', 'description', 'priority', 'resolved', 'assigned_user']

    def __init__(self, *args, **kwargs):
        super(ProblemForm, self).__init__(*args, **kwargs)
        self.fields['assigned_user'].queryset = User.objects.filter(groups__name='Reception')