import pytest
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.db.models import Sum
from ledger.models import Transaction
from matches.models import Match
from directory.models import Skill, Offer, Request


@pytest.mark.django_db
def test_transaction_updates_balances():
    User = get_user_model()
    alice = User.objects.create_user(username='alice', password='x')
    bob = User.objects.create_user(username='bob', password='x')
    skill = Skill.objects.create(name='Python', slug='python')
    offer = Offer.objects.create(user=bob, skill=skill, title='Teach Python', description='Basics')
    req = Request.objects.create(user=alice, skill=skill, title='Need Python', description='Help', hours_needed=Decimal('1.0'))
    m = Match.objects.create(offer=offer, request=req, requester=alice, provider=bob, agreed_hours=Decimal('1.0'))

    # No transactions initially
    assert Transaction.objects.filter(to_user=alice).count() == 0
    assert Transaction.objects.filter(to_user=bob).count() == 0

    # Alice pays Bob 1.0 hours
    Transaction.objects.create(from_user=alice, to_user=bob, hours=Decimal('1.0'), match=m)

    a_in = Transaction.objects.filter(to_user=alice).aggregate(Sum('hours'))['hours__sum'] or Decimal('0')
    a_out = Transaction.objects.filter(from_user=alice).aggregate(Sum('hours'))['hours__sum'] or Decimal('0')
    b_in = Transaction.objects.filter(to_user=bob).aggregate(Sum('hours'))['hours__sum'] or Decimal('0')
    b_out = Transaction.objects.filter(from_user=bob).aggregate(Sum('hours'))['hours__sum'] or Decimal('0')

    assert (a_in - a_out) == Decimal('-1.0')
    assert (b_in - b_out) == Decimal('1.0')


