from django.urls import path
from .views import LoanListView, LoanCreateView, return_book, my_loans, loan_stats

urlpatterns = [
    path('', LoanListView.as_view(), name='loan-list'),
    path('create/', LoanCreateView.as_view(), name='loan-create'),
    path('<int:loan_id>/return/', return_book, name='return-book'),
    path('my-loans/', my_loans, name='my-loans'),
    path('stats/', loan_stats, name='loan-stats'),
]
