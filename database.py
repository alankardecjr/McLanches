import sqlite3

def conectar():
    """Conecta ao banco de dados deliveryVS3.db"""
    return sqlite3.connect("deliveryVS3.db")

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()
    
    try:
        # 1. Tabela de Produtos (itens)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS itens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT UNIQUE NOT NULL,
            preco REAL NOT NULL,
            quantidade INTEGER DEFAULT 0,
            categoria TEXT,
            status_item TEXT DEFAULT 'em estoque'
        )""")

        # 2. Tabela de Clientes
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT UNIQUE NOT NULL,
            logradouro TEXT NOT NULL,
            numero TEXT,
            bairro TEXT,
            ponto_referencia TEXT,
            observacao TEXT,
            status_cliente TEXT DEFAULT 'Ativo'
        )""")

        # 3. Tabela de Pedidos
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            valor_total REAL NOT NULL,
            data TEXT DEFAULT (datetime('now', 'localtime')),
            status_pedido TEXT DEFAULT 'pendente',
            FOREIGN KEY (cliente_id) REFERENCES clientes (id)
        )""")
        
        conn.commit()
    finally:
        conn.close()

# --- GESTÃO DE CLIENTES ---

def salvar_cliente(nome, telefone, logradouro, numero, bairro, referencia, obs, status='Ativo'):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO clientes (nome, telefone, logradouro, numero, bairro, ponto_referencia, observacao, status_cliente) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", 
            (nome, telefone, logradouro, numero, bairro, referencia, obs, status))    
        conn.commit()
    finally:
        conn.close()

def listar_clientes():
    """Retorna todos os clientes em ordem alfabética"""
    conn = conectar()
    cursor = conn.cursor()
    # ORDER BY nome ASC garante a ordem de A a Z
    cursor.execute("SELECT * FROM clientes ORDER BY nome ASC")
    dados = cursor.fetchall()
    conn.close()
    return dados

def atualizar_cliente(id_cliente, nome, telefone, logra, num, bairro, ref, obs, status):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE clientes SET nome=?, telefone=?, logradouro=?, numero=?, bairro=?, 
            ponto_referencia=?, observacao=?, status_cliente=? WHERE id=?""",
            (nome, telefone, logra, num, bairro, ref, obs, status, id_cliente))
        conn.commit()
    finally:
        conn.close()

# --- GESTÃO DE PRODUTOS (ITENS) ---

def salvar_item(produto, preco, quantidade, categoria, status='em estoque'):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO itens (produto, preco, quantidade, categoria, status_item) 
            VALUES (?, ?, ?, ?, ?)""", (produto, preco, quantidade, categoria, status))
        conn.commit()
    finally:
        conn.close()

def listar_itens():
    """Retorna todos os itens em ordem alfabética"""
    conn = conectar()
    cursor = conn.cursor()
    # ORDER BY produto ASC garante a ordem de A a Z
    cursor.execute("SELECT * FROM itens ORDER BY produto ASC")
    dados = cursor.fetchall()
    conn.close()
    return dados

# --- GESTÃO DE PEDIDOS ---

def salvar_pedido(cliente_id, valor_total, status='pendente'):
    """Salva um novo pedido e faz o commit imediato"""
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO pedidos (cliente_id, valor_total, status_pedido) 
            VALUES (?, ?, ?)""", (cliente_id, valor_total, status))
        conn.commit()
    finally:
        conn.close()

def listar_pedidos():
    """Retorna lista de pedidos (Recentes Primeiro)"""
    conn = conectar()
    cursor = conn.cursor()
    query = """
    SELECT p.id, c.nome, p.valor_total, p.data, p.status_pedido
    FROM pedidos p
    JOIN clientes c ON p.cliente_id = c.id
    ORDER BY p.id DESC
    """
    cursor.execute(query)
    dados = cursor.fetchall()
    conn.close()
    return dados

def listar_pedidos_detalhados():
    """Retorna pedidos com informações detalhadas"""
    conn = conectar()
    cursor = conn.cursor()
    query = """
    SELECT p.id, c.nome, p.valor_total, p.data, p.status_pedido, 
           c.status_cliente, c.logradouro, c.bairro
    FROM pedidos p
    JOIN clientes c ON p.cliente_id = c.id 
    ORDER BY p.id DESC
    """
    cursor.execute(query)
    dados = cursor.fetchall()
    conn.close()
    return dados

def atualizar_status_pedido(id_pedido, novo_status):
    """Atualiza o status e confirma em tempo real"""
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE pedidos SET status_pedido = ? WHERE id = ?", (novo_status, id_pedido))
        conn.commit()
    finally:
        conn.close()

# --- INICIALIZAÇÃO ---

if __name__ == "__main__":
    criar_tabelas()
    print("Banco de dados deliveryVS3.db estruturado e atualizado com sucesso!")