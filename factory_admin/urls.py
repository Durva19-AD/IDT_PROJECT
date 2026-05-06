from django.urls import path
from . import views

app_name = 'factory_admin'

urlpatterns = [
    path('login/', views.admin_login_view, name='login'),
    path('logout/', views.admin_logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('materials/', views.materials_view, name='materials'),
    path('materials/delete/<int:pk>/', views.delete_material_view, name='delete_material'),
    path('inventory/', views.inventory_view, name='inventory'),
    path('requests/', views.requests_view, name='requests'),
    path('dimension-config/', views.dimension_config_view, name='dimension_config'),
]
