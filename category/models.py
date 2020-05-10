from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
from tkinter import Place
from django.contrib.admin.utils import help_text_for_field


class Sector(models.Model):
    """Model representing a sector for purchase."""
    name = models.CharField(max_length=200, help_text="구매가 이뤄진 항목은 어떤 분류 체계에 들어있는 지 정의합니다.")
    
    def __str__(self):
        """String for representing the Model object"""
        return self.name

class Way(models.Model):
    """Model representing a way for purchase."""
    WAY_KIND = (
        ('CASH', 'Cash'),
        ('CITI', 'CreditCard(Citi)'),
        ('N26', 'N26'),
        )
    
    name = models.CharField(
        max_length=20,
        choices=WAY_KIND,
        blank=False,
        default='CASH',
        help_text="결제를 어떻게 했는 지 정의합니다.",
        )
    
    def __str__(self):
        """String for representing the Model object"""
        return self.name

class Expense(models.Model):
    """Model representing an expense."""
    dateinfo = models.DateField(auto_now=False, null=True, blank=True)
    place = models.CharField(max_length=200)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    way = models.ForeignKey('Way', on_delete=models.SET_NULL, null=True, help_text="결재 수단을 선택하세요.")
    summary = models.TextField(max_length=1000, default="안 쓰면 안 쓰는데로 이해하는 거 알쥬?", help_text="지출한 내역을 상세히 설명해 주세요.")
    isfixed = models.BooleanField()
    sector = models.ForeignKey('Sector', on_delete=models.SET_NULL, null=True, help_text="지출항목을 어디로 분류할 지 선택해 주세요.")
    creationinfo = models.DateField(auto_now=True)
    
    def __str__(self):
        """String for representing the Model object."""
        return self.place
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this expense."""
        return reverse('expense-detail', args=[str(self.id)])

    class Meta:
        ordering = [ '-dateinfo', 'creationinfo', 'sector']
        
    def update_details(self):
        """Returns the url to access a detail record for this expense."""
        return reverse('expense-update', args=[str(self.id)])

