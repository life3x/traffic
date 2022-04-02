from django.urls import path, re_path
from . import views

urlpatterns = [
    # re_path(r'(?P<username_slug>[-\w]+)/(?P<lat_slug>\d+\.\d+)/(?P<long_slug>\d+\.\d+)$', views.index, name = 'index'),
    path('', views.index, name = 'index'),
    path('mapper/<slug:username_val>/<slug:site_id>', views.mapper, name = 'mapper'),
    path('storeData/<slug:username_slug>/<access_token>/<site_id>/<lat_slug>/<long_slug>/<ip_address_slug>', views.storeData, name = 'storeData'),
    path('coordsDataJson/<slug:site_id>', views.coordsDataJson, name = 'coordsDataJson'),
    path('registered-sites', views.registeredSiteDataJson, name = 'registeredSiteDataJson'),
    path('mapper/<slug:username_val>', views.mapperRedirect, name = 'mapperRedirect'),
    path('integrate', views.integration, name = 'integration'),
]
