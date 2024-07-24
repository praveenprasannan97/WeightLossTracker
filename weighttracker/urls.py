from django.urls import path, include
from hp import views

urlpatterns = [
    path('', views.hp),
    path('wt/', include('wt.urls')),
]
