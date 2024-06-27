from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('signup/', views.register, name='signup'),
    path('signin/', views.signin_view, name='signin'),
    # path('logout/', views.logout_view, name='logout'),
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('about/', views.about_view, name='about'),
    path('academics/', views.academics, name='academics'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('feedback-submit/', views.feedback_submit, name='feedback_submit'),
    path('student-life/', views.student_life, name='student_life'),
    path('news-events/', views.news_events, name='news_events'),
    path('admissions/', views.admissions, name='admissions'),
    path('register/', views.register, name='register'),
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('admission_letter/', views.generate_admission_letter, name='admission_letter'),
    path('profile/', views.profile_view, name='profile'),
]

if settings.DEBUG:  # Only add this during development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)