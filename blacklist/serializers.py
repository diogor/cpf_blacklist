from rest_framework.serializers import ModelSerializer
from .models import ListEntry


class ListEntrySerializer(ModelSerializer):
    class Meta:
        model = ListEntry
        exclude = ()
