import pytest
from model_bakery import baker

pytestmark = pytest.mark.django_db


def test_str_method():
    document_type = baker.make('project_documents.DocumentType', name='the document type')

    assert 'the document type' == str(document_type)
