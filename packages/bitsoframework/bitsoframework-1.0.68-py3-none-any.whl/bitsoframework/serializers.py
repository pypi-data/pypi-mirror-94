from django.db import IntegrityError
from django.utils import timezone
from django_extensions.db.models import TimeStampedModel
from rest_framework import serializers, fields
from rest_framework.exceptions import ValidationError


class AnyField(fields.Field):

    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        return value


class ListIDSerializer(serializers.Serializer):
    ids = fields.ListField(child=AnyField(required=True))


class UpdateBulkListSerializer(serializers.ListSerializer):

    def update(self, instances, validated_data):

        instance_hash = {index: instance for index, instance in enumerate(instances)}

        result = [
            self.child.update(instance_hash[index], attrs)
            for index, attrs in enumerate(validated_data)
        ]

        writable_fields = [field.field_name for field in self.child._writable_fields]

        if isinstance(instances[0], TimeStampedModel):
            writable_fields.append("modified")
            modified = timezone.now()
            for instance in result:
                instance.modified = modified

        try:
            self.child.Meta.model.objects.bulk_update(result, writable_fields)
        except IntegrityError as e:
            raise ValidationError(e)

        return result
