from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db import models
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from directory.models import Offer, Request
from .models import Match


def _is_participant(user, match: Match) -> bool:
    return user.is_authenticated and (user == match.requester or user == match.provider)


@login_required
def matches_list(request: HttpRequest) -> HttpResponse:
    qs = Match.objects.select_related('requester', 'provider', 'offer', 'request').filter(
        # participant only
    ).filter(models.Q(requester=request.user) | models.Q(provider=request.user)).order_by('-created_at')
    return render(request, 'matches/matches_list.html', {'matches': qs})


@login_required
def propose_match(request: HttpRequest) -> HttpResponse:
    offer_id = request.GET.get('offer')
    request_id = request.GET.get('request')
    scheduled_at = request.POST.get('scheduled_at') if request.method == 'POST' else None
    hours = request.POST.get('hours') if request.method == 'POST' else None

    offer = Offer.objects.filter(pk=offer_id).first() if offer_id else None
    req = Request.objects.filter(pk=request_id).first() if request_id else None

    if request.method == 'POST':
        if not (offer or req):
            messages.error(request, 'Select an offer or request to propose a match.')
            return redirect('matches-list')

        # Determine requester/provider from context
        if offer and not req:
            requester = request.user if request.user != offer.user else offer.user
            provider = offer.user
        elif req and not offer:
            requester = request.user
            provider = req.user
        else:
            requester = request.user
            provider = offer.user if offer else req.user

        match = Match.objects.create(
            offer=offer,
            request=req,
            requester=requester,
            provider=provider,
            agreed_hours=Decimal(hours or '1.0'),
            scheduled_at=scheduled_at or None,
        )
        messages.success(request, 'Match proposed.')
        return redirect('matches-list')

    return render(request, 'matches/propose_form.html', {
        'offer': offer,
        'req': req,
    })


@login_required
def match_accept(request: HttpRequest, pk: int) -> HttpResponse:
    match = get_object_or_404(Match, pk=pk)
    if not _is_participant(request.user, match):
        return HttpResponseForbidden()
    match.status = Match.STATUS_ACCEPTED
    match.save(update_fields=['status'])
    template = 'matches/partials/_match_row.html'
    return render(request, template, {'m': match})


@login_required
def match_cancel(request: HttpRequest, pk: int) -> HttpResponse:
    match = get_object_or_404(Match, pk=pk)
    if not _is_participant(request.user, match):
        return HttpResponseForbidden()
    match.status = Match.STATUS_CANCELLED
    match.save(update_fields=['status'])
    template = 'matches/partials/_match_row.html'
    return render(request, template, {'m': match})


@login_required
def match_mark_done(request: HttpRequest, pk: int) -> HttpResponse:
    match = get_object_or_404(Match.objects.select_related('requester', 'provider'), pk=pk)
    if not _is_participant(request.user, match):
        return HttpResponseForbidden()
    if match.status != Match.STATUS_ACCEPTED:
        messages.error(request, 'Match must be accepted to mark done.')
        return redirect('matches-list')

    from ledger.models import Transaction

    with transaction.atomic():
        # Simple overdraft rule: recipient must have enough to pay provider
        recipient = match.requester  # requester receives service, pays provider
        provider = match.provider
        hours = match.agreed_hours

        # compute balance
        incoming = Transaction.objects.filter(to_user=recipient).aggregate(models.Sum('hours'))['hours__sum'] or Decimal('0')
        outgoing = Transaction.objects.filter(from_user=recipient).aggregate(models.Sum('hours'))['hours__sum'] or Decimal('0')
        balance = incoming - outgoing
        if balance - hours < 0:
            messages.error(request, 'Insufficient credits to complete this match.')
            return redirect('matches-list')

        Transaction.objects.create(from_user=recipient, to_user=provider, hours=hours, match=match)
        match.status = Match.STATUS_DONE
        match.save(update_fields=['status'])

    template = 'matches/partials/_match_row.html'
    return render(request, template, {'m': match})

from django.shortcuts import render

# Create your views here.
