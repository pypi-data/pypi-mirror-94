import pytest

from rest_framework.reverse import reverse
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN


def test_admin_user_can_delete_documents(admin_client, document):
    response = delete_document(admin_client, document)

    assert response.status_code == HTTP_204_NO_CONTENT


def test_user_without_permission_can_delete_documents(client, document):
    response = delete_document(client, document)

    assert response.status_code == HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_anonymous_user_cannot_delete_documents(anonymous_client, document):
    response = delete_document(anonymous_client, document)

    assert response.status_code == HTTP_403_FORBIDDEN


def delete_document(client, document):
    return client.delete(
        reverse('document-detail', kwargs=dict(pk=document.pk, project_pk=document.project.pk))
    )
