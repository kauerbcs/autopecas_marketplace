"""Celery tasks for the marketplace app."""

import csv
from decimal import Decimal
from pathlib import Path

from celery import shared_task
from django.db import transaction

from .models import Part


@shared_task(bind=True, name='marketplace.tasks.import_parts_from_csv')
def import_parts_from_csv(self, file_path: str) -> dict:
    result = {
        'processed': 0,
        'created': 0,
        'updated': 0,
        'errors': [],
    }

    csv_path = Path(file_path)
    if not csv_path.exists():
        raise FileNotFoundError(f'O arquivo {file_path} não foi encontrado.')

    with csv_path.open('r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        expected_columns = {'Nome', 'Descricao', 'Preco', 'Quantidade'}
        if not expected_columns.issubset(set(reader.fieldnames or [])):
            raise ValueError('O arquivo CSV deve conter as colunas Nome, Descricao, Preco e Quantidade.')

        for index, row in enumerate(reader, start=2):
            result['processed'] += 1
            try:
                name = row['Nome'].strip()
                description = (row.get('Descricao') or '').strip()
                price = Decimal(str(row['Preco']).replace(',', '.'))
                quantity = int(row['Quantidade'])

                if price < 0:
                    raise ValueError('Preço deve ser maior ou igual a zero.')
                if quantity < 0:
                    raise ValueError('Quantidade deve ser maior ou igual a zero.')

                with transaction.atomic():
                    part, created = Part.objects.update_or_create(
                        name=name,
                        defaults={
                            'description': description,
                            'price': price,
                            'quantity': quantity,
                        },
                    )

                if created:
                    result['created'] += 1
                else:
                    result['updated'] += 1

            except Exception as exc:  # pylint: disable=broad-except
                result['errors'].append(f'Linha {index}: {exc}')

    return result


@shared_task(name='marketplace.tasks.restock_parts')
def restock_parts(minimum_quantity: int = 10) -> dict:
    parts_to_update = Part.objects.filter(quantity__lt=minimum_quantity)
    updated = parts_to_update.count()
    for part in parts_to_update:
        part.quantity = minimum_quantity
        part.save(update_fields=['quantity', 'updated_at'])

    return {
        'updated_parts': updated,
        'minimum_quantity': minimum_quantity,
    }