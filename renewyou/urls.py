"""
URL configuration for renewyou project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from health import views
from django.urls import path, include 



urlpatterns = [
    path("admin/", admin.site.urls),
    path('',views.index,name='home'),
    path('healthcare_tips/', views.healthcare_tips, name='healthcare_tips'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.login, name='login'),
    path('userprofile/', views.userprofile, name='userprofile'),
    path('personalised_nutrition/', views.personalised_nutrition, name='personalised_nutrition'),
    path('food_recommendations/', views.food_recommendation_view, name='food_recommendation'),
    path('tracking/', views.tracking_dashboard, name='tracking_dashboard'),
    path('start-tracking/', views.start_tracking, name='start_tracking'),
    path("mark-day/<int:daily_id>/", views.mark_daily_tracking, name="mark_daily_tracking"),
    path('help/', views.help, name='help'),
    path("chatbot-api/", views.chatbot_api, name="chatbot_api"),
    path('api/', include('health.urls')),
    path('logout/', views.logout_view, name='logout'),
    path('reset-tracking/', views.reset_tracking, name='reset_tracking'),
    path('forgot/', views.forgot_password, name='forgot_password'),
    path('adminhome/', views.adminhome, name='adminhome'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('appointments/', views.appointments, name='appointments'),
    


]


from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )

