import pytest
from django.urls import reverse
from rest_framework import status

from marketplace.models import Part


@pytest.mark.django_db
class TestPartViewSet:
    def test_list_requires_authentication(self, api_client, part):
        url = reverse('part-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_authenticated(self, authenticated_client, part):
        url = reverse('part-list')
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == part.name

    def test_retrieve_authenticated(self, authenticated_client, part):
        url = reverse('part-detail', kwargs={'pk': part.pk})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == part.id

    def test_create_requires_admin(self, authenticated_client):
        url = reverse('part-list')
        payload = {
            'name': 'Pastilha de Freio',
            'description': 'Pastilha dianteira',
            'price': '120.00',
            'quantity': 8,
        }
        response = authenticated_client.post(url, payload, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_as_admin(self, admin_client):
        url = reverse('part-list')
        payload = {
            'name': 'Amortecedor',
            'description': 'Amortecedor dianteiro',
            'price': '350.00',
            'quantity': 4,
        }
        response = admin_client.post(url, payload, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        part = Part.objects.get(name='Amortecedor')
        assert part.quantity == 4

    def test_update_as_admin(self, admin_client, part):
        url = reverse('part-detail', kwargs={'pk': part.pk})
        payload = {'quantity': 12}
        response = admin_client.patch(url, payload, format='json')
        assert response.status_code == status.HTTP_200_OK
        part.refresh_from_db()
        assert part.quantity == 12

    def test_delete_as_admin(self, admin_client, part):
        url = reverse('part-detail', kwargs={'pk': part.pk})
        response = admin_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Part.objects.filter(pk=part.pk).exists()

    def test_upload_csv_requires_admin(self, authenticated_client, csv_file):
        url = reverse('part-upload-csv')
        response = authenticated_client.post(url, {'file': csv_file}, format='multipart')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_upload_csv_as_admin(self, admin_client, csv_file):
        url = reverse('part-upload-csv')
        response = admin_client.post(url, {'file': csv_file}, format='multipart')
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert 'task_id' in response.data
