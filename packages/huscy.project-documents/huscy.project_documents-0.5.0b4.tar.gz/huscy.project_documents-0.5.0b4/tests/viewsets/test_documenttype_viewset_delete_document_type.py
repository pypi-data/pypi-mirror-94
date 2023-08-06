import pytest

from django.contrib.auth.models import Permission
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN


def test_admin_user_can_delete_document_types(admin_client, document_type):
    response = delete_document_type(admin_client, document_type)

    assert response.status_code == HTTP_204_NO_CONTENT


def test_user_with_permission_can_delete_document_types(client, user, document_type):
    delete_permission = Permission.objects.get(codename='delete_documenttype')
    user.user_permissions.add(delete_permission)

    response = delete_document_type(client, document_type)

    assert response.status_code == HTTP_204_NO_CONTENT


def test_user_without_permission_cannot_delete_document_types(client, document_type):
    response = delete_document_type(client, document_type)

    assert response.status_code == HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_anonymous_user_cannot_delete_document_types(anonymous_client, document_type):
    response = delete_document_type(anonymous_client, document_type)

    assert response.status_code == HTTP_403_FORBIDDEN


def delete_document_type(client, document_type):
    return client.delete(reverse('documenttype-detail', kwargs=dict(pk=document_type.pk)))
