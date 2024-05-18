from django import forms

from .models import CustomUser
from django.contrib.auth.forms import BaseUserCreationForm


class CustomUserCreationForm(BaseUserCreationForm):
    """Custom user creation form."""
    class Meta:
        model = CustomUser
        fields = ('email', 'username')

    def save(self, commit=True):
        """Save user and send confirmation email."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        # Account is not active by default
        user.is_active = False
        if commit:
            user.save()
        return user


class EditProfileForm(forms.ModelForm):
    """Edit profile form."""
    email = forms.EmailField(label='New Email', required=False)
    username = forms.CharField(label='New Username', required=False)
    old_password = forms.CharField(widget=forms.PasswordInput, required=False)
    new_password = forms.CharField(widget=forms.PasswordInput, required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'old_password', 'new_password', 'confirm_password')
