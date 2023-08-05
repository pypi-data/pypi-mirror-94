import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth
from django.contrib import admin
from django.urls import path, include

from lavender.views import registration, profile
from lavender.views.api import packages, telemetry
from lavender.views.nidhoggr import textures, users

nidhoggr_urlpatterns = [
    path('user/get', users.get),
    path('user/check_password', users.check_password),
    path('user/save', users.save),

    path('texture/get', textures.get),
]


urlpatterns = [
    path('', auth.LoginView.as_view(redirect_authenticated_user=True)),

    path('admin/', admin.site.urls),
    path('accounts/login/', auth.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('accounts/logout/', auth.LogoutView.as_view(), name='logout'),

    path('accounts/password_change/', auth.PasswordChangeView.as_view(), name='password_change'),
    path('accounts/password_change/done/', auth.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('accounts/password_reset/', auth.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', auth.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('accounts/registration/', registration.registration, name='registration'),
    path('accounts/profile/', profile.profile, name='profile'),

    path('api/v1/nidhoggr/', include(nidhoggr_urlpatterns)),

    path('api/v1/logs/upload/', telemetry.save_logs),
    path('api/v1/packages/list/', packages.package_list),

    # FIXME: Deprecated and will be removed soon
    path('api/packages/', packages.package_list),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
