import sqlite3

def conectar():
    return sqlite3.connect("deliveryVs4.db")

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()
    
    try:
        # 1. Itens/Produtos
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS itens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT UNIQUE NOT NULL,
            preco REAL NOT NULL,
            quantidade INTEGER DEFAULT 0,
            categoria TEXT,
            status_item TEXT DEFAULT 'em estoque'
        )""")

        # 2. Clientes
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT UNIQUE NOT NULL,
            logradouro TEXT NOT NULL,
            numero INTEGER NOT NULL,
            bairro TEXT,
            ponto_referencia TEXT,
            observacao TEXT,
            status_cliente TEXT DEFAULT 'Ativo'
        )""")

        # 3. Pedidos (Cabeçalho)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            valor_total REAL NOT NULL,
            data TEXT DEFAULT (datetime('now', 'localtime')),
            status_pedido TEXT DEFAULT 'pendente',
            FOREIGN KEY (cliente_id) REFERENCES clientes (id)
        )""")

        # 4. ITENS DO PEDIDO (Melhoria 1: Relacionamento Muitos-para-Muitos)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS itens_pedido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            quantidade_vendida INTEGER NOT NULL,
            preco_unitario REAL NOT NULL,
            FOREIGN KEY (pedido_id) REFERENCES pedidos (id),
            FOREIGN KEY (item_id) REFERENCES itens (id)
        )""")
        
        conn.commit()
    finally:
        conn.close()

# --- GESTÃO DE ESTOQUE E VENDAS (Melhoria 2) ---

def registrar_pedido_completo(cliente_id, lista_produtos):
    """
    lista_produtos deve ser uma lista de tuplas: [(item_id, qtde, preco_un), ...]
    Realiza a venda e baixa o estoque em uma única transação.
    """
    conn = conectar()
    cursor = conn.cursor()
    valor_total = sum(p[1] * p[2] for p in lista_produtos)
    
    try:
        # Inserir cabeçalho do pedido
        cursor.execute("INSERT INTO pedidos (cliente_id, valor_total) VALUES (?, ?)", 
                       (cliente_id, valor_total))
        pedido_id = cursor.lastrowid

        for item_id, qtde, preco in lista_produtos:
            # Inserir na tabela de itens do pedido
            cursor.execute("""
                INSERT INTO itens_pedido (pedido_id, item_id, quantidade_vendida, preco_unitario)
                VALUES (?, ?, ?, ?)""", (pedido_id, item_id, qtde, preco))
            
            # Baixa automática no estoque
            cursor.execute("""
                UPDATE itens 
                SET quantidade = quantidade - ? 
                WHERE id = ?""", (qtde, item_id))
            
            # Atualizar status se chegar a zero
            cursor.execute("""
                UPDATE itens SET status_item = 'esgotado' 
                WHERE id = ? AND quantidade <= 0""", (item_id,))

        conn.commit()
        return True, pedido_id
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()

# --- BUSCAS E FILTROS (Melhoria 3) ---

def buscar_cliente_por_telefone(telefone):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes WHERE telefone = ?", (telefone,))
    cliente = cursor.fetchone()
    conn.close()
    return cliente

def filtrar_pedidos_por_status(status):
    conn = conectar()
    cursor = conn.cursor()
    query = """
    SELECT p.id, c.nome, p.valor_total, p.status_pedido 
    FROM pedidos p
    JOIN clientes c ON p.cliente_id = c.id
    WHERE p.status_pedido = ?
    ORDER BY p.id DESC
    """
    cursor.execute(query, (status,))
    dados = cursor.fetchall()
    conn.close()
    return dados

# --- FUNÇÕES ORIGINAIS MANTIDAS/OTIMIZADAS ---
# (Manter aqui as funções salvar_cliente, salvar_item, listar_itens, etc.)


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

def atualizar_item(id_item, produto, preco, quantidade, categoria, status):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE itens SET produto=?, preco=?, quantidade=?, categoria=?, status_item=? 
            WHERE id=?""", (produto, preco, quantidade, categoria, status, id_item))
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
    print("Banco de dados deliveryVs4.db estruturado e atualizado com sucesso!")