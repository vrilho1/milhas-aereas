#!/usr/bin/env python3
"""
Monitor Diário de Milhas Smiles
Foco: Rio de Janeiro (GIG/SDU) e Belo Horizonte (CNF) -> Nacionais e América do Sul
"""

import sys
from tracker import SmilesTracker
from notifier import Notifier

def main():
    print("=" * 60)
    print("✈️  MONITOR DE MILHAS SMILES - ALERTA DE OPORTUNIDADES")
    print("=" * 60)

    # 1. Inicializa os módulos
    tracker = SmilesTracker(config_path="rotas.json")
    notifier = Notifier()

    # 2. Executa a varredura das rotas
    ofertas = tracker.varrer_rotas(dias_futuros=45)

    print("\n" + "=" * 60)
    print(f"📊 Varredura concluída! Total de oportunidades encontradas: {len(ofertas)}")
    print("=" * 60)

    # 3. Notifica se houver oportunidades
    if ofertas:
        notifier.enviar_alerta(ofertas)
    else:
        print("Nenhuma passagem encontrada abaixo dos tetos no momento.")
        print("O robô continuará monitorando na próxima execução!")

if __name__ == "__main__":
    main()
