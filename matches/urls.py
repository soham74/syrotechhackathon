from django.urls import path
from . import views


urlpatterns = [
    path('matches/', views.matches_list, name='matches-list'),
    path('matches/propose', views.propose_match, name='matches-propose'),
    path('matches/<int:pk>/accept', views.match_accept, name='matches-accept'),
    path('matches/<int:pk>/cancel', views.match_cancel, name='matches-cancel'),
    path('matches/<int:pk>/mark-done', views.match_mark_done, name='matches-done'),
]

