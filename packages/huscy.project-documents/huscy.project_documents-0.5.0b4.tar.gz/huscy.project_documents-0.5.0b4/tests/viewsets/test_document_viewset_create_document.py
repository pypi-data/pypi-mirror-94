import pytest

from django.contrib.auth.models import Permission
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN

from huscy.projects.services import add_member

pytestmark = pytest.mark.django_db


def test_admin_user_can_create_documents(admin_client, project, tmp_file, document_type):
    response = upload_document(admin_client, project, tmp_file, document_type)

    assert response.status_code == HTTP_201_CREATED


def test_user_with_change_project_permission_can_create_documents(client, user, project,
                                                                  tmp_file, document_type):
    change_permission = Permission.objects.get(codename='change_project')
    user.user_permissions.add(change_permission)

    response = upload_document(client, project, tmp_file, document_type)

    assert response.status_code == HTTP_201_CREATED


def test_user_without_permission_cannot_create_documents(client, project, tmp_file, document_type):
    response = upload_document(client, project, tmp_file, document_type)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_anonymous_user_cannot_create_documents(anonymous_client, project, tmp_file, document_type):
    response = upload_document(anonymous_client, project, tmp_file, document_type)

    assert response.status_code == HTTP_403_FORBIDDEN


@pytest.mark.parametrize('is_coordinator,has_write_permission,expected_status_code', [
    (True, False, HTTP_201_CREATED),     # project coordinator
    (False, True, HTTP_201_CREATED),     # member with write permission
    (False, False, HTTP_403_FORBIDDEN),  # member with read permission
])
def test_project_member_creates_document(client, user, project, tmp_file, document_type,
                                         is_coordinator, has_write_permission,
                                         expected_status_code):
    add_member(project, user, is_coordinator, has_write_permission)

    response = upload_document(client, project, tmp_file, document_type)

    assert response.status_code == expected_status_code


def upload_document(client, project, tmp_file, document_type):
    with open(tmp_file, 'r') as f:
        data = dict(project=project.id, filehandle=f, document_type=document_type.id)
        return client.post(reverse('document-list', kwargs=dict(project_pk=project.pk)), data=data)
