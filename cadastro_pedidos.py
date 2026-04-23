import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import database  # Certifique-se de que o arquivo database.py está na mesma pasta

class JanelaCadastroPedidos(tk.Toplevel):
    def __init__(self, master, nome_cliente_inicial=None):
        super().__init__(master)
        self.title("Gerar Novo Pedido")
        self.geometry("1000x750") 
        self.configure(bg="#f4f6f9")
        
        # Paleta de Cores Monocromática (Discreta)
        self.bg_fundo = "#f4f6f9"
        self.bg_card = "#ffffff"
        self.cor_borda = "#d1d5db"
        self.cor_texto = "#1f2937"
        
        # Tons de Cinza para Botões e Feedback
        self.cinza_escuro = "#374151"  # Destaque / Seleção Ativa
        self.cinza_medio = "#6b7280"   # Ações Secundárias
        self.cinza_claro = "#9ca3af"   # Neutro / Sair
        self.cinza_selecao = "#e5e7eb" # Fundo para item selecionado (Clareado)

        self.cliente_selecionado = None
        self.total_pedido = 0.0

        self.criar_widgets()
        
        if nome_cliente_inicial:
            self.ent_busca_cliente.insert(0, nome_cliente_inicial)
            self.buscar_cliente()

    def criar_widgets(self):
        # --- HEADER (Busca e Listbox) ---
        header_frame = tk.Frame(self, bg=self.bg_fundo, pady=15, padx=20)
        header_frame.pack(fill="x")

        tk.Label(header_frame, text="BUSCAR CLIENTE:", bg=self.bg_fundo, fg="#4b5563", font=("Segoe UI", 9, "bold")).pack(side="left", padx=5)
        self.ent_busca_cliente = tk.Entry(header_frame, font=("Segoe UI", 11), width=20, relief="flat", highlightbackground=self.cor_borda, highlightthickness=1)
        self.ent_busca_cliente.pack(side="left", padx=5, ipady=3)
        
        tk.Button(header_frame, text="BUSCAR", command=self.buscar_cliente, bg=self.cinza_escuro, fg="white", font=("Segoe UI", 9, "bold"), padx=15, relief="flat", cursor="hand2").pack(side="left", padx=5)
        
        # Listbox de resultados (Cores Discretas)
        result_frame = tk.Frame(header_frame, bg=self.bg_card, highlightbackground=self.cor_borda, highlightthickness=1)
        result_frame.pack(side="left", padx=15, fill="both", expand=True)

        self.scroll_lista = tk.Scrollbar(result_frame, orient="vertical")
        self.lista_clientes = tk.Listbox(result_frame, font=("Segoe UI", 9), height=4, relief="flat", 
                                         yscrollcommand=self.scroll_lista.set, bg=self.bg_card, fg=self.cor_texto,
                                         selectbackground=self.cinza_selecao, selectforeground="black", 
                                         borderwidth=0, highlightthickness=0)
        self.scroll_lista.config(command=self.lista_clientes.yview)
        
        self.lista_clientes.pack(side="left", fill="both", expand=True)
        self.scroll_lista.pack(side="right", fill="y")
        self.lista_clientes.bind('<<ListboxSelect>>', self.selecionar_cliente_lista)

        # --- CORPO PRINCIPAL ---
        corpo_frame = tk.Frame(self, bg=self.bg_fundo)
        corpo_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # ESQUERDA: CARDÁPIO
        prod_container = tk.LabelFrame(corpo_frame, text=" CARDÁPIO DE PRODUTOS ", bg=self.bg_fundo, fg=self.cinza_escuro, font=("Segoe UI", 10, "bold"), padx=10, pady=10)
        prod_container.pack(side="left", fill="both", expand=True, padx=(0, 10))

        canvas = tk.Canvas(prod_container, bg=self.bg_fundo, highlightthickness=0)
        scrollbar = ttk.Scrollbar(prod_container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg=self.bg_fundo)

        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.carregar_produtos_grade()

        # DIREITA: RESUMO DO PEDIDO
        resumo_frame = tk.Frame(corpo_frame, bg=self.bg_card, highlightbackground=self.cor_borda, highlightthickness=1)
        resumo_frame.pack(side="right", fill="both", padx=10)

        # Label de Confirmação (Tons de Cinza)
        self.lbl_cliente_topo = tk.Label(resumo_frame, text="SELECIONE UM CLIENTE", bg=self.cinza_selecao, fg=self.cinza_escuro, 
                                         font=("Segoe UI", 10, "bold"), pady=8)
        self.lbl_cliente_topo.pack(fill="x", padx=10, pady=(10, 5))

        tk.Label(resumo_frame, text="ITENS NO CARRINHO", bg=self.bg_card, fg=self.cinza_medio, font=("Segoe UI", 9, "bold")).pack(pady=5)

        self.tree = ttk.Treeview(resumo_frame, columns=("Prod", "Preco"), show="headings", height=12)
        self.tree.heading("Prod", text="Produto")
        self.tree.heading("Preco", text="Preço")
        self.tree.column("Prod", width=160)
        self.tree.column("Preco", width=80, anchor="center")
        self.tree.pack(fill="x", padx=15, pady=5)

        self.lbl_total = tk.Label(resumo_frame, text="TOTAL: R$ 0.00", bg=self.bg_card, font=("Segoe UI", 16, "bold"), fg=self.cor_texto)
        self.lbl_total.pack(pady=15)

        # --- BOTÕES ---
        btn_remover = tk.Button(resumo_frame, text="REMOVER ITEM", bg=self.cinza_medio, fg="white", 
                                font=("Segoe UI", 9, "bold"), width=28, command=self.remover_item, relief="flat", cursor="hand2")
        btn_remover.pack(pady=5, ipady=5)

        btn_pagar = tk.Button(resumo_frame, text="FINALIZAR E PAGAR", bg=self.cinza_escuro, fg="white", 
                              font=("Segoe UI", 9, "bold"), width=28, command=self.ir_para_pagamento, relief="flat", cursor="hand2")
        btn_pagar.pack(pady=5, ipady=5)

        btn_sair = tk.Button(resumo_frame, text="SAIR SEM SALVAR", bg=self.cinza_claro, fg="white", 
                             font=("Segoe UI", 9, "bold"), width=28, command=self.destroy, relief="flat", cursor="hand2")
        btn_sair.pack(pady=5, ipady=5)

    def carregar_produtos_grade(self):
        try:
            itens = database.listar_itens() 
            col, row = 0, 0
            for item in itens:
                if item[5] == "em estoque":
                    texto = f"{item[1]}\nR$ {item[2]:.2f}"
                    btn = tk.Button(self.scrollable_frame, text=texto, width=16, height=4, bg="white", fg=self.cor_texto, 
                                   relief="flat", highlightbackground=self.cor_borda, highlightthickness=1,
                                   font=("Segoe UI", 8, "bold"), command=lambda i=item: self.adicionar_item(i))
                    btn.grid(row=row, column=col, padx=8, pady=8)
                    col += 1
                    if col > 2: col, row = 0, row + 1
        except Exception as e:
            print(f"Erro ao carregar itens: {e}")

    def buscar_cliente(self):
        termo = self.ent_busca_cliente.get().strip()
        if not termo: return
        self.lista_clientes.delete(0, tk.END)
        self.dados_clientes_lista = []

        conn = database.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nome, telefone, logradouro, numero, bairro 
            FROM clientes 
            WHERE nome LIKE ? OR telefone = ?""", (f'%{termo}%', termo))
        resultados = cursor.fetchall()
        conn.close()

        if resultados:
            for res in resultados:
                linha = f"{res[1].upper()} | {res[2]} | {res[3]}, {res[4]} - {res[5]}"
                self.lista_clientes.insert(tk.END, linha)
                self.dados_clientes_lista.append(res)
            if len(resultados) == 1:
                self.lista_clientes.select_set(0)
                self.selecionar_cliente_lista(None)
        else:
            self.lbl_cliente_topo.config(text="CLIENTE NÃO ENCONTRADO", bg="#f3f4f6", fg=self.cinza_medio)
            messagebox.showwarning("Busca", "Nenhum cliente localizado.")

    def selecionar_cliente_lista(self, event):
        selecao = self.lista_clientes.curselection()
        if selecao:
            indice = selecao[0]
            self.cliente_selecionado = self.dados_clientes_lista[indice]
            
            # Feedback Discreto: Fundo cinza escuro com texto branco no topo do resumo
            info = f"CONFIRMADO: {self.cliente_selecionado[1].upper()}"
            self.lbl_cliente_topo.config(text=info, bg=self.cinza_escuro, fg="white")

    def adicionar_item(self, item):
        if not self.cliente_selecionado:
            messagebox.showwarning("Aviso", "Selecione um cliente para prosseguir.")
            return
            
        self.tree.insert("", "end", values=(item[1], f"{item[2]:.2f}"))
        self.total_pedido += item[2]
        self.lbl_total.config(text=f"TOTAL: R$ {self.total_pedido:.2f}")

    def remover_item(self):
        sel = self.tree.selection()
        if sel:
            for i in sel:
                valor = float(self.tree.item(i)["values"][1])
                self.total_pedido -= valor
                self.tree.delete(i)
            self.lbl_total.config(text=f"TOTAL: R$ {self.total_pedido:.2f}")

    def ir_para_pagamento(self):
        if self.cliente_selecionado and self.tree.get_children():
            messagebox.showinfo("Pedido", f"Pedido confirmado para {self.cliente_selecionado[1]}")
            self.destroy()
        else:
            messagebox.showwarning("Atenção", "Conclua a seleção do cliente e dos produtos.")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    JanelaCadastroPedidos(root)
    root.mainloop()