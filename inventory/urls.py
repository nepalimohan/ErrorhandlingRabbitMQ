from django.urls import path
from . import views

urlpatterns = [
    path('', views.InventoryView.as_view(), name="inventory_view"),
    path('delete/', views.InventoryDeleteError.as_view(), name="inventory_delete"),
]
