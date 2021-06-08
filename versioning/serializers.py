from django.contrib.auth.models import User
from rest_framework import serializers


class RevisionField(serializers.RelatedField):
    def to_representation(self, value):
        return value.revision_url


class DocumentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    url = serializers.CharField(allow_blank=False)
    revisions = RevisionField(read_only=True, many=True)
    file = serializers.FileField(write_only=True)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')
