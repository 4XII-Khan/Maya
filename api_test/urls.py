from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'add_book$', add_book, ),
    url(r'select_personal_bills$', select_personal_bills, ),
    url(r'get_all_users$', get_all_users, ),
    url(r'get_financial_accounts$', get_financial_accounts, ),
    url(r'get_continuously_not_pick$', get_continuously_not_pick, ),
    url(r'get_continuously_not_join$', get_continuously_not_join, ),
]
