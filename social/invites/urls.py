from django.urls import path

from . import views

app_name = "invites"
urlpatterns = [path("send/<str:username>/", views.send_invite, name="send_invite")]
