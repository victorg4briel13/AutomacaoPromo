import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
import tkinter as tk
from cappromo import gerar_card

class ProductForm(tb.Window):
    def __init__(self):
        super().__init__(themename="darkly")  # Você pode trocar o tema (ex: 'darkly', 'cyborg', 'superhero', 'journal', etc.)
        self.title("Automação Promo")
        self.geometry("500x620")
        self.resizable(False, False)

        self.frete_gratis_var = tb.BooleanVar()
        self.tem_cupom_var = tb.BooleanVar()

        self._create_widgets()

    def _create_widgets(self):
        container = tb.Frame(self, padding=20)
        container.pack(fill=BOTH, expand=True)

        tb.Label(container, text="Automação Promo", font=("Helvetica", 20, "bold")).pack(pady=(0, 20))

        # Nome
        self.nome_entry = self._add_labeled_entry(container, "Nome do Produto:")

        # Descrição
        tb.Label(container, text="Descrição (máx. 50 caracteres):").pack(anchor=W)
        self.descricao_text = tk.Text(container, height=3, font=("Helvetica", 10))
        self.descricao_text.pack(fill=X, pady=(0, 10))
        self.descricao_text.bind("<KeyRelease>", self._check_description_length)

        # Preço
        self.preco_entry = self._add_labeled_entry(container, "Preço (R$):")

        # Checkbuttons
        tb.Checkbutton(container, text="Frete Grátis", variable=self.frete_gratis_var, bootstyle="info").pack(anchor=W, pady=(10, 2))
        tb.Checkbutton(container, text="Tem Cupom", variable=self.tem_cupom_var, bootstyle="info").pack(anchor=W, pady=(0, 10))

        # Cupom
        self.cupom_entry = self._add_labeled_entry(container, "Cupom:")

        # Seleção de Imagem
        tb.Label(container, text="Imagem do Produto:").pack(anchor=W)
        img_frame = tb.Frame(container)
        img_frame.pack(fill=X, pady=(0, 10))
        self.imagem_entry = tb.Entry(img_frame, state="readonly")
        self.imagem_entry.pack(side=LEFT, fill=X, expand=True)
        tb.Button(img_frame, text="Selecionar", bootstyle="secondary", command=self._selecionar_imagem).pack(side=RIGHT, padx=5)

        # Botão Salvar
        tb.Button(container, text="Salvar Produto", bootstyle="primary outline", command=self._salvar_dados).pack(pady=20, ipadx=10, ipady=5)

    def _add_labeled_entry(self, parent, label):
        tb.Label(parent, text=label).pack(anchor=W)
        entry = tb.Entry(parent)
        entry.pack(fill=X, pady=(0, 10))
        return entry

    def _check_description_length(self, event=None):
        content = self.descricao_text.get("1.0", "end-1c")
        if len(content) > 50:
            messagebox.showwarning("Limite de caracteres", "A descrição deve ter no máximo 50 caracteres.")
            self.descricao_text.delete("end-2c")

    def _selecionar_imagem(self):
        filepath = filedialog.askopenfilename(
            title="Selecione uma imagem",
            filetypes=(("Imagens", "*.png;*.jpg;*.jpeg"), ("Todos os Arquivos", "*.*"))
        )
        if filepath:
            self.imagem_entry.config(state="normal")
            self.imagem_entry.delete(0, tk.END)
            self.imagem_entry.insert(0, filepath)
            self.imagem_entry.config(state="readonly")

    def _salvar_dados(self):
        try:
            nome = self.nome_entry.get()
            descricao = self.descricao_text.get("1.0", "end-1c")
            preco = self.preco_entry.get()
            frete_gratis = self.frete_gratis_var.get()
            tem_cupom = self.tem_cupom_var.get()
            cupom = self.cupom_entry.get()
            imagem = self.imagem_entry.get()

            if not nome or not descricao or not self.preco_entry.get():
                messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos obrigatórios.")
                return

            print("==== Produto Cadastrado ====")
            print(f"Nome: {nome}")
            print(f"Descrição: {descricao}")
            print(f"Preço: R${preco}")
            print(f"Frete Grátis: {'Sim' if frete_gratis else 'Não'}")
            print(f"Tem Cupom: {'Sim' if tem_cupom else 'Não'}")
            print(f"Cupom: {cupom or 'N/A'}")
            print(f"Imagem: {imagem or 'N/A'}")
            print("============================")

            messagebox.showinfo("Sucesso", "Anúncio criado com sucesso!")

            gerar_card(
                nome=nome,
                descricao=descricao,
                preco=preco,
                frete_gratis=frete_gratis,
                temcupom=tem_cupom,
                cupom=cupom,
                imagem_produto_path=imagem,
                imagem_moldura_path=r"D:\Capitão promo\Automação promo\Modelos\moldura post instagram capitão promo.png",
                imagem_moldura_frete_path=r"D:\Capitão promo\Automação promo\Modelos\moldura post instagram capitão promo frete gratis.png"
            )

        except ValueError:
            messagebox.showerror("Erro", "O preço deve ser um número válido.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {e}")

if __name__ == "__main__":
    app = ProductForm()
    app.mainloop()
