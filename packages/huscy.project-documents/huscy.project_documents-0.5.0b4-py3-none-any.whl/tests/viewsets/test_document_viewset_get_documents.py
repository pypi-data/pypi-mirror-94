import pytest

from django.contrib.auth.models import Permission
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_405_METHOD_NOT_ALLOWED

from huscy.projects.services import add_member

pytestmark = pytest.mark.django_db


def test_retrieve_documents_is_not_provided(client, document):
    response = retrieve_document(client, document)

    assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED


def test_admin_can_list_documents(admin_client, project):
    response = list_documents(admin_client, project)

    assert response.status_code == HTTP_200_OK


def test_user_with_permission_can_list_documents(client, user, project):
    view_permission = Permission.objects.get(codename='view_project')
    user.user_permissions.add(view_permission)

    response = list_documents(client, project)

    assert response.status_code == HTTP_200_OK


def test_user_without_permission_cannot_list_documents(client, project):
    response = list_documents(client, project)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_anonymous_user_cannot_list_documents(anonymous_client, project):
    response = list_documents(anonymous_client, project)

    assert response.status_code == HTTP_403_FORBIDDEN


@pytest.mark.parametrize('is_coordinator,has_write_permission', [
    (True, False),   # project coordinator
    (False, True),   # member with write permission
    (False, False),  # member with read permission
])
def test_all_project_members_can_list_documents(client, user, project,
                                                is_coordinator, has_write_permission):
    add_member(project, user, is_coordinator, has_write_permission)

    response = list_documents(client, project)

    assert response.status_code == HTTP_200_OK


def list_documents(client, project):
    return client.get(reverse('document-list', kwargs=dict(project_pk=project.pk)))


def retrieve_document(client, document):
    return client.get(
        reverse('document-detail', kwargs=dict(pk=document.pk, project_pk=document.project.pk))
    )
