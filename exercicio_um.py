import json

COMMISSION_RATE_1 = 0.01
COMMISSION_RATE_5 = 0.05

def calculate_comission():
    with open("vendas.json", "r+", encoding="utf8") as f:
        data = json.load(f)
        for sales in data["vendas"]:
            if float(sales["valor"]) < 100:
                sales["comissão"] = "0"
            elif float(sales["valor"]) < 500:
                sales["comissão"] = round(sales["valor"] * COMMISSION_RATE_1, 2)
            elif float(sales["valor"]) >= 500:
                sales["comissão"] = round(sales["valor"] * COMMISSION_RATE_5, 2)
            
        json.dump(data, f, indent= 4)
            
        print(data)

calculate_comission()