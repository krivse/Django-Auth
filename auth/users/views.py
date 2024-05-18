from django.contrib import messages
from django.contrib.auth import logout, login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode

from .forms import CustomUserCreationForm, EditProfileForm
from .models import CustomUser
from .services import send_confirmation_email, generator_token_email


def index(request):
    return render(request, 'index.html')


@login_required()
def profile(request):
    """Profile view.
    If user is authenticated, render profile.html.
    If user is not authenticated, redirect to index page.

    :args: request

    :returns: render profile.html"""
    return render(request, 'profile.html')


@login_required()
def edit_profile(request):
    """Edit profile view.
    If user is authenticated, render edit_profile.html.
    If user is not authenticated, redirect to index page.

    :args: request

    :returns: render edit_profile.html"""
    form = EditProfileForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():

            user = request.user
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            if username:
                user.username = username
            if email:
                user.email = email

            old_password = form.cleaned_data.get('old_password')
            new_password = form.cleaned_data.get('new_password')
            confirm_password = form.cleaned_data.get('confirm_password')

            if old_password and new_password and confirm_password:
                if user.check_password(old_password):
                    if new_password == confirm_password:
                        user.set_password(new_password)
                        # Update session auth hash if password is changed
                        update_session_auth_hash(request, user)
                    else:
                        return HttpResponseNotFound('Passwords do not match')
                else:
                    return HttpResponseNotFound('Old password is incorrect')

            user.save()
            messages.success(request, 'Profile successfully updated')
            return redirect('index')
    return render(request, 'edit_profile.html', {'form': form})


def register(request):
    """Register view.
    If POST request, create new user. If user is created,
    redirect to index page. If user is not created, render register.html.

    :args: request

    :returns: render register.html or redirect to index page"""
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = CustomUserCreationForm(request.POST)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                user = form.instance
                confirm_url = generator_token_email(user)
                send_confirmation_email(confirm_url, request.POST.get('email'))
                messages.success(
                    request,
                    'Confirm your email address to complete registration'
                )
                return redirect('index')
        return render(
            request,
            'register.html',
            {'form': form}
        )


def confirm_email_view(request, uidb64, token):
    """Confirm email view.
    If user is authenticated, redirect to index page.
    If user is not authenticated, render httpResponseNotFound.

    :args: request, uidb64, token

    :returns: redirect to index page or httpResponseNotFound"""
    if request.user.is_authenticated:
        return redirect('index')
    uid = urlsafe_base64_decode(uidb64).decode('utf-8')
    user: CustomUser = CustomUser.objects.get(pk=uid)

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request,
            'Your email address has been confirmed'
        )
        return redirect('login')
    else:
        return HttpResponseNotFound('Activation link is invalid')


def login_view(request):
    """Login view.
    If POST request, authenticate user. If user is authenticated,
    redirect to index page. If user is not authenticated, render login.html.

    :args: request

    :returns: render login.html or redirect to index page"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(
                request,
                'login.html',
                {'error': 'Username or password is incorrect.'}
            )
    else:
        return render(request, 'login.html')


def logout_view(request):
    """Logout view.
    If user is authenticated, logout and redirect to index page.

    :arg: request - request object from view function

    :returns: redirect to index page."""
    logout(request)
    return redirect('index')


@login_required()
def list_users(request):
    """List users view.
    If user is authenticated, render list_users.html.

    :arg: request - request object from view function

    :returns: render list_users.html"""
    users = CustomUser.objects.all()
    return render(request, context={'users': users}, template_name='list_users.html')
