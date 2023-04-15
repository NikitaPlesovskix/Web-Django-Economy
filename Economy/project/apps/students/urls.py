from django.urls import path, include

from .import views 

app_name = 'students'
urlpatterns = [
    path('', views.case_list, name='case_list'),
    # path('case_add/', views.case_add, name='case_add'),
    # path('<int:case_id>/', views.case_view, name='case_view'),
    # path('<int:case_id>/case_edit', views.case_edit, name='case_edit'),
    # path('<int:case_id>/period_add/', views.period_add, name='period_add'),
    # path('<int:case_id>/section_add/', views.section_add, name='section_add'),
    # path('<int:case_id>/parameter_add/', views.parameter_add, name='parameter_add'),
    # path('<int:case_id>/section_parameter/', views.section_parameter, name='section_parameter'),
    # path('<int:case_id>/section/<int:section_id>/', views.section_view, name='section_view'), 
    # path('<int:case_id>/section_edit/<int:section_id>/', views.section_edit, name='section_edit'),
]
