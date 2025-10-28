from decimal import Decimal

import pytest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient

from marketplace.models import Part


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture(autouse=True)
def _enable_celery_eager(settings):
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.CELERY_TASK_EAGER_PROPAGATES = True


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='user',
        password='password123',
    )


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpass123',
    )


@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def admin_client(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.fixture
def part(db):
    return Part.objects.create(
        name='Filtro de Óleo',
        description='Filtro para motor',
        price=Decimal('45.90'),
        quantity=5,
    )


@pytest.fixture
def csv_file():
    content = (
        'Nome,Descricao,Preco,Quantidade\n'
        'Pastilha de Freio,Pastilha dianteira,120.00,8\n'
    ).encode('utf-8')
    return SimpleUploadedFile('pecas.csv', content, content_type='text/csv')


@pytest.fixture
def invalid_csv_file():
    data = b'not-a-valid,csv,content'
    return SimpleUploadedFile('pecas.txt', data, content_type='text/plain')

