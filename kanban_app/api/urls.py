from django.urls import path, include
from .views import BoardView, BoardDetailView, FindUserWithEmailView

urlpatterns = [
    path("boards/", BoardView.as_view(), name="board"),
    path("boards/<int:pk>/", BoardDetailView.as_view(), name="board_details"),
    path("email-check/", FindUserWithEmailView.as_view(), name="email_user")
]