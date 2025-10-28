import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_obtain_token(api_client, user):
    url = reverse('token_obtain_pair')
    payload = {'username': 'user', 'password': 'password123'}
    response = api_client.post(url, payload, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data


@pytest.mark.django_db
def test_protected_endpoint_requires_token(api_client, part):
    url = reverse('part-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_protected_endpoint_with_token(api_client, user, part):
    token_url = reverse('token_obtain_pair')
    payload = {'username': 'user', 'password': 'password123'}
    token_response = api_client.post(token_url, payload, format='json')
    access_token = token_response.data['access']

    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    url = reverse('part-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
