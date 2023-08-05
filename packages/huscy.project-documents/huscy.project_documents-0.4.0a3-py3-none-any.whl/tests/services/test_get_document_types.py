from itertools import cycle

import pytest
from model_bakery import baker

from huscy.project_documents.services import get_document_types

pytestmark = pytest.mark.django_db


def test_get_document_types():
    baker.make('project_documents.DocumentType', name=cycle(['B', 'D', 'A', 'C']), _quantity=4)

    result = get_document_types()

    assert list(result.values_list('name', flat=True)) == ['A', 'B', 'C', 'D']
