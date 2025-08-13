from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import models
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Transaction


def _compute_balance(user) -> Decimal:
    incoming = Transaction.objects.filter(to_user=user).aggregate(models.Sum('hours'))['hours__sum'] or Decimal('0')
    outgoing = Transaction.objects.filter(from_user=user).aggregate(models.Sum('hours'))['hours__sum'] or Decimal('0')
    return incoming - outgoing


@login_required
def wallet(request: HttpRequest) -> HttpResponse:
    balance = _compute_balance(request.user)
    tx_qs = Transaction.objects.select_related('from_user', 'to_user', 'match').filter(
        models.Q(from_user=request.user) | models.Q(to_user=request.user)
    ).order_by('-created_at')
    paginator = Paginator(tx_qs, 20)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'ledger/wallet.html', {
        'balance': balance,
        'page_obj': page_obj,
    })

from django.shortcuts import render

# Create your views here.
