from django.urls import path, re_path
from category import views


urlpatterns = [
    path('', views.index, name='index'),
    path('expenses/', views.ExpenseListView.as_view(), name='expenses'),
    re_path(r'^expense/(?P<pk>\d+)$', views.ExpenseDetailView.as_view(), name='expense-detail'),
    path('import/', views.importData, name='import-data'),
    
    path('expense/create/', views.ExpenseCreate.as_view(), name='expense-create'),
    path('expense/<int:pk>/update/', views.ExpenseUpdate.as_view(), name='expense-update'),
    path('expense/<int:pk>/delete/', views.ExpenseDelete.as_view(), name='expense-delete'),
]

