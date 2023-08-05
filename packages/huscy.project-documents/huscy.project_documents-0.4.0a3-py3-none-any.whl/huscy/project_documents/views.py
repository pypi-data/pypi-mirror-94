from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated

from huscy.projects.models import Project
from huscy.project_documents import serializer, services


class DocumentViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = serializer.DocumentSerializer

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.project = get_object_or_404(Project, pk=self.kwargs['project_pk'])

    def get_queryset(self):
        return services.get_documents(self.project)


class DocumentTypeViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    permission_classes = (DjangoModelPermissions, )
    queryset = services.get_document_types()
    serializer_class = serializer.DocumentTypeSerializer
