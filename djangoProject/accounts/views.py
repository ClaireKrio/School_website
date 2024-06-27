# views.py
import json
from urllib import request
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from allauth.account.views import PasswordResetView
from django.contrib.auth.views import PasswordResetConfirmView
# from .forms import SignUpForm, CustomUserCreationForm, CustomPasswordResetForm, CustomSetPasswordForm, ProfileForm
import requests

from .forms import ProfileForm, CustomUserCreationForm, CustomSetPasswordForm, CustomPasswordResetForm
# from .models import CustomUser, Profile
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .models import CustomUser, Profile


def home_view(request):
    return render(request, 'accounts/home.html')


@login_required
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')


def about_view(request):
    return render(request, 'accounts/about.html')


def academics(request):
    context = {
        'curriculum': 'Overview of the academic programs and subjects offered.',
        'departments_faculty': 'Information on academic departments and faculty profiles.',
        'class_schedules': 'Timetables for different grades and programs.',
        'academic_calendar': 'Key dates, holidays, and exam schedules.',
        'student_resources': 'Access to libraries, labs, and academic support services.'
    }
    return render(request, 'accounts/academics.html', context)


def contact_us(request):
    context = {
        'contact_information': 'Phone numbers, email addresses, and physical address.',
        'staff_directory': 'Comprehensive list of staff members and their contact details.',
        'feedback_inquiries': 'Forms for submitting questions, feedback, or concerns.'
    }
    return render(request, 'accounts/contact.html', context)


def feedback_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # You can save the feedback to the database or send an email
        # For simplicity, let's just return a success message
        return HttpResponse('Thank you for your feedback!')
    else:
        return redirect('contact_us')


def student_life(request):
    context = {
        'extracurricular_activities': 'Information on clubs, sports teams, and other activities.',
        'student_services': 'Counseling, health services, and support programs.',
        'code_of_conduct': 'Policies and expectations for student behavior.',
        'housing_dining': 'Details on residential options and meal plans (if applicable).'
    }
    return render(request, 'accounts/student_life.html', context)


def news_events(request):
    context = {
        'school_news': 'Updates on school activities and achievements.',
        'event_calendar': 'Upcoming events, including sports, performances, and meetings.',
        'photo_video_galleries': 'Visual highlights from recent events and activities.'
    }
    return render(request, 'accounts/news_events.html', context)


def admissions(request):
    context = {
        'how_to_apply': 'Step-by-step guide to the application process.',
        'admission_criteria': 'Requirements and eligibility for prospective students.',
        'tours_open_houses': 'Information on visiting the school.',
        'tuition_fees': 'Details on the cost of attendance and available payment options.',
        'scholarships_financial_aid': 'Information on financial support and scholarship opportunities.'
    }
    return render(request, 'accounts/admissions.html', context)


# def register(request):
#     if request.method == 'POST':
#         user_form = CustomUserCreationForm(request.POST)
#         profile_form = ProfileForm(request.POST, request.FILES)
#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save()
#             profile = profile_form.save(commit=False)
#             profile.user = user
#             profile.full_name = f"{user.first_name} {user.last_name}"
#             profile.kcpe_marks = user.kcpe_results
#             profile.save()
#             return redirect('signin')
#         else:
#             return render(request, 'accounts/register.html', {'user_form': user_form, 'profile_form': profile_form})
#     else:
#         user_form = CustomUserCreationForm()
#         profile_form = ProfileForm()
#     return render(request, 'accounts/register.html', {'user_form': user_form, 'profile_form': profile_form})



def register(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.full_name = f"{user.first_name} {user.last_name}"
            profile.save()
            messages.success(request, 'Registration successful.')
            return redirect('signin')
        else:
            messages.error(request, 'Registration unsuccessful. Please correct the errors below.')
    else:
        user_form = CustomUserCreationForm()
        profile_form = ProfileForm()

    return render(request, 'accounts/register.html', {'user_form': user_form, 'profile_form': profile_form})
def signin_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                return render(request, 'accounts/signin.html', {'form': form, 'error': 'Invalid login credentials'})
        else:
            return render(request, 'accounts/signin.html', {'form': form, 'error': 'Invalid login credentials'})
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/signin.html', {'form': form})


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'profile': request.user.profile})


@login_required
def admission_letter_view(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="admission_letter.pdf"'
    # Your code to generate the PDF goes here
    return response


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    success_url = '/password_reset/done/'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = '/signin'


def check_admission_status(student_id):
    # Replace with the actual API endpoint and required headers or parameters
    api_url = "https://government-api.example.com/check-admission"
    response = requests.post(api_url, data={'student_id': student_id})
    return response.json()


# views.py

@login_required
def generate_admission_letter(request):
    # Fetch the logged-in user's details
    user = request.user

    # Dummy data for fees structure, you can replace it with actual data as per your database
    fees_structure = {
        'term_1': 20000,
        'term_2': 15000,
        'term_3': 10000,
        'total': 45000,
    }

    # Current date for admission date
    admission_date = timezone.now().strftime("%Y-%m-%d")

    context = {
        'user': user,
        'fees_structure': fees_structure,
        'admission_date': admission_date,
    }

    return render(request, 'accounts/admission_letter.html', context)


def send_notification_email(user):
    subject = 'Admission Status Notification'
    message = f'Dear {user.first_name},\n\nYou have not been selected for admission at this time. You will be notified via email if space becomes available.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
