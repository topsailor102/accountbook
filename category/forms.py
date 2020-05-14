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

my_choices1 =( 
    ("WY", "Wonyoung"), 
    ("YO", "Yunok"), 
    ("SH", "Seunghu"), 
    ("SY", "Seungyeon"), 
)
my_choices2 = (
    ("All", "All"),
    ("L3", "Last 3 months"),
    ("L6", "Last 6 months"),
    ("T", "This month"),
)

my_choices3 = (('2019-9', '2019-9'), ('2019-10', '2019-10'), ('2019-11', '2019-11'), ('2019-12', '2019-12'), ('2020-1', '2020-1'), ('2020-2', '2020-2'), ('2020-3', '2020-3'), ('2020-4', '2020-4'), ('2020-5', '2020-5'))
from .models import Sector, Way, Expense
from django.db.models import Sum, Count

def get_choice1():
    choices = [('999', '모두'),]
    queryset_cost = Sector.objects.all()
    

    for query in queryset_cost:
        choices.append(("{}".format(query.id), "{}".format(query)))
    
    print(tuple(choices)) 
    return tuple(choices)


def get_choice2():
    choices = []
    queryset_cost = Expense.objects.values('dateinfo__year','dateinfo__month').order_by('dateinfo__year').annotate(Count('cost'))
    for query in queryset_cost:
        choices.append(("{}-{}".format(query['dateinfo__year'], query['dateinfo__month']), "{}-{}".format(query['dateinfo__year'], query['dateinfo__month'])))
    
    print(tuple(choices)) 
    return tuple(choices)
    
        
class ChartFilterForm(forms.Form):
    kind = forms.MultipleChoiceField()
    period = forms.ChoiceField()


            
    def __init__(self, *arg, **kwargs):
        super(ChartFilterForm, self).__init__(*arg, **kwargs)
        self.fields['kind'].choices = get_choice1()
        self.fields['kind'].widget.attrs['size']='11'
        self.fields['kind'].initial = ['999',]
        self.fields['period'].choices = my_choices2
