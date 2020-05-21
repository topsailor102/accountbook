from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Sum, Count, F, Func
from django.db.models.functions import TruncMonth, TruncYear

from .models import Sector, Way, Expense, Currency
from .forms import UploadExpenseForm, ChartFilterForm
from .datatransfer import get_date_from_the_file as dt
from .currency import update_currency_through_api as uc

from datetime import date, datetime, timedelta
import json


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
    
    check_information_update()

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


def check_information_update():
    # Query DB to check if currency information has updated.
    result = Currency.objects.order_by('date').values('date').last()
    days = date.today() - result['date']

    if days.days > 0:
        # Call function if nothing has been updated for a while.
        uc(days.days-1)


class ExpenseListView(generic.ListView):
    model = Expense
    paginate_by = 21
    
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
    """Import data from the .csv file"""
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


def currencyTrend(request):
    queryset = Expense.objects.filter(dateinfo__year=datetime.now().year).filter(dateinfo__month=datetime.now().month).values('sector__name').order_by('sector').annotate(sector__cost=Round(Sum('cost')))

    return render(request, 'currency.html', {'thismonth':datetime.now().month, 'queryset':queryset})


def getCurrencyData(request):
    labels = []
    datasets = []
    item = {}
    data = []
    item['label'] = "환율!"
    item['backgroundColor'] = "rgba(78, 115, 223, 0.05)"
    item['pointHoverRadius'] = 3
    item['lineTension'] = 0.3
    item['backgroundColor'] = "rgba(78, 115, 223, 0.05)"
    item['borderColor'] = "rgba(78, 115, 223, 1)"
    item['pointRadius'] = 3
    item['pointBackgroundColor'] = "rgba(78, 115, 223, 1)"
    item['pointBorderColor'] = "rgba(78, 115, 223, 1)"
    item['pointHoverRadius'] = 3
    item['pointHoverBackgroundColor'] = "rgba(78, 115, 223, 1)"
    item['pointHoverBorderColor'] = "rgba(78, 115, 223, 1)"
    item['pointHitRadius'] = 10
    item['pointBorderWidth'] = 2
    queryset = Currency.objects.filter(date__gte=datetime.now()-timedelta(100)).values('date','cur_unit','ttb', 'tts').order_by('date')
    #print(queryset)
    for query in queryset:
        #print("{} >> {} 원/{}".format(query['date'], query['ttb'], query['cur_unit']))
        labels.append(query['date'])
        data.append(query['ttb'])
    item['data'] = data
    datasets.append(item)
    #print(labels)
    #print(datasets)
    #print(data)
    return JsonResponse(data={
        'labels': labels,
        'datasets': datasets,    
    })


def applyFilter(request):
    """Apply filter to make a chart"""
    
    if request.method == 'POST':
        form = ChartFilterForm(request.POST)
        
        if form.is_valid():
            print("============>>>>>>>>>>")
            period = form.cleaned_data['period']
            kind = form.cleaned_data['kind']
            print("period: {}, kind: {}".format(period, kind))
            
            return redirect('index')
        else:
            print("######################")
    else:
        form = ChartFilterForm()
        #print(request.GET['kind'])
        
    return render(request, 'charts.html', {'form': form })


class Round(Func):
       function = 'ROUND'


def drawDashboard(request):
    table_data = []
    queryset = Expense.objects.filter(dateinfo__year=datetime.now().year).filter(dateinfo__month=datetime.now().month).values('sector__name').order_by('sector').annotate(sector__cost=Round(Sum('cost')))
    print(queryset)
    return render(request, 'dashboard.html', {'thismonth':datetime.now().month, 'queryset':queryset})


def getDataset(request):
    labels = []
    datasets = []
    
    sector_color = { '마켓':'red', '식사':'orange', '여행':'yellow', '고정비':'green', '교육':'skyblue', '병원':'blue',
                    '쇼핑': 'purple', '은행(금전)': 'black', '주유': 'pink', '행정': 'gray' }
    sector_list = ['마켓','식사','여행','고정비','교육','병원','쇼핑','은행(금전)','주유', '행정']

    queryset_sc = Expense.objects.values('dateinfo__year','dateinfo__month', 'sector__name').order_by('dateinfo__year').annotate(sector__cost=Sum('cost'))
    """
    for query in queryset_sc:
        print("{},{} - {} : {}".format(query['dateinfo__year'], query['dateinfo__month'], query['sector__name'], query['sector__cost']))
    """
    
    queryset_cost = Expense.objects.values('dateinfo__year','dateinfo__month').order_by('dateinfo__year', 'dateinfo__month').annotate(Count('cost'))
    for query in queryset_cost:
        labels.append('{}-{}'.format(query['dateinfo__year'], query['dateinfo__month']))
        
    for sector in sector_list:
        item = {}
        item['data'] = []    
        item['label'] = sector
        item['backgroundColor'] = sector_color[sector]
        
        for query in queryset_cost:
            #print("now checking {} year {} month with sector name {}".format(query['dateinfo__year'],query['dateinfo__month'], sector))
            if not any(sc['dateinfo__year'] == query['dateinfo__year'] and sc['dateinfo__month'] == query['dateinfo__month'] and sc['sector__name'] == sector for sc in queryset_sc):
                item['data'].append(0)
            else:
                [item['data'].append(round(float(sc['sector__cost']),2)) for sc in queryset_sc if sc['dateinfo__year'] == query['dateinfo__year'] and sc['dateinfo__month'] == query['dateinfo__month'] and sc['sector__name'] == sector]
            
        datasets.append(item)

    return JsonResponse(data={
        'labels': labels,
        'datasets': datasets,    
    })

