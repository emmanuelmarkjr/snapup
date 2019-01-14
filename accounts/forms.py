from django.contrib.auth.forms import AuthenticationForm
from django import forms
from accounts.models import UserProfile, SnapLink
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from SnapUp.settings import ALLOWED_SIGNUP_DOMAINS


def SignupDomainValidator(value):
    if '*' not in ALLOWED_SIGNUP_DOMAINS:
        try:
            domain = value[value.index("@"):]
            if domain not in ALLOWED_SIGNUP_DOMAINS:
                raise ValidationError('Invalid domain. Allowed domains on this network: {0}'.format(','.join(ALLOWED_SIGNUP_DOMAINS)))  # noqa: E501

        except Exception:
            raise ValidationError('Invalid domain. Allowed domains on this network: {0}'.format(','.join(ALLOWED_SIGNUP_DOMAINS)))  # noqa: E501


def ForbiddenUsernamesValidator(value):
    forbidden_usernames = ['admin', 'settings', 'news', 'about', 'help',
                           'signin', 'signup', 'signout', 'terms', 'privacy',
                           'cookie', 'new', 'login', 'logout', 'administrator',
                           'join', 'account', 'username', 'root', 'blog',
                           'user', 'users', 'billing', 'subscribe', 'reviews',
                           'review', 'blog', 'blogs', 'edit', 'mail', 'email',
                           'home', 'job', 'jobs', 'contribute', 'newsletter',
                           'shop', 'profile', 'register', 'auth',
                           'authentication', 'campaign', 'config', 'delete',
                           'remove', 'forum', 'forums', 'download',
                           'downloads', 'contact', 'blogs', 'feed', 'feeds',
                           'faq', 'intranet', 'log', 'registration', 'search',
                           'explore', 'rss', 'support', 'status', 'staticfiles',
                           'media', 'setting', 'css', 'js', 'follow',
                           'activity', 'questions', 'articles', 'network', ]

    if value.lower() in forbidden_usernames:
        raise ValidationError('This is a reserved word.')


def InvalidUsernameValidator(value):
    if '@' in value or '+' in value or '-' in value:
        raise ValidationError('Enter a valid username.')


def UniqueEmailValidator(value):
    if User.objects.filter(email__iexact=value).exists():
        raise ValidationError('User with this Email already exists.')


def UniqueUsernameIgnoreCaseValidator(value):
    if User.objects.filter(username__iexact=value).exists():
        raise ValidationError('User with this Username already exists.')


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username',
                                                             'placeholder': ' Username'}))
    password = forms.CharField(max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password',
                                                                 'placeholder': 'Password'}))


class ProfileForm(forms.ModelForm):

    picture = forms.ImageField(required=False, widget=forms.FileInput)

    class Meta:
        model = UserProfile
        fields = ('full_name', 'phone', 'picture')


class SignUpForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        max_length=30,
        label="",
        required=True)
        #help_text='Usernames may contain <strong>alphanumeric</strong>, <strong>_</strong> and <strong>.</strong> characters')  # noqa: E261
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label="",
        )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        label="",
        required=True)
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        required=True,
        label="* Please a functional email as emails cannot be changed and you would get your snap links price notifications here ",
        max_length=75)

    class Meta:
        model = User
        exclude = ['last_login', 'date_joined']
        fields = ['username', 'email', 'password', 'confirm_password', ]

    def __init__(self, *args, **kwargs):
            super(SignUpForm, self).__init__(*args, **kwargs)
            self.fields['username'].validators.append(ForbiddenUsernamesValidator)
            self.fields['username'].validators.append(InvalidUsernameValidator)
            self.fields['username'].validators.append(
                UniqueUsernameIgnoreCaseValidator)
            self.fields['email'].validators.append(UniqueEmailValidator)
            self.fields['email'].validators.append(SignupDomainValidator)

    def clean(self):
            super(SignUpForm, self).clean()
            password = self.cleaned_data.get('password')
            confirm_password = self.cleaned_data.get('confirm_password')
            if password and password != confirm_password:
                self._errors['password'] = self.error_class(
                    ['Passwords don\'t match'])
            return self.cleaned_data


class PasswordResetRequestForm(forms.Form):
    email_or_username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',  'placeholder': 'Email Or Username'}),
                                            label=(""), max_length=254)


class SetPasswordForm(forms.Form):
        """
        A form that lets a user change set their password without entering the old
        password
        """
        error_messages = {
            'password_mismatch': ("The two password fields didn't match."),
        }
        new_password1 = forms.CharField(label=(" "),
                                        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New password'}))
        new_password2 = forms.CharField(label=(" "),
                                        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New password confirmation'}))

        def clean_new_password2(self):
            password1 = self.cleaned_data.get('new_password1')
            password2 = self.cleaned_data.get('new_password2')
            if password1 and password2:
                if password1 != password2:
                    raise forms.ValidationError(
                        self.error_messages['password_mismatch'],
                        code='password_mismatch',
                    )
            return password2


class NewSnapLinkForm(forms.ModelForm):

    class Meta:
        model = SnapLink
        fields = ('snap_link', )

