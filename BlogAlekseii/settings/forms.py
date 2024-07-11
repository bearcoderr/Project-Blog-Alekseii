from django import forms
from .models import FormsHome

class formsHome(forms.ModelForm):
    class Meta:
        model = FormsHome
        fields = ['nameFormsHome', 'emailFormsHome', 'callFormsHome', 'massageFormsHome']