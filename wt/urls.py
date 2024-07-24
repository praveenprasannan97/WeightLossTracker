from django.urls import path
from wt import views

urlpatterns = [
    path('', views.weight_list, name='weight_list'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_form, name='login'),
    path('logout/', views.logout, name='logout'),
    path('add_weight/', views.add_weight, name='add_weight'),
    path('edit_weight/<int:pk>/', views.edit_weight, name='edit_weight'),
    path('delete_weight/<int:pk>/', views.delete_weight, name='delete_weight'),
    path('weight_loss/', views.weight_loss, name='weight_loss'),
]