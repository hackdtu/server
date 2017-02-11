from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'healthBub.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^patient$', 'main.views.index', name='patient'),
    url(r'^doctor$', 'main.views.doc', name='doctor'),
    url(r'^government$', 'main.views.govt', name='governemnt'),
    url(r'^info$', 'main.views.info', name='info'),
    url(r'^graph$', 'main.views.graph', name='graph'),
    url(r'^chart$', 'main.views.chart', name='graph'),
    url(r'^category$', 'main.views.category', name='category'),


)
