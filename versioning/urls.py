from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.urls import path, re_path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter, BaseRouter
from versioning import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
# router.register(r'documents', views.DocumentViewSet)
router.register(r'users', views.UserViewSet)
# router.register(r'revisions', views.RevisionViewSet)


# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    path('documents/<path:url>/revisions/', views.DocumentViewSet.as_view({'get': 'list'})),
    path('documents/<path:url>/', views.DocumentViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    url(r'^documents/$', views.DocumentViewSet.as_view({'get': 'list', 'post': 'perform_create', 'put': 'update'})),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    url(r'^whoami/$', views.WhoamIViewSet.as_view({'get': 'retrieve'})),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

a='d'
