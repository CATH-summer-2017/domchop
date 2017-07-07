from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^tst/', include('tst.urls')),
    url(r'^admin/', admin.site.urls),
]
