import pytest

from django.contrib.auth.models import Permission
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN

from huscy.projects.services import add_member


def test_admin_user_can_delete_documents(admin_client, document):
    response = delete_document(admin_client, document)

    assert response.status_code == HTTP_204_NO_CONTENT


def test_user_with_change_project_permission_can_delete_documents(client, user, document):
    change_permission = Permission.objects.get(codename='change_project')
    user.user_permissions.add(change_permission)

    response = delete_document(client, document)

    assert response.status_code == HTTP_204_NO_CONTENT


def test_user_without_permission_cannot_delete_documents(client, document):
    response = delete_document(client, document)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_anonymous_user_cannot_delete_documents(anonymous_client, document):
    response = delete_document(anonymous_client, document)

    assert response.status_code == HTTP_403_FORBIDDEN


@pytest.mark.parametrize('is_coordinator,has_write_permission,expected_status_code', [
    (True, False, HTTP_204_NO_CONTENT),  # project coordinator
    (False, True, HTTP_204_NO_CONTENT),  # member with write permission
    (False, False, HTTP_403_FORBIDDEN),  # member with read permission
])
def test_project_member_deletes_document(client, user, document, is_coordinator,
                                         has_write_permission, expected_status_code):
    add_member(document.project, user, is_coordinator, has_write_permission)

    response = delete_document(client, document)

    assert response.status_code == expected_status_code


def delete_document(client, document):
    return client.delete(
        reverse('document-detail', kwargs=dict(pk=document.pk, project_pk=document.project.pk))
    )
