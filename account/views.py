import secrets
import time

from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    login,
    get_user_model,
    logout,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.db import transaction

from .forms import SignUpForm
from .models import UserProfile

User = get_user_model()

OTP_EXPIRY_SECONDS = 300  # 5 minutes
OTP_MAX_ATTEMPTS = 5
OTP_RESEND_WAIT = 60  # 1 minute


# PROFILE
@login_required
def profile(request):
    # Ensure existing users also have a profile.
    user_profile, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'phone_number': '',
            'country': '',
        },
    )

    return render(
        request,
        'profile.html',
        {'profile': user_profile},
    )


# SIGN IN
def sign_in(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        remember_me = request.POST.get('remember_me')

        account = User.objects.filter(email__iexact=email).first()

        user = None
        if account:
            user = authenticate(
                request,
                username=account.username,
                password=password,
            )

        if user is not None:
            login(request, user)

            if remember_me:
                # Keep the session for 2 weeks
                request.session.set_expiry(1209600)
            else:
                # Expire the session when the browser closes
                request.session.set_expiry(0)

            return redirect('home')

        messages.error(request, 'Invalid email or password.')

    return render(request, 'signin.html')

# SIGN UP
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data['first_name'].strip()
            last_name = form.cleaned_data['last_name'].strip()
            email = form.cleaned_data['email'].strip().lower()
            password = form.cleaned_data['password']
            phone_number = form.cleaned_data['phone_number'].strip()
            country = form.cleaned_data['country'].strip()

            try:
                validate_password(password)

                # Generate a username from the person's name.
                base_username = (
                    f'{first_name}{last_name}'
                    .replace(' ', '')
                    .lower()
                )

                # Ensure the username is not empty.
                if not base_username:
                    base_username = 'novauser'

                username = base_username
                counter = 1

                while User.objects.filter(
                    username=username
                ).exists():
                    username = f'{base_username}{counter}'
                    counter += 1

                # Create the user and profile together.
                with transaction.atomic():
                    user = User.objects.create_user(
                        username=username,
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        password=password,
                    )

                    UserProfile.objects.create(
                        user=user,
                        phone_number=phone_number,
                        country=country,
                    )

                messages.success(
                    request,
                    'Account created successfully. Please sign in.',
                )
                return redirect('login')

            except ValidationError as error:
                for message in error.messages:
                    form.add_error('password', message)

        return render(request, 'signup.html', {'form': form})

    form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


# FORGOT PASSWORD: SEND OTP
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()

        if not email:
            messages.error(
                request,
                'Please enter your email address.',
            )
            return render(request, 'forgot_password.html')

        user = User.objects.filter(email__iexact=email).first()

        if user:
            last_sent = request.session.get('otp_last_sent', 0)

            if time.time() - last_sent < OTP_RESEND_WAIT:
                messages.error(
                    request,
                    'Please wait before requesting another code.',
                )
                return render(request, 'forgot_password.html')

            otp = f'{secrets.randbelow(1000000):06d}'

            try:
                send_mail(
                    subject='NOVA Password Reset Verification',
                    message=(
                        f'Your NOVA verification code is {otp}.\n\n'
                        'This code expires in 5 minutes. '
                        'Do not share it with anyone.'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )

            except Exception:
                messages.error(
                    request,
                    'Unable to send the email right now. '
                    'Please try again later.',
                )
                return render(request, 'forgot_password.html')

            request.session['reset_email'] = user.email
            request.session['reset_otp'] = otp
            request.session['otp_created_at'] = time.time()
            request.session['otp_attempts'] = 0
            request.session['otp_last_sent'] = time.time()
            request.session['otp_verified'] = False

        # Keep the response consistent for registered and
        # unregistered email addresses.
        messages.info(
            request,
            'If the email is registered, a verification code '
            'will be sent.',
        )
        return redirect('verify_otp')

    return render(request, 'forgot_password.html')


# VERIFY OTP
def verify_otp(request):
    if 'reset_email' not in request.session:
        messages.error(
            request,
            'Please start the password reset process.',
        )
        return redirect('forgot_password')

    if request.method == 'POST':
        otp_entered = request.POST.get('otp', '').strip()
        saved_otp = request.session.get('reset_otp')
        created_at = request.session.get('otp_created_at', 0)
        attempts = request.session.get('otp_attempts', 0)

        # Reject missing or expired codes.
        if not saved_otp or time.time() - created_at > OTP_EXPIRY_SECONDS:
            clear_reset_session(request)
            messages.error(
                request,
                'Your verification code has expired. '
                'Please request a new one.',
            )
            return redirect('forgot_password')

        if attempts >= OTP_MAX_ATTEMPTS:
            clear_reset_session(request)
            messages.error(
                request,
                'Too many incorrect attempts. Please request a new code.',
            )
            return redirect('forgot_password')

        if secrets.compare_digest(otp_entered, saved_otp):
            request.session['otp_verified'] = True
            return redirect('new_password')

        request.session['otp_attempts'] = attempts + 1
        messages.error(
            request,
            'Invalid verification code. Please try again.',
        )

    return render(request, 'verify_otp.html')


# NEW PASSWORD
def new_password(request):
    if not request.session.get('otp_verified'):
        messages.error(
            request,
            'Please verify your email first.',
        )
        return redirect('forgot_password')

    email = request.session.get('reset_email')
    user = User.objects.filter(email__iexact=email).first()

    if not user:
        clear_reset_session(request)
        messages.error(
            request,
            'Unable to reset this account.',
        )
        return redirect('forgot_password')

    if request.method == 'POST':
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not password or not confirm_password:
            messages.error(
                request,
                'Please fill in both password fields.',
            )

        elif password != confirm_password:
            messages.error(
                request,
                'Passwords do not match.',
            )

        else:
            try:
                validate_password(password, user=user)

                user.set_password(password)
                user.save()

                clear_reset_session(request)

                messages.success(
                    request,
                    'Password reset successfully. Please sign in.',
                )
                return redirect('login')

            except ValidationError as error:
                for message in error.messages:
                    messages.error(request, message)

    return render(request, 'new_password.html')


# CLEAR PASSWORD-RESET SESSION DATA
def clear_reset_session(request):
    for key in (
        'reset_email',
        'reset_otp',
        'otp_created_at',
        'otp_attempts',
        'otp_last_sent',
        'otp_verified',
    ):
        request.session.pop(key, None)


# LOGOUT
def sign_out(request):
    if request.method == 'POST':
        logout(request)

    return redirect('home')
