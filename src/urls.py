from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.contrib.auth import views as auth_views

from Users import views

schema_view = get_schema_view(
    openapi.Info(
        title="Django Timer API",
        default_version='v1',
        description="Timer API Description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="aram.simonyan.03@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

a = 'api/v1/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'', include('Users.urls')),
    path('auth/', include('django.contrib.auth.urls')),  # new
    path('', views.main),  # new
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout, name='logout'),

    # path('auth/', include('djoser.urls')),
    # Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path('snippets/', login_required(views.snippet_list)),
]
