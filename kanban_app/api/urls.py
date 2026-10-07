from django.urls import path, include
from .views import BoardView, BoardDetailView

urlpatterns = [
    path("boards/", BoardView.as_view(), name="board"),
    path("boards/<int:board_id>/", BoardDetailView.as_view(), name="board_details")
]