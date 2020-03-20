from django import forms
from .models import *

class ModelFormWithFileField(forms.ModelForm):
    
    class Meta:
        model = File
        fields = ('name', 'file')