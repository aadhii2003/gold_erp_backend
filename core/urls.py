from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core.views import CustomTokenObtainPairView
from apps.sales.views import sync_sales, SalesListView
from apps.users.views import (
    UserListView, UserCreateView, UserDetailView, UserDeleteView, UserStatusToggleView,
    BranchCreateView, BranchListView, BranchDetailView,
    UOMListView, CurrencyListView,
    ExpenseListView, ExpenseCreateView, AdminLogListView
)
from apps.gold_rates.views import RateDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Auth
    path('api/auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Sales
    path('api/sales/', SalesListView.as_view(), name='sales-list'),
    path('api/sales/sync/', sync_sales, name='sync-sales'),
    
    # Settings (Rates)
    path('api/rates/', RateDetailView.as_view(), name='rates'),

    # Admin/Manager Management
    path('api/users/', UserListView.as_view(), name='users-list'),
    path('api/users/create/', UserCreateView.as_view(), name='user-create'),
    path('api/users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('api/users/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
    path('api/users/<int:pk>/toggle/', UserStatusToggleView.as_view(), name='user-toggle'),
    
    path('api/branches/', BranchListView.as_view(), name='branch-list'),
    path('api/branches/create/', BranchCreateView.as_view(), name='branch-create'),
    path('api/branches/<int:pk>/', BranchDetailView.as_view(), name='branch-detail'),
    
    # Expenses
    path('api/expenses/', ExpenseListView.as_view(), name='expense-list'),
    path('api/expenses/create/', ExpenseCreateView.as_view(), name='expense-create'),

    # Constants
    path('api/uoms/', UOMListView.as_view(), name='uom-list'),
    path('api/currencies/', CurrencyListView.as_view(), name='currency-list'),
    path('api/admin-logs/', AdminLogListView.as_view(), name='admin-logs'),
    path('api/density-purity/', include('apps.density_purity.urls')),
]
