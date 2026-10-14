from django.urls import path, include
from .views import (
    BoardView, 
    BoardDetailView, 
    FindUserWithEmailView, 
    CreateTaskInBoardView,
    TaskDetailView,
    CommentsListView,
    CommentIDView,
    AssigneeView,
    ReviewerView
    )

urlpatterns = [
    path("boards/", BoardView.as_view(), name="board"),
    path("boards/<int:pk>/", BoardDetailView.as_view(), name="board-details"),
    path("email-check/", FindUserWithEmailView.as_view(), name="email-user"),
    path("tasks/", CreateTaskInBoardView.as_view(), name="create-task"),
    path("tasks/assigned-to-me/", AssigneeView.as_view(), name="assigned-to-me-task"),
    path("tasks/reviewing/", ReviewerView.as_view(), name="reviewer-is-me-task"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="patch-delete-task"),
    path("tasks/<int:task_id>/comments/", CommentsListView.as_view(), name="task-comments"),
    path("tasks/<int:task_id>/comments/<int:comment_id>/", CommentIDView.as_view(), name="comment-id"),
]