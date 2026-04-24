import tkinter as tk
from tkinter import messagebox, ttk
import database  
from cadastro_cliente import JanelaCadastroCliente
from cadastro_produtos import JanelaCadastroProduto
from cadastro_pedidos import JanelaCadastroPedidos

# Para simplificar, as janelas de cadastro foram unificadas em JanelaCadastro e JanelaPedido
class SistemaJAD:
    def __init__(self, root):
        self.root = root
        self.root.title("***** Sistema JAD - SQLite *****")
        self.root.geometry("1100x700")
        self.root.configure(bg="#f4f6f9")
        
        self.modo_atual = "clientes" 
        self.setup_ui()
        
        # Tags de Cores e Estilo 
        self.tree.tag_configure('inativo', background="#e0e0e0", foreground='#424242', font=('Arial', 9, 'bold', 'italic', 'overstrike'))
        self.tree.tag_configure('finalizado', background="#bdc3c7", foreground='white', font=('Arial', 9, 'bold', 'italic', 'overstrike')) 
        self.tree.tag_configure('prioridade', foreground="#2c3e50", font=('Arial', 11, 'bold', 'italic'))
        
        self.exibir_clientes()

    def setup_ui(self):
        tk.Label(self.root, text="--- McLanches Delivery ---", 
                 font=("Arial", 18, "bold"), bg="#f4f6f9", fg="#333").pack(pady=15)

        # Busca
        frame_busca = tk.Frame(self.root, bg="#f4f6f9")
        frame_busca.pack(fill="x", padx=40, pady=5)
        
        tk.Label(frame_busca, text="Buscar:", bg="#f4f6f9", font=("Arial", 10, "bold")).pack(side="left")
        self.ent_busca = tk.Entry(frame_busca, font=("Arial", 11), relief="flat", highlightthickness=1, highlightbackground="#ccc")
        self.ent_busca.pack(side="left", padx=10, fill="x", expand=True)
        self.ent_busca.bind("<KeyRelease>", self.filtrar_dados) 

        # Menu de Botões
        frame_menu = tk.Frame(self.root, bg="#f4f6f9")
        frame_menu.pack(pady=15)
        
        btn_style = {
            "width": 15, "height": 2, "bg": "#f4f6f9", "fg": "black", 
            "font": ("Arial", 9, "bold"), "relief": "flat",
            "highlightthickness": 1, "highlightbackground": "#d1d1d1", "cursor": "hand2"
        }

        botoes = [
            ("Gerar Pedido", self.abrir_pedido),
            ("Novo Cliente", self.abrir_cadastro),
            ("Ver Clientes", self.exibir_clientes),
            ("Ver Produtos", self.editar_produtos),
            ("Ver Pedidos", self.exibir_pedidos),
            ("Sair", self.confirmar_saida)
        ]

        for i, (texto, comando) in enumerate(botoes):
            btn = tk.Button(frame_menu, text=texto, command=comando, **btn_style)
            btn.grid(row=0, column=i, padx=5)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#e2e6ea"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#f4f6f9"))

        # Tabela (Treeview)
        self.tree_frame = tk.Frame(self.root, bg="white")
        self.tree_frame.pack(fill="both", expand=True, padx=40, pady=5)

        self.tree = ttk.Treeview(self.tree_frame, selectmode="browse", show="headings")
        self.tree.pack(side="left", fill="both", expand=True)
        
        # Vincular DUPLO CLIQUE para editar
        self.tree.bind("<Double-1>", lambda e: self.editar_selecionado())
        
        scrol = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        scrol.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrol.set)

        self.lbl_total = tk.Label(self.root, text="", font=("Arial", 11, "bold"), bg="#f4f6f9", fg="#2c3e50")
        self.lbl_total.pack(pady=10)

    def preparar_colunas(self, colunas):
        """Reconfigura as colunas da Treeview"""
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = colunas
        for col in colunas:
            header = col.replace("_", " ").title()
            self.tree.heading(col, text=header, anchor="center")
            self.tree.column(col, width=150, anchor="center")
        self.tree.column(colunas[0], width=50) 

    def exibir_clientes(self):
        self.modo_atual = "clientes"
        self.lbl_total.config(text="")
        self.preparar_colunas(("id", "nome", "telefone", "endereco", "status"))
        
        dados = sorted(database.listar_clientes(), key=lambda x: str(x[1]).lower())
        for c in dados:
            endereco = f"{c[3]}, {c[4]} - {c[5]}".strip().replace(" ,", "")
            status = str(c[8])
            tag = "inativo" if status == "Inativo" else "prioridade" if status in ["Idoso", "PCD", "PCD/Idoso"] else ""
            self.tree.insert("", "end", values=(c[0], c[1], c[2], endereco, status), tags=(tag,))

    def exibir_pedidos(self):
        self.modo_atual = "pedidos"
        # Ajustado para incluir as colunas de status específicas
        self.preparar_colunas(("id", "cliente", "valor", "data", "status_pedido"))
        
        dados = sorted(database.listar_pedidos(), key=lambda x: str(x[1]).lower())
        total = 0
        for p in dados:
            try: total += float(p[2])
            except: pass
            
            # Tag baseada no status do pedido (p[4])
            tag = "finalizado" if p[4] == "Finalizado" else ""
            self.tree.insert("", "end", values=p, tags=(tag,))
            
        self.lbl_total.config(text=f"Total em Vendas: R$ {total:.2f}")

    def editar_produtos(self):
        self.modo_atual = "produtos"
        self.lbl_total.config(text="")
        self.preparar_colunas(("id", "produto", "preco", "quantidade", "categoria", "status_item"))
        
        dados = sorted(database.listar_itens(), key=lambda x: str(x[1]).lower())
        for item in dados:
            tag = "inativo" if item[5] == "Fora de estoque" else ""
            self.tree.insert("", "end", values=item, tags=(tag,))

    def editar_selecionado(self):
        item = self.tree.selection()
        if not item: return
        
        dados = self.tree.item(item)["values"]
        
        if self.modo_atual == "clientes":
            janela = JanelaCadastroCliente(self.root, dados_cliente=dados, callback_pedido=self.abrir_pedido)
            self.root.wait_window(janela)
            self.exibir_clientes()
        elif self.modo_atual == "produtos":
            janela = JanelaCadastroProduto(self.root, dados_produto=dados)
            self.root.wait_window(janela)
            self.editar_produtos()
        else:
            # Ao clicar duas vezes no pedido, abre a janela de pedidos/edição
            janela = JanelaCadastroPedidos(self.root) 
            if hasattr(janela, 'top'): self.root.wait_window(janela.top)
            self.exibir_pedidos()

    def filtrar_dados(self, event):
        termo = self.ent_busca.get().lower()
        self.tree.delete(*self.tree.get_children())
        
        if self.modo_atual == "clientes":
            dados_raw = database.listar_clientes()
        elif self.modo_atual == "produtos":
            dados_raw = database.listar_itens()
        else:
            dados_raw = database.listar_pedidos()
        
        dados = sorted(dados_raw, key=lambda x: str(x[1]).lower())

        for d in dados:
            if termo in str(d[1]).lower() or termo in str(d[2]).lower():
                if self.modo_atual == "clientes":
                    endereco = f"{d[3]}, {d[4]} - {d[5]}".strip().replace(" ,", "")
                    status = str(d[8])
                    tag = "inativo" if status == "Inativo" else "prioridade" if status in ["Idoso", "PCD", "PCD/Idoso"] else ""
                    self.tree.insert("", "end", values=(d[0], d[1], d[2], endereco, status), tags=(tag,))
                elif self.modo_atual == "produtos":
                    status = str(d[5])
                    tag = "inativo" if status == "sem estoque" else ""
                    self.tree.insert("", "end", values=d, tags=(tag,))
                else:
                    status = str(d[4])
                    tag = "finalizado" if status == "Finalizado" else ""
                    self.tree.insert("", "end", values=d, tags=(tag,))

    def abrir_cadastro(self):
        JanelaCadastroCliente(self.root, callback_pedido=self.abrir_pedido)
        self.exibir_clientes()

    def abrir_pedido(self, nome_cliente=None):
        janela = JanelaCadastroPedidos(self.root, nome_cliente_inicial=nome_cliente)
        if hasattr(janela, 'top'): self.root.wait_window(janela.top)
        self.exibir_pedidos()

    def confirmar_saida(self):
        if messagebox.askyesno("Sair", "Deseja encerrar o sistema?"): self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaJAD(root)
    root.mainloop()