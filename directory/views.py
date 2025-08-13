from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView

from .models import Skill, Offer, Request
from .forms import OfferForm, RequestForm


class SkillListView(ListView):
    model = Skill
    template_name = 'directory/skills_list.html'
    context_object_name = 'skills'


class SkillDetailView(DetailView):
    model = Skill
    template_name = 'directory/skills_detail.html'
    context_object_name = 'skill'


def _filter_offers(request: HttpRequest):
    qs = Offer.objects.select_related('user', 'skill').filter(is_active=True)
    skill = request.GET.get('skill')
    location = request.GET.get('location')
    availability = request.GET.get('availability')
    if skill:
        qs = qs.filter(skill__id=skill)
    if location:
        qs = qs.filter(location__icontains=location)
    if availability:
        qs = qs.filter(availability__icontains=availability)
    return qs


def _filter_requests(request: HttpRequest):
    qs = Request.objects.select_related('user', 'skill').filter(is_active=True)
    skill = request.GET.get('skill')
    location = request.GET.get('location')
    when = request.GET.get('when')
    if skill:
        qs = qs.filter(skill__id=skill)
    if location:
        qs = qs.filter(location__icontains=location)
    if when:
        qs = qs.filter(when__icontains=when)
    return qs


def offer_list(request: HttpRequest) -> HttpResponse:
    offers_qs = _filter_offers(request)
    paginator = Paginator(offers_qs, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    skills = Skill.objects.all()

    if request.headers.get('HX-Request'):
        return render(request, 'directory/partials/_offers_results.html', {
            'page_obj': page_obj,
        })

    return render(request, 'directory/offers_list.html', {
        'page_obj': page_obj,
        'skills': skills,
        'filters': {
            'skill': request.GET.get('skill', ''),
            'location': request.GET.get('location', ''),
            'availability': request.GET.get('availability', ''),
        }
    })


def request_list(request: HttpRequest) -> HttpResponse:
    requests_qs = _filter_requests(request)
    paginator = Paginator(requests_qs, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    skills = Skill.objects.all()

    if request.headers.get('HX-Request'):
        return render(request, 'directory/partials/_requests_results.html', {
            'page_obj': page_obj,
        })

    return render(request, 'directory/requests_list.html', {
        'page_obj': page_obj,
        'skills': skills,
        'filters': {
            'skill': request.GET.get('skill', ''),
            'location': request.GET.get('location', ''),
            'when': request.GET.get('when', ''),
        }
    })


def offer_detail(request: HttpRequest, pk: int) -> HttpResponse:
    offer = get_object_or_404(Offer.objects.select_related('user', 'skill'), pk=pk)
    return render(request, 'directory/offer_detail.html', {'offer': offer})


def request_detail(request: HttpRequest, pk: int) -> HttpResponse:
    req = get_object_or_404(Request.objects.select_related('user', 'skill'), pk=pk)
    return render(request, 'directory/request_detail.html', {'request_obj': req})


@login_required
def offer_create(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.user = request.user
            offer.save()
            return redirect(offer.get_absolute_url())
    else:
        form = OfferForm()
    return render(request, 'directory/offer_form.html', {'form': form})


@login_required
def offer_update(request: HttpRequest, pk: int) -> HttpResponse:
    offer = get_object_or_404(Offer, pk=pk, user=request.user)
    if request.method == 'POST':
        form = OfferForm(request.POST, instance=offer)
        if form.is_valid():
            form.save()
            if request.headers.get('HX-Request'):
                return render(request, 'directory/partials/_offer_card.html', {'offer': offer})
            return redirect(offer.get_absolute_url())
    else:
        form = OfferForm(instance=offer)
    return render(request, 'directory/offer_form.html', {'form': form, 'offer': offer})


@login_required
def offer_toggle(request: HttpRequest, pk: int) -> HttpResponse:
    offer = get_object_or_404(Offer, pk=pk, user=request.user)
    offer.is_active = not offer.is_active
    offer.save(update_fields=['is_active'])
    if request.headers.get('HX-Request'):
        return render(request, 'directory/partials/_offer_card.html', {'offer': offer})
    return redirect('offers-list')


@login_required
def request_create(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            req = form.save(commit=False)
            req.user = request.user
            req.save()
            return redirect(req.get_absolute_url())
    else:
        form = RequestForm()
    return render(request, 'directory/request_form.html', {'form': form})


@login_required
def request_update(request: HttpRequest, pk: int) -> HttpResponse:
    req = get_object_or_404(Request, pk=pk, user=request.user)
    if request.method == 'POST':
        form = RequestForm(request.POST, instance=req)
        if form.is_valid():
            form.save()
            if request.headers.get('HX-Request'):
                return render(request, 'directory/partials/_request_card.html', {'request_obj': req})
            return redirect(req.get_absolute_url())
    else:
        form = RequestForm(instance=req)
    return render(request, 'directory/request_form.html', {'form': form, 'request_obj': req})


@login_required
def request_toggle(request: HttpRequest, pk: int) -> HttpResponse:
    req = get_object_or_404(Request, pk=pk, user=request.user)
    req.is_active = not req.is_active
    req.save(update_fields=['is_active'])
    if request.headers.get('HX-Request'):
        return render(request, 'directory/partials/_request_card.html', {'request_obj': req})
    return redirect('requests-list')

from django.shortcuts import render

# Create your views here.
