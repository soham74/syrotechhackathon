from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('seed/', views.seed_data, name='seed-data'),  # Temporary - remove after use
    path('skills/', views.SkillListView.as_view(), name='skills-list'),
    path('skills/<slug:slug>/', views.SkillDetailView.as_view(), name='skills-detail'),

    path('offers/', views.offer_list, name='offers-list'),
    path('offers/new/', views.offer_create, name='offers-create'),
    path('offers/<int:pk>/', views.offer_detail, name='offers-detail'),
    path('offers/<int:pk>/edit/', views.offer_update, name='offers-update'),
    path('offers/<int:pk>/toggle/', views.offer_toggle, name='offers-toggle'),

    path('requests/', views.request_list, name='requests-list'),
    path('requests/new/', views.request_create, name='requests-create'),
    path('requests/<int:pk>/', views.request_detail, name='requests-detail'),
    path('requests/<int:pk>/edit/', views.request_update, name='requests-update'),
    path('requests/<int:pk>/toggle/', views.request_toggle, name='requests-toggle'),
]


