from django.urls import path, include
from .views import BoardView

urlpatterns = [
    path("boards/", BoardView.as_view(), name="board"),
]