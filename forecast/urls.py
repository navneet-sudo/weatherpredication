from django.urls import path
from django.contrib.auth import views as auth_views  # Importing Django's built-in auth views
from.import views  # Import your app's views

urlpatterns = [
    # Set login as the default page (for non-authenticated users)
    path('', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),

    # Weather view (require login to access)
    path('weather/', views.weather_view, name='weather_view'),

    # Login
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),

    # Logout
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),

    # Sign-up
    path('signup/', views.signup_view, name='signup'),
]
