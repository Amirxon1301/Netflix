from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from film.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', HelloAPI.as_view()),
    path('aktyorlar/', AktyorlarAPI.as_view()),
    path('aktyor/<int:pk>/', AktyorAPI.as_view()),
    path('tarif/<int:pk>/', TarifAPI.as_view()),
    path('tariflar/', TariflarAPI.as_view()),
    path('kinolar/', KinolarAPI.as_view()),
    path('kino/<int:pk>/', KinoAPI.as_view()),

    path('token/', obtain_auth_token),

    path('comments/', IzohListCreateAPI.as_view()),
    path('comments/<int:pk>/', IzohDestroyAPI.as_view())

]
