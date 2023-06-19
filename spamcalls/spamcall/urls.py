from django.urls import path
from .  import views
urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='user-registration'),
    path('login/',views. UserLoginView.as_view(), name='user-login'),
    path('profile/',views.UserProfileView.as_view(), name='user-profile'),
    path('spam/mark/',views.MarkSpamNumberView.as_view(), name='mark-spam-number'),
    path('search/',views.SearchView.as_view(), name='search'),
]