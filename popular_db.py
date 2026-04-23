import database
import sqlite3
import random

def popular_banco():
    # 1. Garante a criação das tabelas no deliveryVS3.db
    database.criar_tabelas()
    conn = database.conectar()
    cursor = conn.cursor()

    print("--- Iniciando Povoamento do Banco de Dados VS3 ---")

    # --- 50 CLIENTES VARIADOS ---
    nomes_base = ["Ana", "Bruno", "Carla", "Daniel", "Eduarda", "Fabio", "Gisele", "Henrique", "Iara", "João"]
    sobrenomes = ["Silva", "Santos", "Oliveira", "Souza", "Pereira", "Costa", "Rodrigues", "Almeida", "Nascimento", "Lima"]
    bairros = ["Centro", "Jardins", "Vila Nova", "Bela Vista", "Itaim", "Alphaville", "Barra", "Leblon"]
    ruas = ["Rua das Flores", "Av. Brasil", "Rua Treze de Maio", "Av. Paulista", "Rua do Comércio", "Rua Amazonas"]

    clientes_dados = []
    for i in range(50):
        nome = f"{random.choice(nomes_base)} {random.choice(sobrenomes)}"
        tel = f"(11) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
        logra = random.choice(ruas)
        num = str(random.randint(1, 2000))
        bairro = random.choice(bairros)
        clientes_dados.append((nome, tel, logra, num, bairro, "Perto do mercado", "Sem observações", "Ativo"))

    # --- 30 ITENS (CARDÁPIO BOB'S) ---
    # Estrutura: (produto, preco, quantidade, categoria, status)
    produtos_bobs = [
        # Lanches
        ('Big Bob', 28.90, 50, 'Lanche', 'em estoque'),
        ('Bob’s Burger', 15.00, 40, 'Lanche', 'em estoque'),
        ('Double Cheese', 22.50, 30, 'Lanche', 'em estoque'),
        ('Cheddar Australiano', 31.00, 25, 'Lanche', 'em estoque'),
        ('Big Bob Picanha', 38.00, 20, 'Lanche', 'em estoque'),
        ('Tentador Carne', 32.00, 15, 'Lanche', 'em estoque'),
        ('Tentador Frango', 29.00, 15, 'Lanche', 'em estoque'),
        ('Bob’s Artesanal', 35.50, 10, 'Lanche', 'em estoque'),
        ('Crispy Frango', 24.00, 20, 'Lanche', 'em estoque'),
        ('Franlitos 6 unidades', 18.00, 100, 'Lanche', 'em estoque'),
        # Bebidas
        ('Coca-Cola 500ml', 9.00, 200, 'Bebida', 'em estoque'),
        ('Coca-Cola Zero 500ml', 9.00, 150, 'Bebida', 'em estoque'),
        ('Guaraná Antarctica 500ml', 8.50, 100, 'Bebida', 'em estoque'),
        ('Fanta Laranja 500ml', 8.50, 80, 'Bebida', 'em estoque'),
        ('Suco de Laranja 400ml', 11.00, 50, 'Bebida', 'em estoque'),
        ('Água Mineral 500ml', 5.00, 300, 'Bebida', 'em estoque'),
        ('Milk Shake Crocante 300ml', 16.00, 100, 'Bebida', 'em estoque'),
        ('Milk Shake Paçoca 500ml', 21.00, 80, 'Bebida', 'em estoque'),
        ('Milk Shake Morango 300ml', 16.00, 70, 'Bebida', 'em estoque'),
        ('Milk Shake Chocolate 500ml', 21.00, 90, 'Bebida', 'em estoque'),
        # Sobremesas
        ('Sundae Chocolate', 12.00, 60, 'Sobremesa', 'em estoque'),
        ('Sundae Morango', 12.00, 50, 'Sobremesa', 'em estoque'),
        ('Bob’s Max Baunilha', 14.50, 40, 'Sobremesa', 'em estoque'),
        ('Bob’s Max Ovomaltine', 15.50, 45, 'Sobremesa', 'em estoque'),
        ('Casquinha Recheada', 5.00, 500, 'Sobremesa', 'em estoque'),
        ('Casquinha Baunilha', 4.00, 600, 'Sobremesa', 'em estoque'),
        ('Petit Gateau', 18.00, 20, 'Sobremesa', 'em estoque'),
        ('Torta de Maçã', 9.00, 30, 'Sobremesa', 'em estoque'),
        ('Cone de Doce de Leite', 7.00, 100, 'Sobremesa', 'em estoque'),
        ('Mini Churros 5 unidades', 10.00, 40, 'Sobremesa', 'em estoque')
    ]

    # --- INSERÇÃO ---
    print("\nInserindo 50 Clientes...")
    for c in clientes_dados:
        try:
            cursor.execute("""INSERT INTO clientes 
                (nome, telefone, logradouro, numero, bairro, ponto_referencia, observacao, status_cliente) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", c)
        except sqlite3.IntegrityError:
            continue # Pula se o telefone gerado randomicamente repetir

    print("Inserindo 30 Produtos (Bobs)...")
    for p in produtos_bobs:
        try:
            cursor.execute("""INSERT INTO itens 
                (produto, preco, quantidade, categoria, status_item) 
                VALUES (?, ?, ?, ?, ?)""", p)
        except sqlite3.IntegrityError:
            continue

    # --- 5 PEDIDOS INICIAIS ---
    print("Inserindo 5 Pedidos Iniciais...")
    pedidos = [
        (1, 45.90, 'finalizado'),
        (2, 32.00, 'pendente'),
        (3, 110.50, 'finalizado'),
        (4, 15.00, 'cancelado'),
        (5, 58.00, 'pendente')
    ]
    for ped in pedidos:
        cursor.execute("INSERT INTO pedidos (cliente_id, valor_total, status_pedido) VALUES (?, ?, ?)", ped)

    conn.commit()
    conn.close()
    print("\n✅ Banco de dados 'deliveryVS3.db' populado com sucesso!")

if __name__ == "__main__":
    popular_banco()