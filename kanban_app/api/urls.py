from django.urls import path, include
from .views import (
    BoardView, 
    BoardDetailView, 
    FindUserWithEmailView, 
    CreateTaskInBoardView,
    TaskDetailView,
    CommentsListView,
    )

urlpatterns = [
    path("boards/", BoardView.as_view(), name="board"),
    path("boards/<int:pk>/", BoardDetailView.as_view(), name="board-details"),
    path("email-check/", FindUserWithEmailView.as_view(), name="email-user"),
    path("tasks/", CreateTaskInBoardView.as_view(), name="create-task"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="patch-delete-task"),
    path("tasks/<int:pk>/comments/", CommentsListView.as_view(), name="task-comments"),
]