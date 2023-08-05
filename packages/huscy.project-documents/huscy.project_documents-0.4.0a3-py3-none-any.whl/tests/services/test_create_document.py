from datetime import datetime

import pytest

from django.core.files import File

from huscy.project_documents.services import create_document


@pytest.mark.freeze_time('2020-01-01 10:00:00')
def test_create_document(user, project, tmp_file, document_type):
    with open(tmp_file, 'r') as fh:
        filehandle = File(fh)
        result = create_document(project, filehandle, document_type, user)

    assert result.project == project
    assert result.document_type == document_type
    assert result.filename == 'tmp.txt'
    assert result.uploaded_at == datetime(2020, 1, 1, 10)
    assert result.uploaded_by == user
