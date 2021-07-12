from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    #url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

    path('admin/', admin.site.urls),
    path('', include('enroll.urls', namespace="enroll")),
    path('accounts/', include('accounts.urls',))
]
