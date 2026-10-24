# ⚙️ Configuração

## Arquivo `.env`

Crie seu arquivo `.env` na raiz do projeto com as chaves:

```dotenv
TELEGRAM_BOT_TOKEN=seu_token_aqui
TELEGRAM_CHAT_ID=seu_chat_id_aqui
```

> ⚠️ O arquivo `.env` está protegido no `.gitignore` e nunca deve ser compartilhado ou enviado ao GitHub!

## Arquivo `rotas.json`

Configure as rotas de interesse e os tetos em milhas Smiles:

```json
[
  {
    "origem": "RIO",
    "destino": "BHZ",
    "data_ida": "2026-11-15",
    "teto_milhas": 10000
  }
]
```
