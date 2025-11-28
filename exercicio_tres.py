from datetime import datetime
from typing import TypedDict, Dict, Any


class FeeResult(TypedDict):
    dias_atraso: int
    juros: float
    valor_final: float


def calculate_fees(value: float, due_date_str: str, date_format: str = "%d/%m/%Y") -> FeeResult:
    """
    Calcula juros simples por atraso com base no valor e data de vencimento.

    :param value: valor original
    :param due_date_str: data de vencimento como string (ex: "dd/mm/YYYY")
    :param date_format: formato da data de vencimento
    :return: dicionário com dias de atraso, juros, e valor final
    """
    try:
        due_date = datetime.strptime(due_date_str, date_format).date()
    except ValueError as err:
        raise ValueError(f"Formato de data inválido: '{due_date_str}' (esperado {date_format})") from err

    today = datetime.today().date()
    delay_days = (today - due_date).days

    if delay_days <= 0:
        return {"dias_atraso": 0, "juros": 0.0, "valor_final": value}

    daily_rate = 0.025  # taxa por dia de atraso (2.5%)

    juros = value * daily_rate * delay_days
    final_value = value + juros

    return {"dias_atraso": delay_days, "juros": juros, "valor_final": final_value}


def main():
    valor_original = 1000.00
    data_vencimento = "15/11/2025"

    try:
        resultado = calculate_fees(valor_original, data_vencimento)
    except ValueError as e:
        print("Erro:", e)
        return

    dias = resultado["dias_atraso"]
    juros = resultado["juros"]
    valor_final = resultado["valor_final"]

    print(f"Dias de atraso: {dias}")
    print(f"Juros: R$ {juros:.2f}")
    print(f"Valor final: R$ {valor_final:.2f}")


if __name__ == "__main__":
    main()