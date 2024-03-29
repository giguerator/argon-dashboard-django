from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import Http404
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect

from .models import ManualAsset
from .forms import ManualAssetForm
from apps.accounts.models import Account, Institution, get_total_account_value

def get_total_asset_value(assets):
        total = 0
        for asset in assets:
            total = total + asset.current_value
        return total 


class ManualAssetListView(LoginRequiredMixin, ListView):
    model = ManualAsset
    context_object_name = "manual_assets"
    template_name = 'networth/manual_asset_list.html'
    login_url = "/login" 
    title = 'Manual Assets'
    hierarchy = [
        {'name': 'Manual Assets', 'urlname': 'manual_assets.list'},
    ]

    def get_queryset(self):
        return self.request.user.manual_assets.all()

class ManualAssetDeleteView(DeleteView):
    model = ManualAsset
    context_object_name = "manual_asset"
    success_url = '/networth/manual_assets'
    template_name = 'networth/manual_asset_delete.html'
    title = 'Delete Manual Asset'
    hierarchy = [
        {'name': 'Manual Assets', 'urlname': 'manual_assets.list'},
    ]

class ManualAssetUpdateView(UpdateView):
    model = ManualAsset
    form_class = ManualAssetForm
    success_url = '/networth/manual_assets'
    template_name = 'networth/manual_asset_form.html'
    title = 'Edit Manual Asset'
    hierarchy = [
        {'name': 'Manual Assets', 'urlname': 'manual_assets.list'},
    ]

class ManualAssetCreateView(CreateView):
    model = ManualAsset
    form_class = ManualAssetForm
    success_url = '/networth/manual_assets'
    template_name = 'networth/manual_asset_form.html'
    title = 'New Manual Asset'
    hierarchy = [
        {'name': 'Manual Assets', 'urlname': 'manual_assets.list'},
        {'name': 'New', 'urlname': 'manual_asset.new'},
    ]

    def form_valid(self, form):
        self.object = form.save(commit = False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class ManualAssetDetailsView(DetailView):
    model = ManualAsset
    context_object_name = "manual_asset"
    template_name = 'networth/manual_asset_detail.html'
    title = 'Manual Asset Details'
    hierarchy = [
        {'name': 'Manual Assets', 'urlname': 'manual_assets.list'},
    ]
    
class NetworthSummaryView(LoginRequiredMixin, ListView):
    template_name = 'networth/networth_summary.html'
    login_url = "/login" 
    title = 'Net Worth Summary'
    hierarchy = [
        {'name': 'Net Worth Summary', 'urlname': 'networth.summary'},
    ]

    def get_queryset(self):
        return self.request.user.manual_assets.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        accounts = self.request.user.accounts.all()
        context['accounts'] = accounts

        context['institutions'] = self.request.user.institutions.all()

        assets = self.request.user.manual_assets.all()
        context['manual_assets'] = assets

        account_total = get_total_account_value(accounts)
        context['accounts_total'] = account_total

        asset_total = get_total_asset_value(assets)
        context['manual_assets_total'] = asset_total

        context['networth']= asset_total + account_total

        return context
    

class testview(ListView):
    model = ManualAsset
    context_object_name = "manual_asset"
    template_name = 'networth/test.html'