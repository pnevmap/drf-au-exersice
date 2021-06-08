import os

from django.contrib.auth.models import User
from django.db import transaction
from django.http import FileResponse, HttpResponseNotFound, Http404
from rest_framework import permissions, renderers, viewsets, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from versioning.models import Document, Revision
from versioning.permissions import IsOwner
from versioning.serializers import DocumentSerializer,  UserSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsOwner)
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    lookup_field = 'url'

    def perform_create(self, serializer):
        with transaction.atomic():
            document = Document.objects.create(url=self.request.data['url'], owner=self.request.user)
            revision = Revision.objects.create(document=document, file=self.request.data['file'])
            document.revisions.add(revision)
        return Response({'url': document.url, 'file': revision.url})

    def list(self, request, *args, **kwargs):

        data = self.queryset.filter(owner=request.user)
        url = kwargs.get("url")
        if url:
            data = data.filter(url=kwargs["url"])

        serializer = DocumentSerializer(data, many=True,
                                        context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        document = self.get_object()
        revision_index = request.GET.get("revision")
        some_file = None
        revision = document.revisions.filter(index=revision_index).first()
        if revision_index and revision is not None:
            some_file = revision.file
        elif revision_index and revision is None:
            raise Http404
        else:
            some_file = document.revisions.last().file
        if not some_file:
            raise Http404
        response = FileResponse(some_file)
        # https://docs.djangoproject.com/en/1.11/howto/outputting-csv/#streaming-large-csv-files
        # filename = os.path.basename(some_file.file.name)
        # response['Content-Disposition'] = 'attachment; filename="%s"' % filename
        return response

    def update(self, request, *args, **kwargs):
        url = kwargs.get('url')
        if url is None:
            url = request.data.get("url")
        if url is None:
            raise Http404

        revision = Revision.objects.create(document=self.queryset.filter(url=url).first(), file=request.data['file'])
        # serializer = self.get_serializer()
        # serializer = DocumentSerializer( data={'url': url, 'file': request.data['file']}, context={'request': request})
        return Response({'url': url, 'file': revision.url})


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer


class WhoamIViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        serializer = UserSerializer(self.queryset.filter(username=request.user.username).get(),context={'request': request})
        return Response(serializer.data)
