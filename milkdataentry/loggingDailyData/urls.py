from django.urls import path
from . import views

app_name = 'loggingDailyData'

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('create/', views.EntryCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.EntryUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.EntryDeleteView.as_view(), name='delete'),
    path('saved/', views.SavedDisplay.as_view(), name='saved'),
    path('daily_total/', views.DailyTotal.as_view(), name='daily_total'),
    path('delete/', views.DailyTotal.as_view(), name='delete'),
    path('monthly_total/', views.monthly_milk, name='monthly_total'),
]