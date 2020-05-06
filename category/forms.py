from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

def check_csvfile(file):    
    if file.split('.')[-1] != "csv":
        raise forms.ValidationError(_('file format is not expected!'))
    
class UploadExpenseForm(forms.Form):
    csvfile = forms.FilePathField(path='/Users/wonyoungchi/django/accountbook/', validators = [check_csvfile])
    text = forms.CharField(widget=forms.Textarea)
    """
    def clean_csvfile(self):
        file  = self.cleaned_data['csvfile']
        
        if file.split('.')[-1] != "csv":
            raise ValidationError(_('file format is not expected!'))
        
        return file
    """