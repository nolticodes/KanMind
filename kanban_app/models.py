"""Database models for boards, tasks, and comments."""

from django.db import models
from django.conf import settings

# Create your models here.


class Board(models.Model):
    """Represent a board owned by a user and shared with members."""

    title = models.CharField(max_length=50)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_boards",
    )

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="boards",
    )


class Task(models.Model):
    """Represent a task belonging to a board."""

    STATUS_CHOICES = [
        ("to-do", "To Do"),
        ("in-progress", "In Progress"),
        ("review", "Review"),
        ("done", "Done"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    board = models.ForeignKey(
        Board, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tasks",
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="review_tasks",
    )
    due_date = models.DateField()
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            related_name="owned_tasks")


class Comment(models.Model):
    """Represent a comment written by a user for a task."""

    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    content = models.TextField()
    task = models.ForeignKey(
        Task, 
        on_delete=models.CASCADE,
        related_name="comments"
    )