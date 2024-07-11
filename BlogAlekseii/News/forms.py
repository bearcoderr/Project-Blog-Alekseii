from django import forms
from .models import FormsNews

class FeedbackCreateForm(forms.ModelForm):
    """
    Форма отправки обратной связи
    """

    class Meta:
        model = FormsNews
        fields = ('nameComm', 'emailComm', 'textComm')
