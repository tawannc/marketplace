from django.urls import path
from . import views

urlpatterns = [
    path('criar/<int:product_id>/', views.criar_review, name='criar_review'),
]
