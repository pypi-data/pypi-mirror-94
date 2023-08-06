import pytest

from django.contrib.auth.models import Permission
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN


def test_admin_user_can_create_document_types(admin_client):
    response = create_document_type(admin_client)

    assert response.status_code == HTTP_201_CREATED


def test_user_with_permission_can_create_document_types(client, user):
    create_permission = Permission.objects.get(codename='add_documenttype')
    user.user_permissions.add(create_permission)

    response = create_document_type(client)

    assert response.status_code == HTTP_201_CREATED


def test_user_without_permission_cannot_create_document_types(client):
    response = create_document_type(client)

    assert response.status_code == HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_anonymous_user_cannot_create_document_types(anonymous_client):
    response = create_document_type(anonymous_client)

    assert response.status_code == HTTP_403_FORBIDDEN


def create_document_type(client):
    return client.post(reverse('documenttype-list'), data=dict(name='Questionaire'))
