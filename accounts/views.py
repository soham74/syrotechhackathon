from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.db.models import Avg, Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from reviews.models import Review


def profile_view(request: HttpRequest, username: str) -> HttpResponse:
    User = get_user_model()
    user = get_object_or_404(User, username=username)
    reviews = Review.objects.filter(ratee=user).select_related('rater').order_by('-created_at')
    agg = reviews.aggregate(avg=Avg('rating'), count=Count('id'))
    return render(request, 'accounts/profile.html', {
        'profile_user': user,
        'reviews': reviews[:10],
        'avg_rating': agg['avg'],
        'reviews_count': agg['count'],
    })


def signup_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
from django.shortcuts import render

# Create your views here.
