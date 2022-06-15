from django.contrib import admin
from django.urls import path, include
from .views import Gallery, home, HomeView
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home, name="home"),
    path('', HomeView.as_view(), name='homeview'),
    # path('', TemplateView.as_view(template_name='home.html'), name='homeview'),
    path('tuition/', include('tuition.urls')),
    path('session/', include('session.urls')),
    path('gallery/', Gallery, name='gallery'),
    path('inbox/notifications/', include('notifications.urls', namespace='notifications')),
    
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='session/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="session/password_reset_confirm.html"), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='session/password_reset_complete.html'), name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
