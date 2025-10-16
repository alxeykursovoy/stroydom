from django.shortcuts import render
from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class CatalogPageView(TemplateView):
    template_name = 'pages/catalog.html'

class ContactsPageView(TemplateView):
    template_name = 'pages/contacts.html'