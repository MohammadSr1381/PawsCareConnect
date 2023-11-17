from django.urls import path , include
from . import views


urlpatterns = [
    path('roleClass/' , views.roleClass , name = 'roleClass'),
    path('registerUser/' , views.registerUser , name = 'registerUser'),
    path('registerClinic/' , views.registerClinic , name = 'registerClinic'),
    path('registerLaboratory/' , views.registerLaboratory , name = 'registerLaboratory'),

]