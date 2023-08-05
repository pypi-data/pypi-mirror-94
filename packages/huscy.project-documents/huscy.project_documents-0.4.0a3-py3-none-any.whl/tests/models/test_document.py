def test_delete_user(django_user_model, user, document):
    assert document.uploaded_by == user

    django_user_model.objects.filter(username=user.username).delete()

    document.refresh_from_db()

    assert document.uploaded_by is None
