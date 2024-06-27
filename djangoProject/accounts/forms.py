from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from .models import CustomUser, Profile


# import requests  # Comment this out since we are mocking the API call

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


class LoginForm(AuthenticationForm):
    username = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

class CustomUserCreationForm(UserCreationForm):
    YEAR_CHOICES = [(year, str(year)) for year in range(2000, 2025)]
    year_of_joining = forms.ChoiceField(choices=YEAR_CHOICES, required=True)
    kcpe_index_number = forms.CharField(max_length=12, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'year_of_joining', 'kcpe_index_number', 'password1', 'password2')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'profile_image']
        widgets = {
            'profile_image': forms.FileInput(attrs={'accept': 'image/*'})
        }
class CustomPasswordResetForm(PasswordResetForm):
    username = forms.CharField(max_length=150)


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label="New password", strip=False, widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="New password confirmation", strip=False, widget=forms.PasswordInput)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'kcpe_marks', 'profile_image']
        widgets = {
            'profile_image': forms.FileInput(attrs={'accept': 'image/*'})
        }