from django.conf.urls import url
from django.contrib.auth import views as v
from accounts.forms import LoginForm
from accounts import views as account_views
from accounts.views import ResetPasswordRequestView
from accounts.views import PasswordResetConfirmView


urlpatterns = [
    url(r'^login/$', v.login, {'template_name': 'accounts/login.html', 'authentication_form': LoginForm}, name='login'),
    url(r'^logout/$', v.logout, {'next_page': '/'},  name='logout'),
    url(r'^change_password$', account_views.change_password, name='change_password'),
    url(r'^edit_profile/$', account_views.user_profile, name='edit_profile'),
    url(r'^new/user/$', account_views.register, name='register'),
    url(r'^reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', PasswordResetConfirmView.as_view(),name='reset_password_confirm'),
    url(r'^password_success/$', account_views.password_success, name='password_success'),
    url(r'^forgot/$', ResetPasswordRequestView.as_view(), name='forgot'),
    url(r'^dashboard/$', account_views.dashboard, name='dashboard'),
    ]