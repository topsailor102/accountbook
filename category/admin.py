from django.contrib import admin
from category.models import Way, Sector, Expense

admin.site.register(Way)
admin.site.register(Sector)

#admin.site.register(Expense)
@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('dateinfo', 'sector', 'place', 'cost', 'way', 'summary')
    list_filter = ('sector', 'way')