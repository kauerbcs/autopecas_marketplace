from rest_framework import serializers

from .models import Part


class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = [
            'id',
            'name',
            'description',
            'price',
            'quantity',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ('id', 'created_at', 'updated_at')


class CSVUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError('O arquivo deve ser um CSV.')
        return value