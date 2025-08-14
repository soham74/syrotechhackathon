import pytest
from directory.forms import OfferForm, RequestForm


def test_offer_form_required_fields():
    form = OfferForm(data={})
    assert not form.is_valid()
    assert 'title' in form.errors
    assert 'description' in form.errors


def test_request_form_required_fields():
    form = RequestForm(data={})
    assert not form.is_valid()
    assert 'title' in form.errors
    assert 'description' in form.errors


