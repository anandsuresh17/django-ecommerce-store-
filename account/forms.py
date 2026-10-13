from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class SignUpForm(forms.Form):
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter first name',
            'autocomplete': 'given-name',
        })
    )

    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter last name',
            'autocomplete': 'family-name',
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter email address',
            'autocomplete': 'email',
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Create password',
            'autocomplete': 'new-password',
        })
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm password',
            'autocomplete': 'new-password',
        })
    )

    phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter phone number',
            'autocomplete': 'tel',
        })
    )

    country = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter country',
            'autocomplete': 'country-name',
        })
    )

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                'This email is already registered. Please sign in.'
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if (
            password
            and confirm_password
            and password != confirm_password
        ):
            self.add_error(
                'confirm_password',
                'Passwords do not match.'
            )

        return cleaned_data
