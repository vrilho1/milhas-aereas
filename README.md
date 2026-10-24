# ✈️ Monitor de Milhas Smiles

Automação diária desenvolvida em Python para rastrear oportunidades e promoções em milhas na **Smiles (GOL)** com foco em saídas do **Rio de Janeiro** e **Belo Horizonte** para destinos nacionais e América do Sul.

---

## 📁 Estrutura do Projeto

- [rotas.json](file:///home/edbrilhante/Área de Trabalho/Programação/Mlhas aéreas/rotas.json): Onde você configura suas rotas favoritas, origens, destinos e teto máximo de milhas.
- [tracker.py](file:///home/edbrilhante/Área de Trabalho/Programação/Mlhas aéreas/tracker.py): Motor que consulta os voos e filtra as tarifas Clube Smiles abaixo do teto.
- [notifier.py](file:///home/edbrilhante/Área de Trabalho/Programação/Mlhas aéreas/notifier.py): Formata um e-mail HTML moderno e envia o resumo com links diretos.
- [main.py](file:///home/edbrilhante/Área de Trabalho/Programação/Mlhas aéreas/main.py): Ponto central de execução do robô.
- [.env.example](file:///home/edbrilhante/Área de Trabalho/Programação/Mlhas aéreas/.env.example): Modelo de configuração de e-mail/SMTP.

---

## 🚀 Como Configurar e Usar

### 1. Configurar o Telegram (Recomendado - 2 minutos)
1. No Telegram, abra uma conversa com o [@BotFather](https://t.me/BotFather) e envie o comando `/newbot`.
2. Siga as instruções para dar um nome ao bot e copie o **HTTP API Token** gerado.
3. Abra uma conversa com o [@userinfobot](https://t.me/userinfobot) (ou inicie seu próprio bot recém-criado dando `/start`) para descobrir o seu **ID** numérico (Chat ID).
4. Abra o arquivo [.env](file:///home/edbrilhante/Área de Trabalho/Programação/Mlhas aéreas/.env) e preencha:
   ```dotenv
   TELEGRAM_BOT_TOKEN=seu_token_aqui
   TELEGRAM_CHAT_ID=seu_chat_id_aqui
   ```

### 2. Testar o envio de alerta
Para testar o envio com dados simulados:
```bash
python3 test_notifier.py
```
Se estiver tudo certo, a notificação chegará diretamente no seu Telegram com links clicáveis!

### 3. Rodar a busca real
```bash
python3 main.py
```

### 4. Agendar para rodar automaticamente todo dia (Cron)
Para rodar todos os dias às 08:00 da manhã no seu Linux:
```bash
crontab -e
```
Adicione a linha:
```cron
0 8 * * * cd "/home/edbrilhante/Área de Trabalho/Programação/Mlhas aéreas" && python3 main.py >> tracker.log 2>&1
```

