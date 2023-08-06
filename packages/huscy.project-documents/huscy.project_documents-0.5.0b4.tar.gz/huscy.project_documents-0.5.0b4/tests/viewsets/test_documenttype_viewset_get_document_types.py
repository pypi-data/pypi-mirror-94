import pytest

from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN


def test_admin_user_can_list_document_types(admin_client):
    response = list_document_types(admin_client)

    assert response.status_code == HTTP_200_OK


def test_user_without_permission_can_list_document_types(client):
    response = list_document_types(client)

    assert response.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_anonymous_user_cannot_list_document_types(anonymous_client):
    response = list_document_types(anonymous_client)

    assert response.status_code == HTTP_403_FORBIDDEN


def list_document_types(client):
    return client.get(reverse('documenttype-list'))
