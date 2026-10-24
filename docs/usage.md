# 🚀 Como Usar

## 1. Testar o envio de alertas
```bash
python3 test_notifier.py
```

## 2. Executar a busca de milhas
```bash
python3 main.py
```

## 3. Automatizar via Cron (Linux)
Para rodar diariamente às 08:00:
```cron
0 8 * * * cd "/caminho/do/projeto" && /caminho/do/projeto/venv/bin/python main.py >> tracker.log 2>&1
```
