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


def homepage(request: HttpRequest) -> HttpResponse:
    """Homepage view that shows offers at the root URL"""
    offers_qs = _filter_offers(request)
    paginator = Paginator(offers_qs, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    skills = Skill.objects.all()

    if request.headers.get('HX-Request'):
        return render(request, 'directory/partials/_offers_results.html', {
            'page_obj': page_obj,
        })

    return render(request, 'directory/homepage.html', {
        'page_obj': page_obj,
        'skills': skills,
        'filters': {
            'skill': request.GET.get('skill', ''),
            'location': request.GET.get('location', ''),
            'availability': request.GET.get('availability', ''),
        }
    })


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
    offer = get_object_or_404(Offer, pk=pk)
    return render(request, 'directory/offer_detail.html', {'offer': offer})


def request_detail(request: HttpRequest, pk: int) -> HttpResponse:
    request_obj = get_object_or_404(Request, pk=pk)
    return render(request, 'directory/request_detail.html', {'request': request_obj})


@login_required
def offer_create(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        # Handle form submission
        skill_id = request.POST.get('skill')
        title = request.POST.get('title')
        description = request.POST.get('description')
        hour_value = request.POST.get('hour_value')
        availability = request.POST.get('availability')
        location = request.POST.get('location')
        
        if skill_id and title and description:
            skill = get_object_or_404(Skill, id=skill_id)
            offer = Offer.objects.create(
                user=request.user,
                skill=skill,
                title=title,
                description=description,
                hour_value=hour_value or 1.0,
                availability=availability or '',
                location=location or '',
            )
            return redirect(offer.get_absolute_url())
    
    skills = Skill.objects.all()
    return render(request, 'directory/offer_form.html', {'skills': skills})


@login_required
def request_create(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        # Handle form submission
        skill_id = request.POST.get('skill')
        title = request.POST.get('title')
        description = request.POST.get('description')
        hour_value = request.POST.get('hour_value')
        when = request.POST.get('when')
        location = request.POST.get('location')
        
        if skill_id and title and description:
            skill = get_object_or_404(Skill, id=skill_id)
            request_obj = Request.objects.create(
                user=request.user,
                skill=skill,
                title=title,
                description=description,
                hour_value=hour_value or 1.0,
                when=when or '',
                location=location or '',
            )
            return redirect(request_obj.get_absolute_url())
    
    skills = Skill.objects.all()
    return render(request, 'directory/request_form.html', {'skills': skills})


@login_required
def offer_update(request: HttpRequest, pk: int) -> HttpResponse:
    offer = get_object_or_404(Offer, pk=pk, user=request.user)
    
    if request.method == 'POST':
        # Handle form submission
        skill_id = request.POST.get('skill')
        title = request.POST.get('title')
        description = request.POST.get('description')
        hour_value = request.POST.get('hour_value')
        availability = request.POST.get('availability')
        location = request.POST.get('location')
        
        if skill_id and title and description:
            skill = get_object_or_404(Skill, id=skill_id)
            offer.skill = skill
            offer.title = title
            offer.description = description
            offer.hour_value = hour_value or 1.0
            offer.availability = availability or ''
            offer.location = location or ''
            offer.save()
            return redirect(offer.get_absolute_url())
    
    skills = Skill.objects.all()
    return render(request, 'directory/offer_form.html', {'offer': offer, 'skills': skills})


@login_required
def request_update(request: HttpRequest, pk: int) -> HttpResponse:
    request_obj = get_object_or_404(Request, pk=pk, user=request.user)
    
    if request.method == 'POST':
        # Handle form submission
        skill_id = request.POST.get('skill')
        title = request.POST.get('title')
        description = request.POST.get('description')
        hour_value = request.POST.get('hour_value')
        when = request.POST.get('when')
        location = request.POST.get('location')
        
        if skill_id and title and description:
            skill = get_object_or_404(Skill, id=skill_id)
            request_obj.skill = skill
            request_obj.title = title
            request_obj.description = description
            request_obj.hour_value = hour_value or 1.0
            request_obj.when = when or ''
            request_obj.location = location or ''
            request_obj.save()
            return redirect(request_obj.get_absolute_url())
    
    skills = Skill.objects.all()
    return render(request, 'directory/request_form.html', {'request': request_obj, 'skills': skills})


@login_required
def offer_toggle(request: HttpRequest, pk: int) -> HttpResponse:
    offer = get_object_or_404(Offer, pk=pk, user=request.user)
    offer.is_active = not offer.is_active
    offer.save()
    
    if request.headers.get('HX-Request'):
        return render(request, 'directory/partials/_offer_card.html', {'offer': offer})
    
    return redirect('offers-list')


@login_required
def request_toggle(request: HttpRequest, pk: int) -> HttpResponse:
    request_obj = get_object_or_404(Request, pk=pk, user=request.user)
    request_obj.is_active = not request_obj.is_active
    request_obj.save()
    
    if request.headers.get('HX-Request'):
        return render(request, 'directory/partials/_request_card.html', {'request': request_obj})
    
    return redirect('requests-list')


# Temporary view to trigger seeding (remove after use)
def seed_data(request: HttpRequest) -> HttpResponse:
    """Temporary view to seed realistic data - REMOVE AFTER USE"""
    try:
        from scripts.seed_data import run
        run()
        return HttpResponse("✅ Realistic data seeded successfully! Refresh the homepage to see the changes.")
    except Exception as e:
        return HttpResponse(f"❌ Error seeding data: {str(e)}")
