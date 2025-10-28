import os

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import Part
from .serializers import CSVUploadSerializer, PartSerializer
from .tasks import import_parts_from_csv


class PartViewSet(viewsets.ModelViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(methods=['post'], detail=False, url_path='upload-csv', permission_classes=[IsAdminUser])
    def upload_csv(self, request):
        serializer = CSVUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uploaded_file = serializer.validated_data['file']
        file_path = default_storage.save(
            os.path.join('uploads', uploaded_file.name),
            ContentFile(uploaded_file.read()),
        )
        absolute_path = default_storage.path(file_path)

        task = import_parts_from_csv.delay(absolute_path)

        return Response(
            {
                'message': 'Importação iniciada.',
                'task_id': task.id,
            },
            status=status.HTTP_202_ACCEPTED,
        )