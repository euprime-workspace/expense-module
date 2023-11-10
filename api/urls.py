from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    path('users/', views.UserListCreateView.as_view(), name='Read Users and Create User'),
    path('token/obtain/', TokenObtainPairView.as_view(), name='Create Access Token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='Refresh Access Token'),
    path('projects/', views.ProjectListCreateView.as_view(), name='Read Projects and Create Project'),
    path('items/', views.ItemListCreateView.as_view(), name='Read Items and Create Item'),
    path('action_items/', views.ActionItemListCreateView.as_view(), name='Read Action Items and Create Action Item'),
    path('expenses/', views.ExpenseHeaderListCreateView.as_view(), name='Read Expense Headers and Create Expense Header'),
    path('expenses/<uuid:UUID>/', views.ExpenseHeaderRetrieveUpdateDestroyView.as_view(), name='Read, Update and Delete Expense Header'),
    path('expenses/history/<uuid:UUID>/',views.expense_header_history,name="Read Expense Header History"),
    path('expenses/lines/', views.ExpenseLineListCreateAPIView.as_view(), name='Read Expense Lines and Create Expense Line'),
    path('expenses/lines/<uuid:UUID>/', views.ExpenseLineRetrieveUpdateDestroyView.as_view(), name='Read, Update and Delete Expense Header'),
    path('expenses/lines/history/<uuid:UUID>/', views.expense_line_history, name='Read Expense Line History'),
    path('expenses/<uuid:header_id>/lines/', views.ExpenseLinesByExpenseHeader.as_view(), name = 'Read and Create Expense Lines By Expense Header'),
    path('expenses/<uuid:header_id>/lines/<uuid:UUID>/', views.ExpenseLineByExpenseHeaderAndExpenseLineRetrieveUpdateDestroyView.as_view(), name = 'Read, Update and Delete Expense Line By Expense Header And Expense Line'),
]