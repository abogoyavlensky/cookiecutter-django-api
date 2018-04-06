"""
    config/urls.py
    ~~~~~~~~~~~~~~

    Common url config.

    :copyright: (c) 2018 by {{cookiecutter.author}}.
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views
from rest_framework.documentation import include_docs_urls
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)
from .routers import router_v1

urlpatterns = [
    url(settings.ADMIN_URL, admin.site.urls),
    # API
    url(r'^api/v1/', include((router_v1.urls, 'v1'))),
    url(r'^api/token/$', TokenObtainPairView.as_view(), name='token-obtain'),
    url(r'^api/token/refresh/$', TokenRefreshView.as_view(),
        name='token-refresh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DJANGO_SHOW_API_DOCS:
    urlpatterns += [
        url(r'^api/docs/',
            include_docs_urls(title='{{cookiecutter.project_name}}',
                              public=False))
    ]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request,
            kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied,
            kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found,
            kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if settings.USE_DEBUG_TOOLBAR:
        import debug_toolbar
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns

    if settings.USE_DJANGO_SILK:
        urlpatterns += [url(r'^silk/', include('silk.urls', namespace='silk'))]
