from django.urls import path, include
from .import views 

app_name = 'cases'
urlpatterns = [
    path('', views.case_list, name='case_list'),
    path('<int:case_id>/', views.case_view, name='case_view'),
    # path('<int:case_id>/', views.case_add, name='case_add'),
    # path('section/', views.section_list, name='section_list'),    
    # path('<int:case_id>/section/<int:section_id>/', views.section_view, name='section_view'),    
    # path('<int:case_id>/section/<int:section_id>/caseparam/<int:caseparam_id>/', views.caseparam_view, name='caseparam_view'),
]
