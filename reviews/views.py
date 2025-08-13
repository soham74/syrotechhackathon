from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from matches.models import Match
from .models import Review
from .forms import ReviewForm
from accounts.models import User


def _is_participant(user, match: Match) -> bool:
    return user.is_authenticated and (user == match.requester or user == match.provider)


@login_required
def pending_reviews(request: HttpRequest) -> HttpResponse:
    # Matches done, involving the user, where the user has not yet reviewed the other
    done_matches = Match.objects.filter(status=Match.STATUS_DONE).filter(
        models.Q(requester=request.user) | models.Q(provider=request.user)
    )
    reviewed_match_ids = Review.objects.filter(rater=request.user).values_list('match_id', flat=True)
    pending = done_matches.exclude(id__in=reviewed_match_ids).select_related('requester', 'provider')
    return render(request, 'reviews/pending.html', {'matches': pending})


@login_required
def create_review(request: HttpRequest, match_id: int) -> HttpResponse:
    match = get_object_or_404(Match.objects.select_related('requester', 'provider'), pk=match_id)
    if not _is_participant(request.user, match):
        return HttpResponseForbidden()
    if match.status != Match.STATUS_DONE:
        messages.error(request, 'You can only review completed matches.')
        return redirect('reviews-pending')

    ratee = match.provider if request.user == match.requester else match.requester

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.match = match
            review.rater = request.user
            review.ratee = ratee
            review.save()
            _update_reputation_for_review(review)
            messages.success(request, 'Review submitted.')
            return redirect('reviews-pending')
    else:
        form = ReviewForm()
    return render(request, 'reviews/review_form.html', {'form': form, 'match': match, 'ratee': ratee})


def _update_reputation_for_review(review: Review) -> None:
    # Increase reputation by (rating - 3), clamped between [-2, +2]
    delta = max(-2, min(2, review.rating - 3))
    ratee: User = review.ratee
    ratee.reputation_score = (ratee.reputation_score or 0) + delta
    ratee.save(update_fields=['reputation_score'])

from django.shortcuts import render

# Create your views here.
