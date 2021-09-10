from django import forms
from problembank.widget import MoratabEditor

class QuestionForm(forms.ModelForm):
    text_tmp1 = forms.CharField(widget=MoratabEditor, required=False)
    text_tmp2 = forms.CharField(widget=MoratabEditor, required=False)
    
