import json, sys

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
    
def calculate_max_id(transactions):
    return max((t.get("id_da_movimentação", 0) for t in transactions), default=0)
    
def run_system():
    
    while True:
        print_menu()

        try:
            option = int(input(": "))
        except:
            option = None

        if option == 1:
            with open("estoque.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                print(data)

        elif option == 2:
            try:
                with open("movimentações.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    print(data)
            except FileNotFoundError:
                print("Não existem movimentações cadastradas ainda.")

        elif option == 3:
            product_id = input("Digite o Id da mercadoria:")
            product_name = input("Digite o nome da mercadoria: ")
            product_quantity = safe_int_convert(input("Digite a quantidade que deseja adicionar: "))

            try:
                with open("movimentações.json", "r", encoding="utf-8") as f:
                    data = json.load(f)

                    transactions: list = data.get("movimentações", [])

                    max_id = calculate_max_id(transactions)
                    new_entry = {
                        "id_da_movimentação": max_id + 1,
                        "id_do_produto": product_id,
                        "nome_do_produto": product_name,
                        "quantidade_do_produto": product_quantity,
                        "tipo_da_movimentação": "adição"
                    }

                    transactions.append(new_entry)
                    data["movimentações"] = transactions

                    with open("movimentações.json", "w", encoding="utf-8") as w:
                        json.dump(data, w, ensure_ascii=False, indent=4)

                    print(data)
            except FileNotFoundError:
                data = [{
                    "id_da_movimentação" : 1,
                    "id_do_produto": product_id,
                    "nome_do_produto" : product_name,
                    "quantidade_do_produto" : product_quantity,
                    "tipo_da_movimentação" : "adição"
                }]

                transactions = {
                    "movimentações" : data
                }

                print(transactions)

                with open("movimentações.json", "w", encoding="utf-8") as w:
                    json.dump(transactions, w, ensure_ascii=False, indent= 4)

            is_existing_product = False

            with open("estoque.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                for stock in data["estoque"]:
                    if stock["codigoProduto"] == product_id:
                        is_existing_product = True
                        stock["estoque"] = int(stock["estoque"]) + product_quantity
                        result_quantity = stock["estoque"]
                if is_existing_product == False:
                    new_entry = {
		                "codigoProduto": product_id,
		                "descricaoProduto": product_name,
		                "estoque": product_quantity
	                }
                    data_list: list = data["estoque"]
                    data_list.append(new_entry)
                    data["estoque"] = data_list
                with open("estoque.json", "w", encoding="utf-8") as w:
                        json.dump(data, w, ensure_ascii=False, indent= 4)
                
                try:
                    if result_quantity is None:
                        result_quantity = product_quantity
                except UnboundLocalError:
                    result_quantity = product_quantity
                    
                print(f"Quantidade de produtos existentes: {result_quantity}")
                    
        elif option == 4:
            product_id = input("Digite o Id da mercadoria:")
            product_name = input("Digite o nome da mercadoria: ")
            product_quantity = safe_int_convert(input("Digite a quantidade que deseja remover: "))
            
            try:
                with open("movimentações.json", "r", encoding="utf-8") as f:
                    data = json.load(f)

                    transactions: list = data.get("movimentações", [])

                    max_id = calculate_max_id(transactions)
                    new_entry = {
                        "id_da_movimentação": max_id + 1,
                        "id_do_produto": product_id,
                        "nome_do_produto": product_name,
                        "quantidade_do_produto": product_quantity,
                        "tipo_da_movimentação": "remoção"
                    }

                    transactions.append(new_entry)
                    data["movimentações"] = transactions

                    with open("movimentações.json", "w", encoding="utf-8") as w:
                        json.dump(data, w, ensure_ascii=False, indent=4)

                    print(data)
            except FileNotFoundError:
                data = [{
                    "id_da_movimentação" : 1,
                    "id_do_produto": product_id,
                    "nome_do_produto" : product_name,
                    "quantidade_do_produto" : product_quantity,
                    "tipo_da_movimentação" : "remoção"
                }]

                transactions = {
                    "movimentações" : data
                }

                print(transactions)

                with open("movimentações.json", "w", encoding="utf-8") as w:
                    json.dump(transactions, w, ensure_ascii=False, indent= 4)

            is_existing_product = False
            
            with open("estoque.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                for stock in data["estoque"]:
                    if stock["codigoProduto"] == product_id:
                        is_existing_product = True
                        stock["estoque"] = int(stock["estoque"]) - product_quantity
                        result_quantity = stock["estoque"]
                if is_existing_product == False:
                    print("Produto não existe!")
                    
                with open("estoque.json", "w", encoding="utf-8") as w:
                        json.dump(data, w, ensure_ascii=False, indent= 4)
                
                print(f"Quantidade de produtos existentes: {result_quantity}")
            
        elif option == 5:
            sys.exit()
        else:
            print("Comando inválido, tente novamente.")

        _ = input()
        clear_screen()
        
run_system()