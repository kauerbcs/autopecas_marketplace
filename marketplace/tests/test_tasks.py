from decimal import Decimal

import pytest

from marketplace.models import Part
from marketplace.tasks import import_parts_from_csv, restock_parts


@pytest.mark.django_db
def test_restock_parts_updates_low_inventory(part):
    assert part.quantity == 5
    result = restock_parts()
    part.refresh_from_db()
    assert part.quantity == 10
    assert result['updated_parts'] == 1


@pytest.mark.django_db
def test_restock_parts_skip_high_inventory(db):
    Part.objects.create(
        name='Bateria',
        description='Bateria 60Ah',
        price=Decimal('450.00'),
        quantity=12,
    )
    result = restock_parts()
    assert result['updated_parts'] == 0


@pytest.mark.django_db
def test_import_parts_from_csv_creates_records(tmp_path):
    csv_content = (
        'Nome,Descricao,Preco,Quantidade\n'
        'Radiador,Radiador de alumínio,380.00,7\n'
    )
    csv_path = tmp_path / 'pecas.csv'
    csv_path.write_text(csv_content, encoding='utf-8')

    result = import_parts_from_csv(str(csv_path))
    assert result['processed'] == 1
    assert result['created'] == 1
    assert Part.objects.filter(name='Radiador').exists()


@pytest.mark.django_db
def test_import_parts_from_csv_updates_existing(part, tmp_path):
    csv_content = (
        'Nome,Descricao,Preco,Quantidade\n'
        f"{part.name},Filtro atualizado,99.50,12\n"
    )
    csv_path = tmp_path / 'pecas.csv'
    csv_path.write_text(csv_content, encoding='utf-8')

    result = import_parts_from_csv(str(csv_path))
    part.refresh_from_db()
    assert result['updated'] == 1
    assert part.description == 'Filtro atualizado'
    assert part.price == Decimal('99.50')
    assert part.quantity == 12
