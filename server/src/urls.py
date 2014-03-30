from django.conf.urls import patterns
from django.conf.urls import url
from django.conf.urls import include
from django.contrib.auth.decorators import login_required

from search.views import Index
from search.views import Proxy
from search.views import FindGroups
from search.views import FindPosts

# Create your views here.
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', Index.as_view(), name='index'),
    url(r'^findPosts/$', login_required(FindPosts.as_view()), name='find_posts'),
    url(r'^findGroups/$', login_required(FindGroups.as_view()), name='find_groups'),
    url(r'^proxy/$', login_required(Proxy.as_view()), name='proxy'),
    url(r'^account/', include('account.urls')),
    url(r'^control-center/', include(admin.site.urls)),
)
