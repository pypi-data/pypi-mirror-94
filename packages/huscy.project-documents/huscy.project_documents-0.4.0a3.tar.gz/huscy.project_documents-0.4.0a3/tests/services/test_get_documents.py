from itertools import cycle

import pytest
from model_bakery import baker

from huscy.project_documents.services import get_documents

pytestmark = pytest.mark.django_db


@pytest.fixture
def projects():
    return baker.make('projects.Project', _quantity=3)


@pytest.fixture
def documents(projects):
    return baker.make('project_documents.Document', project=cycle(projects), _quantity=6)


def test_get_documents(documents):
    result = get_documents()

    assert list(result) == documents


def test_get_documents_filtered_by_project(projects, documents):
    result = get_documents(projects[0])

    assert len(result) == 2
    assert list(result) == [documents[0], documents[3]]
