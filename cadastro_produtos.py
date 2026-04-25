import tkinter as tk
from tkinter import messagebox
import sqlite3
import database  # Referenciando seu databaseVs4.db

class JanelaCadastroProduto(tk.Toplevel):
    def __init__(self, master, dados_produto=None):
        super().__init__(master)
        self.title("Gerenciar Produtos")
        self.geometry("460x600")
        
        # Paleta de Cores
        self.bg_fundo = "#f4f5f9"
        self.bg_card = "#ffffff"
        self.cor_borda = "#d1d5db"
        self.cor_texto = "#1f2937"
        self.cor_lbl = "#4b5563"
        self.cor_btn_1 = "#374151"   
        self.cor_btn_sair = "#9ca3af" 

        self.configure(bg=self.bg_fundo)
        self.produto_id = None

        self.criar_widgets()

        if dados_produto:
            self.preencher_dados(dados_produto)

    def criar_widgets(self):
        main_frame = tk.Frame(self, bg=self.bg_fundo, padx=25, pady=20)
        main_frame.pack(fill="both", expand=True)

        def criar_campo(parent, texto, row, col=0, colspan=2, width=None):
            tk.Label(parent, text=texto, bg=self.bg_fundo, fg=self.cor_lbl, 
                     font=("Segoe UI", 9, "bold")).grid(row=row, column=col, sticky="w", pady=(12, 2))
            
            ent = tk.Entry(parent, font=("Segoe UI", 11), bg=self.bg_card, fg=self.cor_texto,
                           relief="flat", highlightbackground=self.cor_borda, highlightthickness=1)
            
            if width: ent.config(width=width)
            ent.grid(row=row+1, column=col, columnspan=colspan, sticky="ew", ipady=5, padx=(0, 5) if colspan==1 else 0)
            
            ent.bind("<FocusIn>", lambda e: e.widget.config(highlightbackground="#3b82f6"))
            ent.bind("<FocusOut>", lambda e: e.widget.config(highlightbackground=self.cor_borda))
            return ent

        # --- Nome do Produto ---
        self.ent_produto = criar_campo(main_frame, "NOME DO PRODUTO / ITEM", 0)

        # --- Categoria (Substituído Entry por OptionMenu) ---
        tk.Label(main_frame, text="CATEGORIA", bg=self.bg_fundo, fg=self.cor_lbl, 
                 font=("Segoe UI", 9, "bold")).grid(row=2, column=0, sticky="w", pady=(12, 2))
        
        self.var_categoria = tk.StringVar(value="Lanche")
        self.opt_categoria = tk.OptionMenu(main_frame, self.var_categoria, "Lanche", "Bebida", "Sobremesa")
        self.opt_categoria.config(bg=self.bg_card, fg=self.cor_texto, relief="flat", 
                                  highlightthickness=1, highlightbackground=self.cor_borda, font=("Segoe UI", 10))
        self.opt_categoria.grid(row=3, column=0, columnspan=2, sticky="ew")

        # --- Preço e Quantidade ---
        self.ent_preco = criar_campo(main_frame, "PREÇO (R$)", 4, col=0, colspan=1)
        self.ent_qtd = criar_campo(main_frame, "QUANTIDADE EM ESTOQUE", 4, col=1, colspan=1)

        # --- Status do Produto ---
        tk.Label(main_frame, text="STATUS DO ESTOQUE", bg=self.bg_fundo, fg=self.cor_lbl, 
                 font=("Segoe UI", 9, "bold")).grid(row=6, column=0, sticky="w", pady=(15, 2))
        
        self.var_status = tk.StringVar(value="em estoque")
        self.opt_status = tk.OptionMenu(main_frame, self.var_status, "em estoque", "em falta")
        self.opt_status.config(bg=self.bg_card, fg=self.cor_texto, relief="flat", 
                               highlightthickness=1, highlightbackground=self.cor_borda, font=("Segoe UI", 10))
        self.opt_status.grid(row=7, column=0, columnspan=2, sticky="ew")

        # --- Botões ---
        btn_frame = tk.Frame(main_frame, bg=self.bg_fundo)
        btn_frame.grid(row=8, column=0, columnspan=2, pady=(40, 10))

        self.btn_salvar = tk.Button(btn_frame, text="SALVAR", bg=self.cor_btn_1, fg="white", 
                                   font=("Segoe UI", 10, "bold"), width=35, relief="flat",
                                   cursor="hand2", command=self.salvar)
        self.btn_salvar.pack(pady=5, ipady=8)

        self.btn_sair = tk.Button(main_frame, text="SAIR", bg=self.cor_btn_sair, fg="white", 
                                 font=("Segoe UI", 9, "bold"), width=38, relief="flat",
                                 cursor="hand2", command=self.destroy)
        self.btn_sair.grid(row=9, column=0, columnspan=2, pady=5, ipady=5)

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

    def coletar_dados(self):
        return {
            "produto": self.ent_produto.get().strip(),
            "preco": self.ent_preco.get().replace(',', '.').strip(),
            "quantidade": self.ent_qtd.get().strip(),
            "categoria": self.var_categoria.get(),
            "status": self.var_status.get()
        }

    def salvar(self):
        d = self.coletar_dados()
        
        # Validação básica
        if not d["produto"] or not d["preco"]:
            messagebox.showwarning("Atenção", "Nome e Preço são obrigatórios.")
            return

        try:
            # Conversão de tipos para evitar erros no banco
            preco_float = float(d["preco"])
            qtd_int = int(d["quantidade"]) if d["quantidade"] else 0
            
            # LÓGICA DE ALTERAÇÃO:
            if self.produto_id:
                # Se o ID existe, chamamos a função de ATUALIZAR
                database.atualizar_item(
                    self.produto_id, 
                    d["produto"], 
                    preco_float, 
                    qtd_int, 
                    d["categoria"], 
                    d["status"]
                )
                messagebox.showinfo("Sucesso", f"Produto '{d['produto']}' salvo com sucesso!")
            else:
                # Se o ID não existe, chamamos a função de SALVAR NOVO
                database.salvar_item(
                    d["produto"], 
                    preco_float, 
                    qtd_int, 
                    d["categoria"], 
                    d["status"]
                )
                messagebox.showinfo("Sucesso", f"Produto '{d['produto']}' cadastrado com sucesso!")
            
            # Fecha a janela para que a tela principal possa atualizar a lista
            self.destroy()

        except ValueError:
            messagebox.showerror("Erro", "Preço e Quantidade devem ser números válidos.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Este produto já está cadastrado (conflito de integridade).")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro inesperado: {e}")

    def preencher_dados(self, dados):
        """Preenche para edição (id, produto, preco, quantidade, categoria, status)"""
        self.produto_id = dados[0]
        self.ent_produto.insert(0, dados[1])
        self.ent_preco.insert(0, str(dados[2]))
        self.ent_qtd.insert(0, str(dados[3]))
        self.var_categoria.set(dados[4])
        self.var_status.set(dados[5])
        self.btn_salvar.config(text="ATUALIZAR")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    JanelaCadastroProduto(root)
    root.mainloop()