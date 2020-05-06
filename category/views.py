from django.shortcuts import render
from .models import Sector, Way, Expense
from django.views import generic
from datetime import datetime, timedelta

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .forms import UploadExpenseForm
from .datatransfer import get_date_from_the_file as dt
from django.shortcuts import redirect


def index(request):
    """View function for home page of site"""
    
    # counts of expenses
    num_of_expenses = Expense.objects.all().count()
    
    # number of kinds of payments method
    num_of_ways = Way.objects.all().count()
    
    # classified sectors for the statics
    num_of_sectors = Sector.objects.count()
    
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    
    context = {
        'num_expense': num_of_expenses,
        'num_ways': num_of_ways,
        'num_sectors': num_of_sectors,
        'num_visits': num_visits,
        }
    
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class ExpenseListView(generic.ListView):
    model = Expense
    paginate_by = 30
    
    def get_queryset(self):
        return Expense.objects.filter(dateinfo__gte=datetime.now()-timedelta(1000))


class ExpenseDetailView(generic.DetailView):
    model = Expense
    
    def expense_detail_view(request, id):
        try:
            thing = Expense.objects.get(id)
        except Expense.DoesNotExist:
            raise Http404('Expense does not exist')
        
        return render(request, 'category/expense_detail.html', context={'expense': thing})
def importData(request):
    """Import data from the .csv file"""
    
    
    return render(request, 'import_data.html')

class ExpenseCreate(CreateView):
    model = Expense
    fields = '__all__'
    initial = {'summary':'안 쓰면 안 쓰는데로 이해하는 거 알쥬?'}


class ExpenseUpdate(UpdateView):
    model = Expense
    fields = ['place', 'cost', 'way', 'sector']
    
class ExpenseDelete(DeleteView):
    model = Expense
    success_url = reverse_lazy('expenses')


def importData(request):
    if request.method == 'POST':
        form = UploadExpenseForm(request.POST)
        
        if form.is_valid():
            print("============>>>>>>>>>>")
            filepath = form.cleaned_data['csvfile']
            text = form.cleaned_data['text']
            dt(filepath)
            
            return redirect('index')
            
            #text = form.clean_data['text']
        else:
            print("######################")
        
        #form = UploadExpenseForm(request.POST, request.FILES)
    else:
        form = UploadExpenseForm()
        
    return render(request, 'import_data.html', {'form': form })
