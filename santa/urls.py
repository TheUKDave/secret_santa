from django.conf.urls import url
from . import views

app_name = 'santa'

urlpatterns = [
    url(r'^$', views.HomepageView.as_view(), name='home'),
    url(r'^create/$', views.ListCreationView.as_view(), name='create'),
    url(r'^created/(?P<slug>[\w-]+)$', views.ListCreatedView.as_view(), name='created'),
    url(r'^signup/(?P<secure_hash>[a-f0-9]{12})/(?P<slug>[\w-]+)/$', views.SignupView.as_view(), name='signup'),
    url(r'^review/(?P<secure_hash>[a-f0-9]{12})/(?P<slug>[\w-]+)/$', views.ReviewListView.as_view(), name='review'),
    url(r'^close/(?P<secure_hash>[a-f0-9]{12})/(?P<slug>[\w-]+)/$', views.CloseListView.as_view(), name='close'),
    url(r'^thanks/$', views.ThanksView.as_view(), name='thanks'),
]
