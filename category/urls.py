from django.urls import path, re_path
from category import views


urlpatterns = [
    path('', views.index, name='index'),
    path('expenses/', views.ExpenseListView.as_view(), name='expenses'),
    re_path(r'^expense/(?P<pk>\d+)$', views.ExpenseDetailView.as_view(), name='expense-detail'),
    path('import/', views.importData, name='import-data'),
    
    path('dashboard/', views.drawDashboard, name='dashboard'),
    path('dashboard/getdataset/', views.getDataset, name='get_dataset'),
    path('dashboard/filter/', views.applyFilter, name='filter'),
    path('dashboard/filter/getdataset/', views.getDataset, name='get_dataset_from_filter'),
    path('currency/', views.currencyTrend, name='currency'),
    path('currency/getdataset', views.getCurrencyData, name='get_currency_data'),
    
    path('expense/create/', views.ExpenseCreate.as_view(), name='expense-create'),
    path('expense/<int:pk>/update/', views.ExpenseUpdate.as_view(), name='expense-update'),
    path('expense/<int:pk>/delete/', views.ExpenseDelete.as_view(), name='expense-delete'),
]

