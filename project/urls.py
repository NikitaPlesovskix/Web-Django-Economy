from django.contrib import admin
from django.urls import path, include 

urlpatterns = [    
    path('__debug__/', include('debug_toolbar.urls')), #Мод для дебага
    path('admin/', admin.site.urls),
	path('cases/', include('cases.urls')),
	path('', include('cases.urls')),
]
