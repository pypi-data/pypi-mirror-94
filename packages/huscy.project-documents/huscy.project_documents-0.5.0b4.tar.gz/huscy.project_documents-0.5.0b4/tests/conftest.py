import pytest
from model_bakery import baker

from rest_framework.test import APIClient


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(username='user', password='password',
                                                 first_name='Ali', last_name='Mente')


@pytest.fixture
def admin_client(admin_user):
    client = APIClient()
    client.login(username=admin_user.username, password='password')
    return client


@pytest.fixture
def client(user):
    client = APIClient()
    client.login(username=user.username, password='password')
    return client


@pytest.fixture
def anonymous_client():
    return APIClient()


@pytest.fixture
def project():
    return baker.make('projects.Project')


@pytest.fixture
def document_type():
    return baker.make('project_documents.DocumentType')


@pytest.fixture
def document(user, document_type):
    return baker.make('project_documents.Document', document_type=document_type, uploaded_by=user)


@pytest.fixture
def tmp_file(tmp_path):
    _file = tmp_path / 'tmp.txt'
    _file.write_text('foo bar')
    return _file
