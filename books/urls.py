
from django.urls import path
from . import views

urlpatterns = [
    path('', views.optimized_queries_example, name='index'),
]