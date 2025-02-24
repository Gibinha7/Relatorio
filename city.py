from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from Banco import Banco
from APPCidades import Cidades


class Cidade:
    def __init__(self, master=None):
        self.master = master
        self.janela21 = Frame(master)
        self.janela21.pack()
        self.msg1 = Label(self.janela21, text="Informe os dados:")
        self.msg1["font"] = ("Verdana", "14", "bold")
        self.msg1.pack()

        self.janela22 = Frame(master)
        self.janela22["padx"] = 20
        self.janela22.pack()

        self.idcidade_label = Label(self.janela22, text="Id cidade:")
        self.idcidade_label.pack(side="left")
        self.idcidade = Entry(self.janela22, width=20)
        self.idcidade.pack(side="left")

        self.busca = Button(self.janela22, text="Buscar", command=self.buscarCidade)
        self.busca.pack()

        self.janela23 = Frame(master)
        self.janela23["padx"] = 20
        self.janela23.pack()

        self.cidade_label = Label(self.janela23, text="Cidade:")
        self.cidade_label.pack(side="left")
        self.cidade = Entry(self.janela23, width=30)
        self.cidade.pack(side="left")

        self.janela24 = Frame(master)
        self.janela24["padx"] = 20
        self.janela24.pack(pady=5)

        self.uf_label = Label(self.janela24, text="UF:")
        self.uf_label.pack(side="left")
        self.uf = Entry(self.janela24, width=28)
        self.uf.pack(side="left")

        self.janela25 = Frame(master)
        self.janela25["padx"] = 20
        self.janela25.pack()

        self.autentic = Label(self.janela25, text="", font=("Verdana", "10", "italic", "bold"))
        self.autentic.pack()

        # Adicionando os botões para Inserir, Alterar e Excluir
        self.janela11 = Frame(master)
        self.janela11["padx"] = 20
        self.janela11.pack(pady=5)

        self.botao = Button(self.janela11, width=10, text="Inserir", command=self.inserirCidade)
        self.botao.pack(side="left")

        self.botao2 = Button(self.janela11, width=10, text="Alterar", command=self.alterarCidade)
        self.botao2.pack(side="left")

        self.botao3 = Button(self.janela11, width=10, text="Excluir", command=self.excluirCidade)
        self.botao3.pack(side="left")

        # Botão para exportar os dados para PDF
        self.botao5 = Button(self.janela11, width=10, text="Exportar PDF", command=self.exportarPDF)
        self.botao5.pack(side="left")

        # Frame para a tabela
        self.janela12 = Frame(master)
        self.janela12["padx"] = 20
        self.janela12.pack(pady=10)

        self.tree = ttk.Treeview(self.janela12, columns=("ID", "Cidade", "UF"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Cidade", text="Cidade")
        self.tree.heading("UF", text="UF")
        self.tree.pack()

        # Vincula o clique na linha da tabela à função de preencher os campos
        self.tree.bind("<ButtonRelease-1>", self.selecionar_linha)

        # Atualiza a tabela quando a aplicação é carregada
        self.atualizarTabela()

        self.janela13 = Frame(master)
        self.janela13["padx"] = 20
        self.janela13.pack(pady=10)

        self.botao4 = Button(self.janela13, width=10, text="Voltar", command=self.voltarmenu)
        self.botao4.pack(side="left")

    def atualizarTabela(self):
        cid = Cidades()
        cidades = cid.selectAllCidades()
        self.tree.delete(*self.tree.get_children())
        for c in cidades:
            self.tree.insert("", "end", values=(c[0], c[1], c[2]))

    def buscarCidade(self):
        cid = Cidades()
        idcidade = self.idcidade.get()
        self.autentic["text"] = cid.selectCidade(idcidade)
        self.idcidade.delete(0, END)
        self.idcidade.insert(INSERT, cid.idcidade)
        self.cidade.delete(0, END)
        self.cidade.insert(INSERT, cid.cidade)
        self.uf.delete(0, END)
        self.uf.insert(INSERT, cid.uf)

    def inserirCidade(self):
        cid = Cidades(cidade=self.cidade.get(), uf=self.uf.get())
        result = cid.insertCidade()
        self.autentic["text"] = result
        self.atualizarTabela()
        messagebox.showinfo("Inserir", "Cidade inserido com sucesso!")

    def alterarCidade(self):
        cid = Cidades(idcidade=self.idcidade.get(), cidade=self.cidade.get(), uf=self.uf.get())
        result = cid.updateCidade()
        messagebox.showinfo("Alterar", "Cidade alterado com sucesso!")
        self.atualizarTabela()

    def excluirCidade(self):
        cidade = self.cidade.get()

        banco = Banco()
        cursor = banco.conexao.cursor()

        cursor.execute("SELECT * FROM tbl_clientes WHERE cidade=? ", (cidade,))
        engual = cursor.fetchone()

        if engual:
            cid = Cidades(idcidade=self.idcidade.get())
            result = cid.deleteCidade()
            messagebox.showinfo("Excluir", "Cidade excluída com sucesso!")
            self.atualizarTabela()
        else:
            messagebox.showerror("Erro", "Cidade não pode ser excluída!")
        cursor.close()

    def selecionar_linha(self, event):
        # Pega o item selecionado
        item_selecionado = self.tree.selection()
        if item_selecionado:
            valores = self.tree.item(item_selecionado[0], 'values')
            # Preenche os campos de entrada com os valores da linha selecionada
            self.idcidade.delete(0, END)
            self.idcidade.insert(END, valores[0])
            self.cidade.delete(0, END)
            self.cidade.insert(END, valores[1])
            self.uf.delete(0, END)
            self.uf.insert(END, valores[2])

    def voltarmenu(self):
        self.master.destroy()

    def exportarPDF(self):
        # Cria um canvas para o PDF
        c = canvas.Canvas("cidades.pdf", pagesize=letter)
        width, height = letter

        # Define a posição inicial
        x = 50
        y = height - 50

        # Adiciona o título
        c.setFont("Helvetica-Bold", 14)
        c.drawString(x, y, "Dados das Cidades")
        y -= 30

        # Adiciona o cabeçalho
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x, y, "ID")
        c.drawString(x + 100, y, "Cidade")
        c.drawString(x + 300, y, "UF")
        y -= 20

        # Adiciona os dados do Treeview
        c.setFont("Helvetica", 12)
        for item in self.tree.get_children():
            values = self.tree.item(item, 'values')
            c.drawString(x, y, str(values[0]))
            c.drawString(x + 100, y, values[1])
            c.drawString(x + 300, y, values[2])
            y -= 20

        # Salva o PDF
        c.save()
        messagebox.showinfo("Exportar PDF", "Dados exportados com sucesso para 'cidades.pdf'!")


if __name__ == "__main__":
    root = Tk()
    app = Cidade(master=root)
    root.mainloop()
