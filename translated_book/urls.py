from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.views import serve

import session_csrf
from django.views.generic import TemplateView

session_csrf.monkeypatch()

from django.contrib import admin
admin.autodiscover()

urlpatterns = (
    # Examples:
    # url(r'^$', 'translated_book.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^_ah/', include('djangae.urls')),

    # Note that by default this is also locked down with login:admin in app.yaml
    url(r'^admin/', include(admin.site.urls)),

    url(r'^csp/', include('cspreports.urls')),

    url(r'^auth/', include('djangae.contrib.gauth.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include('rest_framework_swagger.urls')),

    url(r'^api/v1/', include('book.urls.api')),
    url(r'^tasks/', include('book.urls.task')),
)

if settings.DEBUG:
    urlpatterns += tuple(static(settings.STATIC_URL, view=serve, show_indexes=True))

urlpatterns += tuple(
    [url(r'^.*$', TemplateView.as_view(template_name='index.html'), name='index')]
)
