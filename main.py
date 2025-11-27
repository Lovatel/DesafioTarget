"""
Considerando que o json abaixo tem registros de vendas de um time comercial, faça um programa que leia os dados e calcule a comissão de cada vendedor, seguindo a seguinte regra para cada venda:
•	Vendas abaixo de R$100,00 não gera comissão
•	Vendas abaixo de R$500,00 gera 1% de comissão
•	A partir de R$500,00 gera 5% de comissão

"""

import json, sys

COMMISSION_RATE_1 = 0.01
COMMISSION_RATE_5 = 0.05

def exercise_one():
    with open("vendas.json", "r", encoding="utf8") as f:
        data = json.load(f)
        for sales in data["vendas"]:
            if float(sales["valor"]) < 100:
                sales["comissão"] = "0"
            elif float(sales["valor"]) < 500:
                sales["comissão"] = round(sales["valor"] * COMMISSION_RATE_1, 2)
            elif float(sales["valor"]) >= 500:
                sales["comissão"] = round(sales["valor"] * COMMISSION_RATE_5, 2)
            
        print(data)

#exercise_one()

"""

2. Faça um programa onde eu possa lançar movimentações de estoque dos produtos que estão no json abaixo, dando entrada ou saída da mercadoria no meu depósito, onde cada movimentação deve ter:
•	Um número identificador único.
•	Uma descrição para identificar o tipo da movimentação realizada
E que ao final da movimentação me retorne a qtde final do estoque do produto movimentado.

"""

def clear_screen():
    print("\033c", end="")

def print_menu():
    print("__Programa de movimentações de estoque dos produtos__")
    print("Digite a opção da ação que deseja realizar.")
    print("1 => Apresentar Estoque.")
    print("2 => Apresentar Movimentações.")
    print("3 => Dar entrada de mercadoria.")
    print("4 => Dar saída de mercadoria.")
    print("5 => Sair do programa.")

def safe_int_convert(value):
    try:
        return int(value)
    except:
        return safe_int_convert(input("Valor inválido, digite novamente: "))
    
def exercise_two():
    
    while True:
        print_menu()

        try:
            option = int(input(": "))
        except:
            option = None

        if option == 1:
            with open("estoque.json", "r", encoding="utf8") as f:
                data = json.load(f)
                print(data)
        elif option == 2:
            try:
                with open("movimentacoes.json", "r", encoding="utf8") as f:
                    data = json.load(f)
                    print(data)
            except FileNotFoundError:
                print("Não existem movimentações cadastradas ainda.")
        elif option == 3:
            product_name = input("Digite o nome da mercadoria: ")
            product_quantity = safe_int_convert(input("Digite a quantidade que deseja adicionar: "))


        elif option == 4:
            product_name = input("Digite o nome da mercadoria: ")
            product_quantity = safe_int_convert(input("Digite a quantidade que deseja remover: "))
        elif option == 5:
            sys.exit()
        else:
            print("Comando inválido, tente novamente.")

        _ = input()
        clear_screen()
        

exercise_two()

"""

3. Faça um programa que a partir de um valor e de uma data de vencimento, calcule o valor dos juros na data de hoje considerando que a multa seja de 2,5% ao dia.

"""

#def exercise_three():

#exercise_three()