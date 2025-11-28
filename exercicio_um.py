import json
from pathlib import Path
from typing import Any, Dict, List, Optional

COMMISSION_RATE_1 = 0.01
COMMISSION_RATE_5 = 0.05

def load_json(filepath: Path) -> Optional[Dict[str, Any]]:
    """Carrega JSON de um arquivo, retornando None se não existir."""
    try:
        with filepath.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def save_json(filepath: Path, data: Dict[str, Any]) -> None:
    """Salva dados em JSON com indentação para facilitar leitura."""
    with filepath.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def calculate_commission_for_sale(sale_value: float) -> float:
    """Retorna o valor da comissão com base no valor da venda."""
    if sale_value < 100:
        return 0.0
    elif sale_value < 500:
        return round(sale_value * COMMISSION_RATE_1, 2)
    else:
        return round(sale_value * COMMISSION_RATE_5, 2)

def update_commissions(sales_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Atualiza a lista de vendas com o campo 'comissao' calculado."""
    updated = []
    for sale in sales_data:
        try:
            value = float(sale.get("valor", 0))
        except (TypeError, ValueError):
            # se valor inválido, considera comissão zero
            commission = 0.0
        else:
            commission = calculate_commission_for_sale(value)

        sale["comissao"] = commission
        updated.append(sale)
    return updated

def process_sales_file(filepath: Path) -> None:
    """Lê o arquivo de vendas, atualiza comissões e escreve de volta."""
    data = load_json(filepath)
    if data is None or "vendas" not in data:
        print(f"Arquivo {filepath} não existe ou não contém 'vendas'.")
        return

    sales = data["vendas"]
    data["vendas"] = update_commissions(sales)
    save_json(filepath, data)
    print("Comissões atualizadas com sucesso.")
    print(json.dumps(data, ensure_ascii=False, indent=4))

if __name__ == "__main__":
    SALES_FILE = Path("vendas.json")
    process_sales_file(SALES_FILE)
