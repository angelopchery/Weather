from django import forms
from .models import History

class weatherForm(forms.ModelForm): #Forms to take data input from users
    class Meta:
        model = History
        fields = ['city']