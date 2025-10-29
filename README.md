# 🛠️ Desafio Backend Django — Marketplace de Autopeças

API RESTful desenvolvida em **Django + Django REST Framework** para gestão de usuários, estoque e compra de autopeças.  
Inclui importação assíncrona de peças via CSV, reposição automática de estoque e autenticação JWT.

## ⚙️ Configuração do Ambiente

### Instalação

```bash
# Clonar
git clone https://github.com/kauerbcs/autopecas_marketplace.git

# Criar venv
python -m venv .venv
source .venv/bin/activate   # Linux/Mac

# Instalar dependências
pip install -r requirements.txt

# Migrar DB
python manage.py migrate

# Criar superuser
python manage.py createsuperuser

# Subir todos conteiner docker
$ docker-compose up -d

# Teste API
http://localhost:8000/api/token/

# Teste pytest
pytest