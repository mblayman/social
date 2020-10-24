from django.urls import path

from social.users import views

app_name = "users"
urlpatterns = [path("<str:username>/", views.UserDetailView.as_view(), name="detail")]
