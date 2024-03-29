from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import Http404
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.core.paginator import Paginator

from .forms import AccountForm, InstitutionForm
from .models import Account, Institution, AccountValue

class AccountDeleteView(DeleteView):
    model = Account
    success_url = '/accounts/accounts'
    template_name = 'accounts/account_delete.html'
    title = 'Delete Account'
    hierarchy = [
        {'name': 'Accounts', 'urlname': 'accounts.list'},
    ]

class AccountUpdateView(UpdateView):
    model = Account
    form_class = AccountForm
    success_url = '/accounts/accounts'  
    title = 'Edit Account'
    hierarchy = [
        {'name': 'Accounts', 'urlname': 'accounts.list'},
    ]

class AccountsListView(LoginRequiredMixin, ListView):
    model = Account
    context_object_name = "accounts"
    template_name = 'accounts/account_list.html'
    login_url = "/login" 
    title = "Accounts"
    hierarchy = [
        {'name': 'Accounts', 'urlname': 'accounts.list'},
    ]

    def get_queryset(self):
        if 'parent_id' in self.kwargs:
            return self.request.user.accounts.filter(parent_institution=self.kwargs['parent_id'])
        else:
            return self.request.user.accounts.all()
        
    def parent_name(self):
        parent_institution=Institution.objects.get(pk=self.kwargs['parent_id'])
        return parent_institution

class AccountCreateView(CreateView):
    model = Account
    form_class = AccountForm
    success_url = '/accounts/accounts'
    title = 'New Account'
    hierarchy = [
        {'name': 'Accounts', 'urlname': 'accounts.list'},
        {'name': 'New', 'urlname': 'account.new'},
    ]

    def form_valid(self, form):
        self.object = form.save(commit = False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class AccountDetailsView(DetailView):
    model = Account
    context_object_name = "account"
    title = 'Account Details'
    template_name = 'accounts/account_detail.html'
    hierarchy = [
        {'name': 'Accounts', 'urlname': 'accounts.list'},
    ]

    page_number = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account_values_pagin = Paginator(self.object.values.order_by('-value_date'),10)
        page_number = self.request.GET.get("page")
        context['account_report'], context['account_report_labels'] = self.object.account_over_time_report()
        if page_number is not None:
            self.page_number = page_number

        context['account_values'] = account_values_pagin.page(self.page_number)

        return context

    

class InstitutionListView(LoginRequiredMixin, ListView):
    model = Institution
    context_object_name = "institutions"
    template_name = 'accounts/institution_list.html'
    login_url = "/login"
    title = "Institutions Profiles"
    hierarchy = [
        {'name': 'Institution Profiles', 'urlname': 'institutions.list'},
    ]

    def get_queryset(self):
        return self.request.user.institutions.all()

class InstitutionCreateView(CreateView):
    model = Institution
    form_class = InstitutionForm
    success_url = '/accounts/institutions'
    title = "New Institution Profiles"
    hierarchy = [
        {'name': 'Institution Profiles', 'urlname': 'institutions.list'},
        {'name': 'New', 'urlname': 'institution.new'},
    ]
    
    def form_valid(self, form):
        self.object = form.save(commit = False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class InstitutionDetailsView(LoginRequiredMixin, DetailView):
    model = Institution
    context_object_name = "institution"
    title = "Institution Profile Details"
    login_url = "/login"
    hierarchy = [
        {'name': 'Institution Profiles', 'urlname': 'institutions.list'},
    ]

class InstitutionDeleteView(DeleteView):
    model = Institution
    success_url = '/accounts/institutions'
    template_name = 'accounts/institution_delete.html'

    title = "Delete Institution Profile"
    hierarchy = [
        {'name': 'Institution Profiles', 'urlname': 'institutions.list'},
    ]

class InstitutionUpdateView(LoginRequiredMixin, UpdateView):
    model = Institution
    form_class = InstitutionForm
    success_url = '/accounts/institutions'
    title = "Edit Institution Profile"
    login_url = "/login"
    hierarchy = [
        {'name': 'Institution Profiles', 'urlname': 'institutions.list'},
    ]
    