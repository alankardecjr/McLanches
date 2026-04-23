import tkinter as tk
from tkinter import messagebox
import sqlite3
import database  # Certifique-se que o arquivo database.py contém as funções do deliveryVS3.db

class JanelaCadastroCliente(tk.Toplevel):
    def __init__(self, master, dados_cliente=None, callback_pedido=None):
        super().__init__(master)
        self.title("Gerenciar Cliente")
        self.geometry("460x720") # Aumentado levemente para acomodar o novo botão
        
        # Paleta de Cores
        self.bg_fundo = "#f4f5f9"
        self.bg_card = "#ffffff"
        self.cor_borda = "#d1d5db"
        self.cor_texto = "#1f2937"
        self.cor_lbl = "#4b5563"
        self.cor_btn_1 = "#374151"   # Salvar e Fechar
        self.cor_btn_2 = "#111827"   # Salvar e Pedir
        self.cor_btn_sair = "#9ca3af" # Sair (Cinza médio)

        self.configure(bg=self.bg_fundo)
        self.cliente_id = None
        self.callback_pedido = callback_pedido 

        self.criar_widgets()

        if dados_cliente:
            self.preencher_dados(dados_cliente)

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

        # --- Campos ---
        self.ent_nome = criar_campo(main_frame, "NOME COMPLETO", 0)
        self.ent_tel = criar_campo(main_frame, "TELEFONE", 2)
        self.ent_logra = criar_campo(main_frame, "LOGRADOURO (Rua/Av)", 4, col=0, colspan=1)
        self.ent_num = criar_campo(main_frame, "Nº", 4, col=1, colspan=1, width=8)
        self.ent_bairro = criar_campo(main_frame, "BAIRRO", 6)
        self.ent_ref = criar_campo(main_frame, "PONTO DE REFERÊNCIA", 8)
        self.txt_obs = criar_campo(main_frame, "OBSERVAÇÕES", 10)

        # --- Status ---
        tk.Label(main_frame, text="STATUS DO CLIENTE", bg=self.bg_fundo, fg=self.cor_lbl, 
                 font=("Segoe UI", 9, "bold")).grid(row=12, column=0, sticky="w", pady=(15, 2))
        
        self.var_status = tk.StringVar(value="Ativo")
        self.opt_status = tk.OptionMenu(main_frame, self.var_status, "Ativo", "Inativo", "VIP", "PCD/Idoso")
        self.opt_status.config(bg=self.bg_card, fg=self.cor_texto, relief="flat", 
                               highlightthickness=1, highlightbackground=self.cor_borda, font=("Segoe UI", 10))
        self.opt_status.grid(row=13, column=0, columnspan=2, sticky="ew")

        # --- Container de Botões ---
        # Frame para os botões superiores (lado a lado)
        btn_top_frame = tk.Frame(main_frame, bg=self.bg_fundo)
        btn_top_frame.grid(row=14, column=0, columnspan=2, pady=(30, 10))

        self.btn_salvar = tk.Button(btn_top_frame, text="SALVAR E FECHAR", bg=self.cor_btn_1, fg="white", 
                                   font=("Segoe UI", 9, "bold"), width=18, relief="flat",
                                   cursor="hand2", command=self.salvar_e_sair)
        self.btn_salvar.pack(side="left", padx=5, ipady=8)

        self.btn_pedido = tk.Button(btn_top_frame, text="SALVAR E PEDIR", bg=self.cor_btn_2, fg="white", 
                                   font=("Segoe UI", 9, "bold"), width=18, relief="flat",
                                   cursor="hand2", command=self.salvar_e_pedir)
        self.btn_pedido.pack(side="left", padx=5, ipady=8)

        # Botão Sair (abaixo e centralizado)
        self.btn_sair_janela = tk.Button(main_frame, text="SAIR SEM SALVAR", bg=self.cor_btn_sair, fg="white", 
                                        font=("Segoe UI", 9, "bold"), width=38, relief="flat",
                                        cursor="hand2", command=self.fechar_limpar)
        self.btn_sair_janela.grid(row=15, column=0, columnspan=2, pady=5, ipady=5)

        main_frame.columnconfigure(0, weight=4)
        main_frame.columnconfigure(1, weight=1)

    def fechar_limpar(self):
        """Fecha a janela e limpa referências para liberar memória"""
        self.grab_release() # Libera o foco se estiver em modo modal
        self.destroy()

    def coletar_dados(self):
        return {
            "nome": self.ent_nome.get().strip(),
            "tel": self.ent_tel.get().strip(),
            "logra": self.ent_logra.get().strip(),
            "num": self.ent_num.get().strip(),
            "bairro": self.ent_bairro.get().strip(),
            "ref": self.ent_ref.get().strip(),
            "obs": self.txt_obs.get().strip(),
            "status": self.var_status.get()
        }

    def validar_e_salvar(self):
        d = self.coletar_dados()
        if not d["nome"] or not d["tel"] or not d["logra"]:
            messagebox.showwarning("Atenção", "Preencha Nome, Telefone e Logradouro.")
            return False
        
        try:
            if self.cliente_id:
                database.atualizar_cliente(self.cliente_id, d["nome"], d["tel"], d["logra"], 
                                          d["num"], d["bairro"], d["ref"], d["obs"], d["status"])
            else:
                database.salvar_cliente(d["nome"], d["tel"], d["logra"], d["num"], 
                                       d["bairro"], d["ref"], d["obs"], d["status"])
            return True
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Telefone já cadastrado.")
            return False

    def salvar_e_sair(self):
        if self.validar_e_salvar():
            self.fechar_limpar()

    def salvar_e_pedir(self):
        nome_cliente = self.ent_nome.get().strip()
        if self.validar_e_salvar():
            self.fechar_limpar()
            if self.callback_pedido:
                self.callback_pedido(nome_cliente)

    def preencher_dados(self, dados):
        self.cliente_id = dados[0]
        self.ent_nome.insert(0, dados[1])
        self.ent_tel.insert(0, dados[2])
        self.ent_logra.insert(0, dados[3])
        self.ent_num.insert(0, dados[4])
        self.ent_bairro.insert(0, dados[5])
        self.ent_ref.insert(0, dados[6])
        self.txt_obs.insert(0, dados[7])
        self.var_status.set(dados[8])
        self.btn_salvar.config(text="ATUALIZAR DADOS")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw() 
    JanelaCadastro(root)
    root.mainloop()