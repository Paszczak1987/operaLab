from django.urls import path
from . import views

app_name = 'labs'

urlpatterns = [
    # path('add/', views.labs_add, name='labs_add'),
    path('list/', views.LabListView.as_view(), name='list'),
    # path('edit/<int:id>/', views.labs_edit, name='labs_edit'),
    # path('delete/<int:id>/', views.labs_delete, name='labs_delete'),
    path('detail_view/<int:pk>/', views.LabDetailView.as_view(), name='detail_view'),
]
