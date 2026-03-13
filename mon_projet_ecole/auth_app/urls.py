from django.urls import path
from .views import login_view, forgot_password_view

urlpatterns = [
    path('', login_view, name='login'),
    path('mot-de-passe-oublie/', forgot_password_view, name='forgot_password'), # Le 'name' est la clé !
]