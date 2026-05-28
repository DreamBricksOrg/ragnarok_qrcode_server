# Ragnarok API

API simples de resgate de cupons com Flask e MongoDB.

Cada cupom tem:

```json
{
  "id": "6f2f0139-eed8-4da8-ae78-9674e10b3f5e",
  "code": "PROMO123",
  "valid": "valid"
}
```

No MongoDB o campo `id` do CSV vira `_id`.

## Como rodar

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
docker compose up -d
```

API em `http://127.0.0.1:5000`.

## Variaveis de ambiente

```env
API_KEY=change-me-api-key
BASE_URL=http://127.0.0.1:5000
MONGO_URI=mongodb://dbprojeto:3177@mongodb:27017/ragnarok?authSource=admin
```

## CSV

Formato esperado:

```csv
id,code,valid
6f2f0139-eed8-4da8-ae78-9674e10b3f5e,PROMO123,valid
fc71ceef-7665-4981-a983-35d58819ced2,PROMO456,notvalid
```

Se `id` vier vazio, a API gera um UUID automaticamente. Se vier preenchido, precisa ser um UUID valido. O campo `valid` aceita apenas `valid` ou `notvalid`.

## Rotas

```http
GET /health/
```

Valida se a API responde e se o MongoDB aceita `ping`.

```http
GET /api/genragcode
api-key: change-me-api-key
```

Busca um cupom com `valid = valid` e retorna:

```json
{
  "url": "http://127.0.0.1:5001/pages/6f2f0139-eed8-4da8-ae78-9674e10b3f5e"
}
```

```http
POST /api/import/codes
api-key: change-me-api-key
Content-Type: multipart/form-data
```

Campo do arquivo: `csv`.

Retorno:

```json
{
  "status": "success",
  "inserted": 2
}
```

```http
GET /pages/6f2f0139-eed8-4da8-ae78-9674e10b3f5e
```

Abre uma pagina simples que chama `GET /api/6f2f0139-eed8-4da8-ae78-9674e10b3f5e`.

```http
GET /pages/demo
```

Abre uma pagina de demonstracao com botao `INICIAR`, chama `GET /api/genragcode` e gera um QR code com o link de resgate. Esta rota funciona apenas com `FLASK_ENV=development` se `FLASK_ENV=production`, não funciona.

```http
GET /api/6f2f0139-eed8-4da8-ae78-9674e10b3f5e
```

No primeiro acesso, retorna o cupom e marca como `notvalid`:

```json
{
  "status": "success",
  "code": "PROMO123"
}
```

No segundo acesso:

```json
{
  "status": "failed",
  "message": "already used"
}
```
