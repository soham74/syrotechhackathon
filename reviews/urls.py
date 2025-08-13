from django.urls import path
from . import views


urlpatterns = [
    path('reviews/pending', views.pending_reviews, name='reviews-pending'),
    path('reviews/<int:match_id>/new', views.create_review, name='reviews-create'),
]

