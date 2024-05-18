from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode


def send_confirmation_email(confirm_url, email):
    """Send confirmation email to user."""
    subject = 'Confirm your email'
    message = f'Please click the link below to confirm your email address: {confirm_url}'
    from_email = 'ivsivovs@yandex.ru'
    to_email = [email]
    send_mail(subject, message, from_email, to_email, fail_silently=False)


def generator_token_email(user):
    """Generate token for email confirmation."""
    token = default_token_generator.make_token(user)
    uidb64 = urlsafe_base64_encode(str(user.pk).encode())
    confirm_url = f'http://localhost:8000/confirm_email/{uidb64}/{token}'

    return confirm_url
