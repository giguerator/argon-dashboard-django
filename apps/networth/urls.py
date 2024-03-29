from django.urls import path

from . import views

urlpatterns = [
    path('manual_assets', views.ManualAssetListView.as_view(), name="manual_assets.list"),
    path('manual_assets/<int:pk>', views.ManualAssetDetailsView.as_view(),name="manual_asset.detail"),
    path('manual_assets/new',views.ManualAssetCreateView.as_view(), name='manual_asset.new'),
    path('manual_assets/<int:pk>/edit', views.ManualAssetUpdateView.as_view(),name="manual_asset.update"),
    path('manual_assets/<int:pk>/delete', views.ManualAssetDeleteView.as_view(),name="manual_asset.delete"),
    
    path('summary', views.NetworthSummaryView.as_view(), name="networth.summary"),
    path('test',views.testview.as_view(), name="test")
]