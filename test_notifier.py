import sys
from notifier import Notifier

def simular():
    print("Testando o módulo de notificações com dados simulados...")
    
    ofertas_exemplo = [
        {
            "origem": "SDU",
            "destino": "CGH",
            "data": "2026-11-15",
            "milhas_clube": 6200,
            "teto": 9000,
            "taxas": 38.50,
            "link_resgate": "https://www.smiles.com.br"
        },
        {
            "origem": "GIG",
            "destino": "EZE",
            "data": "2026-12-04",
            "milhas_clube": 21800,
            "teto": 26000,
            "taxas": 180.20,
            "link_resgate": "https://www.smiles.com.br"
        },
        {
            "origem": "CNF",
            "destino": "SCL",
            "data": "2026-11-28",
            "milhas_clube": 27500,
            "teto": 33000,
            "taxas": 210.00,
            "link_resgate": "https://www.smiles.com.br"
        }
    ]

    notificador = Notifier()
    notificador.enviar_alerta(ofertas_exemplo)

if __name__ == "__main__":
    simular()
