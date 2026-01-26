from django.contrib import admin
from django.urls import path, include





urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('website.urls', 'website'), namespace='website')),
    path('account/', include('customusers.urls')),

]
