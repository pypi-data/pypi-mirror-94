import pytest

from rest_framework.reverse import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN


def test_admin_user_can_create_documents(admin_client, project, tmp_file, document_type):
    response = upload_document(admin_client, project, tmp_file, document_type)

    assert response.status_code == HTTP_201_CREATED, response.json()


def test_user_without_permission_can_create_documents(client, project, tmp_file, document_type):
    response = upload_document(client, project, tmp_file, document_type)

    assert response.status_code == HTTP_201_CREATED, response.json()


@pytest.mark.django_db
def test_anonymous_user_cannot_create_documents(anonymous_client, project, tmp_file, document_type):
    response = upload_document(anonymous_client, project, tmp_file, document_type)

    assert response.status_code == HTTP_403_FORBIDDEN


def upload_document(client, project, tmp_file, document_type):
    with open(tmp_file, 'r') as f:
        data = dict(project=project.id, filehandle=f, document_type=document_type.id)
        return client.post(reverse('document-list', kwargs=dict(project_pk=project.pk)), data=data)
