from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from accounts.forms import ProfileForm, SignUpForm, PasswordResetRequestForm, SetPasswordForm
from accounts.models import UserProfile, SnapLink
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from SnapUp.settings import DEFAULT_FROM_EMAIL
from django.views.generic import *
from django.contrib import messages
from django.db.models.query_utils import Q
from django.contrib.auth import get_user_model
from django.db.models import Q


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return render(request, 'accounts/change_password.html', {'form': form})
        else:
            messages.error(request, 'Wrong Old Password or New Passwords Does Not Match.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })


@login_required
def user_profile(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Profile Successfully Updated')
        else:
            messages.error(request, 'Oops!!! There was an error')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'accounts/profile.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if not form.is_valid():
            return render(request, 'accounts/signup.html',
                          {'form': form})

        else:
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, password=password,
                                     email=email)
            user = authenticate(username=username, password=password)
            login(request, user)
            welcome_post = '{0} has joined the network.'.format(user.username,
                                                                user.username)
            #feed = Feed(user=user, post=welcome_post)
            #feed.save()
            return redirect('/accounts/edit_profile')

    else:
        return render(request, 'accounts/signup.html',
                      {'form': SignUpForm()})


class ResetPasswordRequestView(FormView):
        template_name = "accounts/forgot.html"
        success_url = '/forgot'
        form_class = PasswordResetRequestForm

        @staticmethod
        def validate_email_address(email):
            try:
                validate_email(email)
                return True
            except ValidationError:
                return False

        def post(self, request, *args, **kwargs):

            form = self.form_class(request.POST)
            if form.is_valid():
                data= form.cleaned_data["email_or_username"]
            if self.validate_email_address(data) is True:
                associated_users = User.objects.filter(Q(email=data)|Q(username=data))
                if associated_users.exists():
                    for user in associated_users:
                            c = {
                                'email': user.email,
                                'domain': request.META['HTTP_HOST'],
                                'site_name': 'SnapUp',
                                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                'user': user,
                                'token': default_token_generator.make_token(user),
                                'protocol': 'http',
                                }
                            subject_template_name = 'accounts/password_reset_subject.txt'
                            email_template_name = 'accounts/password_reset_email.html'
                            subject = loader.render_to_string(subject_template_name, c)
                            subject = ''.join(subject.splitlines())
                            email = loader.render_to_string(email_template_name, c)
                            send_mail(subject, email, DEFAULT_FROM_EMAIL , [user.email], fail_silently=False)
                    result = self.form_valid(form)
                    messages.success(request, 'An email has been sent to ' + data +". Please check inbox to continue password reset.")
                    return result
                result = self.form_invalid(form)
                messages.error(request, 'No user is associated with this email address')
                return result
            else:

                associated_users= User.objects.filter(username=data)
                if associated_users.exists():
                    for user in associated_users:
                        c = {
                            'email': user.email,
                            'domain': 'http://snapupng.pythonanywhere.com/', #or your domain
                            'site_name': 'SnapUp',
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'user': user,
                            'token': default_token_generator.make_token(user),
                            'protocol': 'http',
                            }
                        subject_template_name='accounts/password_reset_subject.txt'
                        email_template_name='accounts/password_reset_email.html'
                        subject = loader.render_to_string(subject_template_name, c)
                        # Email subject *must not* contain newlines
                        subject = ''.join(subject.splitlines())
                        email = loader.render_to_string(email_template_name, c)
                        send_mail(subject, email, DEFAULT_FROM_EMAIL , [user.email], fail_silently=False)
                    result = self.form_valid(form)
                    messages.success(request, 'Email has been sent to ' + data +"'s email address. Please check inbox to continue password reset.")
                    return result
                result = self.form_invalid(form)
                messages.error(request, 'This username does not exist in the system.')
                return result
            messages.error(request, 'Invalid Input')
            return self.form_invalid(form)


class PasswordResetConfirmView(FormView):
    template_name = "accounts/password_new.html"
    success_url = '/'
    form_class = SetPasswordForm

    def post(self, request, uidb64=None, token=None, *arg, **kwargs):
        """
        View that checks the hash in a password reset link and presents a
        form for entering a new password.
        """
        UserModel = get_user_model()
        form = self.form_class(request.POST)
        assert uidb64 is not None and token is not None  # checked by URLconf
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            if form.is_valid():
                new_password= form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password has been reset.')
                return self.form_valid(form)
            else:
                messages.error(request, 'Password reset has not been successful.')
                return self.form_invalid(form)
        else:
            messages.error(request,'The reset password link is no longer valid.')
            return self.form_invalid(form)


@login_required
def password_success(request):
    return render(request, 'accounts/password_success.html', {})


@login_required
def dashboard(request):
    user_name = request.user.username
    user_dashboard_total_snap_links = SnapLink.objects.filter(user=user_name).count()
    user_dashboard_total_unset_snap_links = SnapLink.objects.filter(user=user_name).filter(notify_me_type='None').count()
    user_dashboard_total_set_snap_links = SnapLink.objects.filter(user=user_name).filter(~Q(notify_me_type = 'None')).count()
    snap_linker_points = user_dashboard_total_set_snap_links * 1.5
    return render(request, 'accounts/dashboard.html', {'user_dashboard_total_snap_links': user_dashboard_total_snap_links,
                                                       'user_dashboard_total_unset_snap_links': user_dashboard_total_unset_snap_links,
                                                       'user_dashboard_total_set_snap_links': user_dashboard_total_set_snap_links,
                                                       'snap_linker_points': snap_linker_points})