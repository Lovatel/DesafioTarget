import json
import sys
from typing import Any, Dict, List, Optional


def clear_screen() -> None:
    """Limpa a tela do terminal."""
    print("\033c", end="")


def print_menu() -> None:
    """Exibe o menu de opções para o usuário."""
    print("__Programa de movimentações de estoque dos produtos__")
    print("Digite a opção da ação que deseja realizar.")
    print("1 => Apresentar Estoque.")
    print("2 => Apresentar Movimentações.")
    print("3 => Dar entrada de mercadoria.")
    print("4 => Dar saída de mercadoria.")
    print("5 => Sair do programa.")


def safe_int_convert(prompt: str) -> int:
    """Tenta converter para int; repete até o usuário entrar com valor válido."""
    while True:
        try:
            value = input(prompt)
            return int(value)
        except ValueError:
            print("Valor inválido, digite novamente.")


def calculate_max_id(transactions: List[Dict[str, Any]]) -> int:
    """Retorna o maior id e prepara para o próximo."""
    return max((t.get("id_da_movimentação", 0) for t in transactions), default=0)


def load_json_file(filepath: str) -> Optional[Dict[str, Any]]:
    """Tenta carregar um JSON; retorna None se o arquivo não existir."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def save_json_file(filepath: str, data: Dict[str, Any]) -> None:
    """Salva dados em um arquivo JSON com codificação UTF-8."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def show_stock() -> None:
    data = load_json_file("estoque.json")
    if data is None:
        print("Não há estoque cadastrado.")
    else:
        print(json.dumps(data, ensure_ascii=False, indent=4))


def show_transactions() -> None:
    data = load_json_file("movimentacoes.json")
    if data is None or not data.get("movimentacoes"):
        print("Não existem movimentações cadastradas ainda.")
    else:
        print(json.dumps(data, ensure_ascii=False, indent=4))


def add_transaction(
    product_id: str, product_name: str, product_quantity: int, movement_type: str
) -> None:
    """Adiciona uma movimentação (entrada ou saída) no arquivo JSON."""
    key = "movimentacoes"
    data = load_json_file("movimentacoes.json")
    if data is None:
        transactions = []
    else:
        transactions = data.get(key, [])

    new_id = calculate_max_id(transactions) + 1
    new_entry = {
        "id_da_movimentacao": new_id,
        "id_do_produto": product_id,
        "nome_do_produto": product_name,
        "quantidade_do_produto": product_quantity,
        "tipo_da_movimentacao": movement_type,
    }

    transactions.append(new_entry)
    save_json_file("movimentacoes.json", {key: transactions})
    print("Movimentação adicionada com sucesso.")
    print(json.dumps({key: transactions}, ensure_ascii=False, indent=4))


def update_stock(
    product_id: str, product_name: str, quantity_delta: int
) -> None:
    """Atualiza o estoque conforme a movimentação."""
    data = load_json_file("estoque.json") or {"estoque": []}
    stock_list = data.get("estoque", [])
    for item in stock_list:
        if item.get("codigoProduto") == product_id:
            item["estoque"] = int(item.get("estoque", 0)) + quantity_delta
            break
    else:
        # não encontrou produto existente — adiciona novo
        stock_list.append(
            {
                "codigoProduto": product_id,
                "descricaoProduto": product_name,
                "estoque": quantity_delta,
            }
        )
    data["estoque"] = stock_list
    save_json_file("estoque.json", data)

    total = next(
        (item["estoque"] for item in stock_list if item["codigoProduto"] == product_id),
        quantity_delta,
    )
    print(f"Quantidade de produtos existentes: {total}")


def handle_add_entry() -> None:
    product_id = input("Digite o Id da mercadoria: ")
    product_name = input("Digite o nome da mercadoria: ")
    product_quantity = safe_int_convert("Digite a quantidade que deseja adicionar: ")
    add_transaction(product_id, product_name, product_quantity, "adiçao")
    update_stock(product_id, product_name, product_quantity)


def handle_remove_entry() -> None:
    product_id = input("Digite o Id da mercadoria: ")
    product_name = input("Digite o nome da mercadoria: ")
    product_quantity = safe_int_convert("Digite a quantidade que deseja remover: ")
    add_transaction(product_id, product_name, product_quantity, "remocao")
    update_stock(product_id, product_name, -product_quantity)


def run_system() -> None:
    """Loop principal do sistema — exibe menu e trata opções do usuário."""
    while True:
        print_menu()
        try:
            option = safe_int_convert(": ")
        except KeyboardInterrupt:
            print("\nSaindo...")
            sys.exit()

        if option == 1:
            show_stock()
        elif option == 2:
            show_transactions()
        elif option == 3:
            handle_add_entry()
        elif option == 4:
            handle_remove_entry()
        elif option == 5:
            print("Saindo do programa.")
            sys.exit()
        else:
            print("Comando inválido, tente novamente.")

        _ = input("Pressione Enter para continuar...")
        clear_screen()


if __name__ == "__main__":
    run_system()