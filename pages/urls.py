from django.urls import path
from .views import HomePageView, CatalogPageView, ContactsPageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('contacts/', ContactsPageView.as_view(), name='contacts'),
]