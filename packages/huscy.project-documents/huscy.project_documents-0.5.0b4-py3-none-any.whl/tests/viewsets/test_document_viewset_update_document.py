from rest_framework.reverse import reverse
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED


def test_update_not_allowed(client, document):
    response = client.put(
        reverse('document-detail', kwargs=dict(pk=document.pk, project_pk=document.project.pk)),
        data={}
    )

    assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED
