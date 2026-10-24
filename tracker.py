import json
import time
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class SmilesTracker:
    def __init__(self, config_path: str = "rotas.json"):
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)
        
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Origin": "https://www.smiles.com.br",
            "Referer": "https://www.smiles.com.br/",
            "x-api-key": "a3068e64-58a3-41a3-b467-33a7d42cf38f"
        })

    def buscar_voo_smiles(self, origem: str, destino: str, data_partida: str) -> Optional[Dict]:
        """
        Consulta os voos da Smiles para a rota e data informadas.
        data_partida deve estar no formato 'YYYY-MM-DD'.
        """
        url = (
            f"https://api.smiles.com.br/v1/abs/flightsearch"
            f"?originAirportCode={origem}"
            f"&destinationAirportCode={destino}"
            f"&departureDate={data_partida}"
            f"&adults=1"
            f"&tripType=2"
        )
        
        try:
            response = self.session.get(url, timeout=12)
            if response.status_code == 200:
                dados = response.json()
                return self._processar_resposta(dados, origem, destino, data_partida)
        except Exception as e:
            # Em caso de falha de conexão ou timeout na requisição
            pass
        return None

    def _processar_resposta(self, dados: dict, origem: str, destino: str, data_partida: str) -> Optional[Dict]:
        """Extrai a menor tarifa de milhas para Clube Smiles da resposta da API."""
        try:
            itinerarios = dados.get("flightSearch", {}).get("requestedFlight", {}).get("segmentList", [])
            melhor_oferta = None
            menor_milhas = float("inf")
            taxas = 0.0

            for seg in itinerarios:
                for voo in seg.get("flightList", []):
                    # Checa as opções tarifárias do voo
                    for fare in voo.get("fareList", []):
                        milhas_clube = fare.get("miles", {}).get("club") or fare.get("miles", {}).get("total")
                        if milhas_clube and milhas_clube < menor_milhas:
                            menor_milhas = milhas_clube
                            taxas = fare.get("money", {}).get("taxes", 0.0)

            if menor_milhas < float("inf"):
                link_smiles = f"https://www.smiles.com.br/mcom/voos?departure={origem}&arrival={destino}&departureDate={data_partida}&adults=1&tripType=2"
                return {
                    "origem": origem,
                    "destino": destino,
                    "data": data_partida,
                    "milhas_clube": menor_milhas,
                    "taxas": taxas,
                    "link_resgate": link_smiles
                }
        except Exception:
            pass
        return None

    def varrer_rotas(self, dias_futuros: int = 45) -> List[Dict]:
        """
        Percorre todas as rotas configuradas checando datas selecionadas
        e retorna apenas aquelas com valor abaixo do teto de milhas.
        """
        oportunidades = []
        rotas = self.config.get("rotas_monitoradas", [])
        data_base = datetime.now()

        print(f"\n🔍 Iniciando varredura para {len(rotas)} rotas configuradas...")

        # Testa datas estratégicas (ex: terças, quartas e sábados a cada semana)
        dias_para_testar = []
        for i in range(15, dias_futuros + 1, 7):
            dt = data_base + timedelta(days=i)
            dias_para_testar.append(dt.strftime("%Y-%m-%d"))

        for rota in rotas:
            origem = rota["origem"]
            destino = rota["destino"]
            teto = rota["teto_milhas_clube"]
            print(f"-> Verificando rota: {origem} ➔ {destino} (Teto: {teto:,} milhas)...")

            for data_str in dias_para_testar:
                res = self.buscar_voo_smiles(origem, destino, data_str)
                if res and res["milhas_clube"] <= teto:
                    res["teto"] = teto
                    res["descricao"] = rota.get("descricao", f"{origem} -> {destino}")
                    print(f"   🔥 [Oportunidade!] {data_str}: {res['milhas_clube']:,} milhas!")
                    oportunidades.append(res)
                
                # Pausa gentil para evitar bloqueios de taxa de requisições
                time.sleep(0.5)

        return oportunidades
