import requests
from rich import print
from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()


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
            if id_crypto in dados and moeda in dados[id_crypto]:
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
            if crypto1 in dados and crypto2 in dados and moeda in dados[crypto1] and moeda in dados[crypto2]:
                preco1 = dados[crypto1][moeda]
                preco2 = dados[crypto2][moeda]
                par = preco1 / preco2
                print(f"\n{crypto1.upper()}: {moeda.upper()} {preco1:,.2f}")
                print(f"{crypto2.upper()}: {moeda.upper()} {preco2:,.2f}")
                print(f"\n1 {crypto1.upper()} = {par:.8f} {crypto2.upper()}")
                return dados
            else:
                print("❌ Uma ou ambas as cryptos não encontradas")
                return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro na requisição: {e}")
            return None

    def get_top(self):
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "price_change_percentage_24h_desc",
            "per_page": 10,
            "page": 1
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            coins = response.json()

            table = Table(title="Top Cryptos")
            table.add_column("Nome", style="cyan")
            table.add_column("Simbolo", style="magenta")
            table.add_column("Preço (USD)", style="green")
            table.add_column("Variaçao", style="bold")

            for coin in coins:
                variacao = coin.get("price_change_percentage_24h", 0) or 0
                cor = "green" if variacao >= 0 else "red"
                table.add_row(
                    coin["name"],
                    coin["symbol"].upper(),
                    f"${coin['current_price']:.2f}",
                    f"[{cor}]{variacao:.2f}%[/{cor}]"
                )

            console.print(table)
            return coins
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro na requisição: {e}")
            return None


def main():
    app = Crypto()

    menu = """
[bold cyan]1[/bold cyan] PRICE UNIQUE CRYPTO
[bold cyan]2[/bold cyan] PRICE FOR PAR CRYPTO
[bold cyan]3[/bold cyan] TOP CRYPTOS
[bold cyan]4[/bold cyan] SAIR
"""
    console.print(Panel(menu, title="[bold green]MENU CRYPTO[/bold green]", expand=False))

    select = Prompt.ask("Selecione")

    if select == "1":
        crypto = Prompt.ask("Crypto")
        currency = Prompt.ask("Currency ex: usd")
        app.get_price(crypto, currency)

    elif select == "2":
        crypto1 = Prompt.ask("Crypto 1")
        crypto2 = Prompt.ask("Crypto 2")
        moeda = Prompt.ask("Currency ex: usd")
        app.get_par(crypto1, crypto2, moeda)

    elif select == "3":
        app.get_top()

    elif select == "4":
        console.print("[bold magenta]Saindo...[/bold magenta]")

    else:
        console.print("[bold red]Opção inválida.[/bold red]")


if __name__ == "__main__":
    main()
