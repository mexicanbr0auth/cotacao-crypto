import requests
from rich import print



class Crypto:
    def __init__(self):
        self.api = "https://api.coingecko.com/api/v3/simple/price"
    def get_price(self, id_crypto, moeda):
        params = {
                "ids": id_crypto,
                "vs_currencies": moeda
                    }
        try:
            response = requests.get(self.api, params=params)
            response.raise_for_status()
            dados = response.json()
            if id_crypto in dados:
                preco = dados[id_crypto][moeda]
                print(f"{id_crypto.upper()}: {moeda.upper()} {preco:,.2f}")
                return dados
            else:
                print(f"Crypto: '{id_crypto}' Nao Encontrada")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Erro Na Requisicao: {e}")
            return None
    def get_par(self, crypto1, crypto2, moeda):
        params = {
                "ids": f"{crypto1},{crypto2}",
                "vs_currencies": moeda
                }
        try:
            response = requests.get(self.api, params=params)
            response.raise_for_status()
            dados = response.json()
            if crypto1 in dados and crypto2 in dados:
                preco1 = dados[crypto1][moeda]
                preco2 = dados[crypto2][moeda]
                par = preco1 / preco2
                print(f"\n{crypto1.upper()}: {moeda.upper()} {preco1:,.2f}")
                print(f"{crypto2.upper()}: {moeda.upper()} {preco2:,.2f}")
                print(f"\n1 {crypto1.upper()} = {par:.8f} {crypto2.upper()}")
                return dados
            else:
                print(f"❌ Uma ou ambas as cryptos não encontradas")
                return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro na requisição: {e}")
            return None


    
Main = Crypto()

print("""
      _____________
    1 PRICE UNIQUE Crypto
    2 PRICE FOR PAR CRYPTO 

      """)
select = input("Selecione: ")
if select == "1":
    Main.get_price(input("Crypto: "), input("Currencie Ex: usd: "))
elif select == "2":
    Main.get_par(input("Crypto 1: "), input("Crypto 2: "), input("Currencie: "))


