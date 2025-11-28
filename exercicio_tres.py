from datetime import datetime

def calculate_fees(value, due_date):
    date = datetime.strptime(due_date, "%d/%m/%Y").date()
    today = datetime.today().date()

    delay_days = (today - date).days

    if delay_days <= 0:
        return {
            "dias_atraso": 0,
            "juros": 0.0,
            "valor_final": value
        }

    tax_day_percentage = 0.025

    fees = value * tax_day_percentage * delay_days
    final_value = value + fees

    return {
        "dias_atraso": delay_days,
        "juros": fees,
        "valor_final": final_value
    }

value = 1000.00
final_date = "15/11/2025"

result = calculate_fees(value, final_date)

print(f"Dias de atraso: {result['dias_atraso']}")
print(f"Juros: R$ {result['juros']:.2f}")
print(f"Valor final: R$ {result['valor_final']:.2f}")