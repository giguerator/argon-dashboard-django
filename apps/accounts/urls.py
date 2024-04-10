from django.urls import path, re_path

from . import views

urlpatterns = [
    path('accounts', views.AccountsListView.as_view(), name="accounts.list"),
    path('<int:parent_id>/accounts', views.AccountsListView.as_view(), name="accounts.filteredlist"),
    path('accounts/<int:pk>', views.AccountDetailsView.as_view(),name="account.detail"),
    re_path(r'accounts/((?P<parent_id>[0-9]+)/)?new',views.AccountCreateView.as_view(), name='account.new'),
    path('accounts/<int:pk>/edit', views.AccountUpdateView.as_view(),name="account.update"),
    path('accounts/<int:pk>/delete', views.AccountDeleteView.as_view(),name="account.delete"),

    path('institutions', views.InstitutionListView.as_view(), name="institutions.list"),
    path('institutions/<int:pk>', views.InstitutionDetailsView.as_view(),name="institution.detail"),
    path('institutions/new',views.InstitutionCreateView.as_view(), name='institution.new'),
    path('institutions/<int:pk>/edit', views.InstitutionUpdateView.as_view(),name="institution.update"),
    path('institutions/<int:pk>/delete', views.InstitutionDeleteView.as_view(),name="institution.delete"),
]