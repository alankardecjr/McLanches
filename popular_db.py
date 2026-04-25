import sqlite3
from database import conectar  # Certifique-se que o arquivo de banco de dados se chama database.py

def popular_banco():
    conn = conectar()
    if not conn:
        return
    
    cursor = conn.cursor()

    try:
        # 1. Populando Clientes (Nomenclatura: Ativo / Inativo)
        clientes = [
            ('João Silva', '11999999999', 'Rua das Flores', 123, 'Centro', 'Perto da Padaria', 'Cliente antigo', 'Ativo'),
            ('Maria Oliveira', '11988888888', 'Av. Principal', 500, 'Bairro Novo', 'Ao lado do mercado', '', 'Inativo'),
            ('Carlos Souza', '11977777777', 'Rua Tenente', 45, 'Vila Maria', '', 'Inadimplente', 'Vip'),
            ('Ana Costa', '11966666666', 'Rua 7 de Setembro', 10, 'Jardins', 'Portão Branco', 'Entregar na recepção', 'PDC/IDOSO')
        ]
        
        cursor.executemany("""
            INSERT OR IGNORE INTO clientes (nome, telefone, logradouro, numero, bairro, ponto_referencia, observacao, status_cliente)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, clientes)

        # 2. Populando Itens (Nomenclatura: Estoque / Esgotado)
        itens = [
            ('Pizza Calabresa', 45.00, 10, 'Pizzas', 'Estoque'),
            ('Pizza Margherita', 42.50, 8, 'Pizzas', 'Estoque'),
            ('Coca-Cola 2L', 12.00, 20, 'Bebidas', 'Estoque'),
            ('Suco de Laranja', 8.50, 5, 'Bebidas', 'Estoque'),
            ('Hambúrguer Artesanal', 32.00, 0, 'Lanches', 'Esgotado')
        ]
        
        cursor.executemany("""
            INSERT OR IGNORE INTO itens (produto, preco, quantidade, categoria, status_item)
            VALUES (?, ?, ?, ?, ?)
        """, itens)

        # 3. Populando Pedidos
        # O cliente_id 3 agora aparecerá com status 'Inativo' no JOIN da sua tela inicial
        pedidos = [
            (1, 57.00, '2026-04-25 10:00:00', 'Pendente'),
            (2, 42.50, '2026-04-25 10:15:00', 'Produção'),
            (3, 12.00, '2026-04-25 10:30:00', 'Finalizado'), 
            (4, 90.00, '2026-04-25 10:45:00', 'Entregue')
        ]
        
        cursor.executemany("""
            INSERT INTO pedidos (cliente_id, valor_total, data, status_pedido)
            VALUES (?, ?, ?, ?)
        """, pedidos)

        conn.commit()
        print("✅ Banco de dados populado com as novas nomenclaturas!")
        print("---")
        print("Status Clientes: Ativo / Inativo")
        print("Status Produtos: Estoque / Esgotado")

    except sqlite3.Error as e:
        print(f"❌ Erro ao popular banco: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    popular_banco()