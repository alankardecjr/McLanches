import tkinter as tk
from tkinter import messagebox
import sqlite3
import database 

class JanelaCadastroCliente(tk.Toplevel):
    def __init__(self, master, dados_cliente=None, callback_pedido=None):
        super().__init__(master)
        self.title("McLanches Delivery")
        self.geometry("460x720") 
        self.resizable(False, False)
        
        # Paleta de Cores
        self.bg_fundo = "#f4f5f9"
        self.bg_card = "#ffffff"
        self.cor_borda = "#d1d5db"
        self.cor_texto = "#1f2937"
        self.cor_lbl = "#4b5563"
        self.cor_btn_1 = "#4b5563"   
        self.cor_btn_2 = "#374151"   
        self.cor_btn_sair = "#1f2937" 
        self.cor_hover = "#3b82f6"   # Azul para destaque de borda
        self.cor_hover_btn = "#6b7280" # Cinza claro para hover de botão

        self.configure(bg=self.bg_fundo)
        self.cliente_id = None
        self.callback_pedido = callback_pedido 

        self.criar_widgets()
        
        if dados_cliente:
            self.preencher_dados(dados_cliente)            
     
        self.grab_set()

    def criar_widgets(self):
        main_frame = tk.Frame(self, bg=self.bg_fundo, padx=25, pady=20)
        main_frame.pack(fill="both", expand=True)

        # --- FUNÇÕES DE EFEITO (HOVER) ---
        def ao_entrar_botao(e, cor_destaque):
            e.widget.config(bg=cor_destaque)

        def ao_sair_botao(e, cor_original):
            e.widget.config(bg=cor_original)

        def criar_campo(parent, texto, row, col=0, colspan=2, width=None):
            tk.Label(parent, text=texto, bg=self.bg_fundo, fg=self.cor_lbl, 
                     font=("Segoe UI", 9, "bold")).grid(row=row, column=col, sticky="w", pady=(12, 2))
            
            ent = tk.Entry(parent, font=("Segoe UI", 11), bg=self.bg_card, fg=self.cor_texto,
                            relief="flat", highlightbackground=self.cor_borda, highlightthickness=1)
            
            if width: ent.config(width=width)
            ent.grid(row=row+1, column=col, columnspan=colspan, sticky="ew", ipady=5, padx=(0, 5) if colspan==1 else 0)
            
            # --- DESTAQUE NO CAMPO DE TEXTO ---
            # Muda para azul ao entrar ou focar, volta ao cinza ao sair
            ent.bind("<Enter>", lambda e: e.widget.config(highlightbackground="#9ca3af") if e.widget != self.focus_get() else None)
            ent.bind("<Leave>", lambda e: e.widget.config(highlightbackground=self.cor_borda) if e.widget != self.focus_get() else None)
            ent.bind("<FocusIn>", lambda e: e.widget.config(highlightbackground=self.cor_hover, highlightthickness=2))
            ent.bind("<FocusOut>", lambda e: e.widget.config(highlightbackground=self.cor_borda, highlightthickness=1))
            
            return ent

        # --- HEADER ---
        lbl_header = tk.Label(main_frame, text="Gerenciar Cliente", bg=self.bg_fundo, 
                               fg=self.cor_texto, font=("Segoe UI", 16, "bold"))
        lbl_header.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        # --- CAMPOS ---
        self.ent_nome = criar_campo(main_frame, "NOME COMPLETO", 1)
        self.ent_tel = criar_campo(main_frame, "TELEFONE", 3)
        self.ent_logra = criar_campo(main_frame, "LOGRADOURO (Rua/Av)", 5, col=0, colspan=1)
        self.ent_num = criar_campo(main_frame, "Nº", 5, col=1, colspan=1, width=8)
        self.ent_bairro = criar_campo(main_frame, "BAIRRO", 7)
        self.ent_ref = criar_campo(main_frame, "PONTO DE REFERÊNCIA", 9)
        self.txt_obs = criar_campo(main_frame, "OBSERVAÇÕES", 11)

        # --- STATUS ---
        tk.Label(main_frame, text="STATUS DO CLIENTE", bg=self.bg_fundo, fg=self.cor_lbl, 
                 font=("Segoe UI", 9, "bold")).grid(row=13, column=0, sticky="w", pady=(15, 2))
        
        self.var_status = tk.StringVar(value="Ativo")
        self.opt_status = tk.OptionMenu(main_frame, self.var_status, "Ativo", "Inativo", "Vip", "PDC/IDOSO")
        self.opt_status.config(bg=self.bg_card, fg=self.cor_texto, relief="flat", highlightthickness=1, 
                                highlightbackground=self.cor_borda, font=("Segoe UI", 10), cursor="hand2")
        self.opt_status.grid(row=14, column=0, columnspan=2, sticky="ew")

        # --- BOTÕES ---
        btn_frame = tk.Frame(main_frame, bg=self.bg_fundo)
        btn_frame.grid(row=15, column=0, columnspan=2, pady=(30, 5))

        # Botão SALVAR
        self.btn_salvar = tk.Button(btn_frame, text="SALVAR", bg=self.cor_btn_1, fg="white", 
                                    font=("Segoe UI", 9, "bold"), width=18, relief="flat", cursor="hand2", 
                                    command=self.salvar_e_sair)
        self.btn_salvar.pack(side="left", padx=5, ipady=8)
        self.btn_salvar.bind("<Enter>", lambda e: ao_entrar_botao(e, self.cor_hover_btn))
        self.btn_salvar.bind("<Leave>", lambda e: ao_sair_botao(e, self.cor_btn_1))

        # Botão PEDIR
        self.btn_pedido = tk.Button(btn_frame, text="PEDIR", bg=self.cor_btn_2, fg="white", 
                                    font=("Segoe UI", 9, "bold"), width=18, relief="flat", cursor="hand2", 
                                    command=self.salvar_e_pedir)
        self.btn_pedido.pack(side="left", padx=5, ipady=8)
        self.btn_pedido.bind("<Enter>", lambda e: ao_entrar_botao(e, "#4b5563")) # Destaque mais claro
        self.btn_pedido.bind("<Leave>", lambda e: ao_sair_botao(e, self.cor_btn_2))

        # Botão FECHAR
        self.btn_sair_janela = tk.Button(main_frame, text="FECHAR", bg=self.cor_btn_sair, fg="white", 
                                        font=("Segoe UI", 9, "bold"), width=38, relief="flat", cursor="hand2", 
                                        command=self.fechar_limpar)
        self.btn_sair_janela.grid(row=16, column=0, columnspan=2, pady=5, ipady=5)
        self.btn_sair_janela.bind("<Enter>", lambda e: ao_entrar_botao(e, "#374151"))
        self.btn_sair_janela.bind("<Leave>", lambda e: ao_sair_botao(e, self.cor_btn_sair))

        main_frame.columnconfigure(0, weight=4)
        main_frame.columnconfigure(1, weight=1)

    def fechar_limpar(self):
        self.grab_release()
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
        d = self.coletar_dados()
        if self.validar_e_salvar():
            if self.callback_pedido:
                self.callback_pedido(d["nome"], d["tel"])
            self.fechar_limpar()

    def preencher_dados(self, dados):
        self.cliente_id = dados[0]
        self.ent_nome.insert(0, str(dados[1]))
        self.ent_tel.insert(0, str(dados[2]))
        self.ent_logra.insert(0, str(dados[3]))
        self.ent_num.insert(0, str(dados[4]))
        self.ent_bairro.insert(0, str(dados[5]))
        self.ent_ref.insert(0, str(dados[6]))
        self.txt_obs.insert(0, str(dados[7]))
        self.var_status.set(dados[8])
        self.btn_salvar.config(text="ATUALIZAR DADOS")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw() 
    JanelaCadastroCliente(root)
    root.mainloop()