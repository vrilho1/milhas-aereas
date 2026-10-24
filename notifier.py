import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Dict
import requests
from dotenv import load_dotenv

load_dotenv()

class Notifier:
    def __init__(self):
        # Configurações do Telegram
        self.telegram_token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
        self.telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID", "").strip()

        # Configurações de E-mail (fallback/opcional)
        self.smtp_server = os.getenv("EMAIL_SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("EMAIL_SMTP_PORT", 587))
        self.remetente = os.getenv("EMAIL_REMETENTE", "").strip()
        self.senha = os.getenv("EMAIL_SENHA", "").strip()
        self.destinatario = os.getenv("EMAIL_DESTINATARIO", "").strip()

    def is_telegram_configured(self) -> bool:
        """Verifica se as credenciais do Telegram estão configuradas."""
        return bool(self.telegram_token and self.telegram_chat_id and "seu_token" not in self.telegram_token)

    def is_email_configured(self) -> bool:
        """Verifica se as credenciais de e-mail foram preenchidas."""
        return bool(self.remetente and self.senha and self.destinatario and "seu_email" not in self.remetente)

    def formatar_mensagem_telegram(self, ofertas: List[Dict]) -> str:
        """Gera mensagem formatada em HTML compatível com o Telegram."""
        total = len(ofertas)
        texto = f"🔥 <b>{total} Oportunidade(s) Imperdível(is) Smiles!</b>\n\n"

        for item in ofertas:
            milhas = f"{item['milhas_clube']:,}".replace(",", ".")
            teto = f"{item['teto']:,}".replace(",", ".")
            taxas = f"R$ {item.get('taxas', 0.0):.2f}".replace(".", ",")
            link = item.get("link_resgate", "https://www.smiles.com.br")

            texto += (
                f"✈️ <b>{item['origem']} ➔ {item['destino']}</b>\n"
                f"📅 Data: <code>{item['data']}</code>\n"
                f"💎 Milhas: <b>{milhas}</b> (Teto: {teto})\n"
                f"💰 Taxas: {taxas}\n"
                f"🔗 <a href=\"{link}\">Acessar no Smiles</a>\n\n"
            )

        texto += "💡 <i>As disponibilidades da Smiles variam rapidamente. Garanta seu trecho!</i>"
        return texto

    def enviar_telegram(self, ofertas: List[Dict]) -> bool:
        """Envia o alerta para o chat do Telegram."""
        if not self.is_telegram_configured():
            return False

        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        payload = {
            "chat_id": self.telegram_chat_id,
            "text": self.formatar_mensagem_telegram(ofertas),
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }

        try:
            resp = requests.post(url, json=payload, timeout=15)
            data = resp.json()
            if resp.status_code == 200 and data.get("ok"):
                print("[SUCESSO] Alerta enviado para o Telegram com sucesso!")
                return True
            else:
                print(f"[ERRO TELEGRAM] Falha na API: {data.get('description', resp.text)}")
                return False
        except Exception as e:
            print(f"[ERRO TELEGRAM] Exceção ao conectar com Telegram: {e}")
            return False

    def formatar_html_email(self, ofertas: List[Dict]) -> str:
        """Gera um e-mail HTML com as ofertas encontradas."""
        linhas_tabela = ""
        for item in ofertas:
            linhas_tabela += f"""
            <tr style="border-bottom: 1px solid #e5e7eb;">
                <td style="padding: 12px; font-weight: 600; color: #111827;">{item['origem']} ➔ {item['destino']}</td>
                <td style="padding: 12px; color: #4b5563;">{item['data']}</td>
                <td style="padding: 12px; color: #047857; font-weight: 700; font-size: 15px;">
                    {item['milhas_clube']:,} milhas
                    <span style="display: block; font-size: 11px; color: #6b7280; font-weight: normal;">
                        Teto: {item['teto']:,}
                    </span>
                </td>
                <td style="padding: 12px; color: #374151;">R$ {item.get('taxas', 0.0):.2f}</td>
                <td style="padding: 12px; text-align: center;">
                    <a href="{item.get('link_resgate', 'https://www.smiles.com.br')}" 
                       target="_blank"
                       style="background: #ea580c; color: #ffffff; text-decoration: none; padding: 6px 12px; border-radius: 6px; font-size: 13px; font-weight: 600; display: inline-block;">
                       Ver Voo
                    </a>
                </td>
            </tr>
            """

        return f"""
        <!DOCTYPE html>
        <html>
        <head><meta charset="utf-8"></head>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f3f4f6; margin: 0; padding: 20px;">
            <div style="max-width: 680px; margin: 0 auto; background: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
                <div style="background: linear-gradient(135deg, #ea580c 0%, #f97316 100%); padding: 24px; color: #ffffff;">
                    <h1 style="margin: 0; font-size: 22px; font-weight: 700;">✈️ Alerta de Milhas Smiles Imperdíveis</h1>
                    <p style="margin: 8px 0 0 0; opacity: 0.9; font-size: 14px;">Encontramos trechos abaixo do seu teto estipulado para Clube Smiles!</p>
                </div>
                <div style="padding: 24px;">
                    <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 14px;">
                        <thead>
                            <tr style="background: #f9fafb; color: #6b7280; text-transform: uppercase; font-size: 11px; letter-spacing: 0.05em;">
                                <th style="padding: 10px 12px;">Rota</th>
                                <th style="padding: 10px 12px;">Data</th>
                                <th style="padding: 10px 12px;">Milhas (Clube)</th>
                                <th style="padding: 10px 12px;">Taxas</th>
                                <th style="padding: 10px 12px; text-align: center;">Ação</th>
                            </tr>
                        </thead>
                        <tbody>{linhas_tabela}</tbody>
                    </table>
                </div>
            </div>
        </body>
        </html>
        """

    def enviar_email(self, ofertas: List[Dict]) -> bool:
        """Envia alerta por e-mail se configurado."""
        if not self.is_email_configured():
            return False

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"🔥 {len(ofertas)} Oportunidade(s) Imperdível(is) de Milhas Smiles!"
            msg["From"] = self.remetente
            msg["To"] = self.destinatario

            corpo_html = self.formatar_html_email(ofertas)
            msg.attach(MIMEText(corpo_html, "html"))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.remetente, self.senha)
                server.sendmail(self.remetente, self.destinatario, msg.as_string())

            print(f"[SUCESSO] Alerta enviado por e-mail para {self.destinatario}!")
            return True
        except Exception as e:
            print(f"[ERRO E-MAIL] Falha ao enviar e-mail: {e}")
            return False

    def enviar_alerta(self, ofertas: List[Dict]) -> bool:
        """Envia alertas preferencialmente pelo Telegram, ou por e-mail se configurado."""
        if not ofertas:
            print("Nenhuma oferta para enviar.")
            return False

        telegram_ok = False
        email_ok = False

        if self.is_telegram_configured():
            telegram_ok = self.enviar_telegram(ofertas)
        
        if self.is_email_configured():
            email_ok = self.enviar_email(ofertas)

        if not telegram_ok and not email_ok:
            print("\n[AVISO] Nenhum canal de notificação configurado ou ativo no arquivo .env.")
            print("Para receber via Telegram, preencha TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID.")
            print("\nSimulando visualização das ofertas no console:")
            for o in ofertas:
                print(f"  -> {o['origem']} -> {o['destino']} em {o['data']}: {o['milhas_clube']:,} milhas (Teto: {o['teto']:,})")
            return False

        return telegram_ok or email_ok

