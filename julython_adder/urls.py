from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


urlpatterns = patterns(
    '', # prefix
    url(r'', include('social_auth.urls')),
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^logged-in/$', 'julython_adder.adder.views.logged_in',
        name='logged-in'),
)
