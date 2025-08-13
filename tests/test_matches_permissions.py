import pytest
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import Client
from matches.models import Match
from directory.models import Skill, Offer, Request


@pytest.mark.django_db
def test_only_participants_can_accept_cancel(client: Client):
    User = get_user_model()
    a = User.objects.create_user(username='a', password='x')
    b = User.objects.create_user(username='b', password='x')
    other = User.objects.create_user(username='c', password='x')
    skill = Skill.objects.create(name='Yoga', slug='yoga')
    offer = Offer.objects.create(user=b, skill=skill, title='Teach Yoga', description='Basics')
    req = Request.objects.create(user=a, skill=skill, title='Need Yoga', description='Help', hours_needed=Decimal('1.0'))
    m = Match.objects.create(offer=offer, request=req, requester=a, provider=b, agreed_hours=Decimal('1.0'))

    client.login(username='c', password='x')
    resp = client.post(f'/matches/{m.id}/accept')
    assert resp.status_code in (302, 403)

    client.logout()
    client.login(username='a', password='x')
    resp2 = client.post(f'/matches/{m.id}/accept')
    assert resp2.status_code in (200, 302)

