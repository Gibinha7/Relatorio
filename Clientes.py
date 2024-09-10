from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from APPClientes import Clientes
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


class Cliente:
    def __init__(self, master=None):
        self.master = master
        self.janela21 = Frame(master)
        self.janela21.pack()
        self.msg1 = Label(self.janela21, text="Informe os dados do Cliente:")
        self.msg1["font"] = ("Verdana", "14", "bold")
        self.msg1.pack()

        self.janela22 = Frame(master)
        self.janela22["padx"] = 20
        self.janela22.pack()

        self.idcliente_label = Label(self.janela22, text="ID Cliente:")
        self.idcliente_label.pack(side="left")
        self.idcliente = Entry(self.janela22, width=20)
        self.idcliente.pack(side="left")

        self.busca = Button(self.janela22, text="Buscar", command=self.buscarCliente)
        self.busca.pack()

        self.janela23 = Frame(master)
        self.janela23["padx"] = 20
        self.janela23.pack()

        self.nome_label = Label(self.janela23, text="Nome:")
        self.nome_label.pack(side="left")
        self.nome = Entry(self.janela23, width=30)
        self.nome.pack(side="left")

        self.janela24 = Frame(master)
        self.janela24["padx"] = 20
        self.janela24.pack()

        self.cidade_label = Label(self.janela24, text="Cidade:")
        self.cidade_label.pack(side="left")
        self.cidade_combobox = ttk.Combobox(self.janela24, width=27)
        self.cidade_combobox.pack(side="left")
        self.carregarCidades()

        self.janela25 = Frame(master)
        self.janela25["padx"] = 20
        self.janela25.pack(pady=5)

        self.nascimento_label = Label(self.janela25, text="Nascimento:")
        self.nascimento_label.pack(side="left")
        self.nascimento = Entry(self.janela25, width=28)
        self.nascimento.pack(side="left")

        self.janela26 = Frame(master)
        self.janela26["padx"] = 20
        self.janela26.pack()

        self.cpf_label = Label(self.janela26, text="CPF:")
        self.cpf_label.pack(side="left")
        self.cpf = Entry(self.janela26, width=30)
        self.cpf.pack(side="left")

        self.janela27 = Frame(master)
        self.janela27["padx"] = 20
        self.janela27.pack()

        self.genero_label = Label(self.janela27, text="Gênero:")
        self.genero_label.pack(side="left")
        self.genero = Entry(self.janela27, width=30)
        self.genero.pack(side="left")

        self.janela28 = Frame(master)
        self.janela28["padx"] = 20
        self.janela28.pack()

        self.autentic = Label(self.janela28, text="", font=("Verdana", "10", "italic", "bold"))
        self.autentic.pack()

        self.janela11 = Frame(master)
        self.janela11["padx"] = 20
        self.janela11.pack(pady=5)

        self.botao = Button(self.janela11, width=10, text="Inserir", command=self.inserirCliente)
        self.botao.pack(side="left")

        self.botao2 = Button(self.janela11, width=10, text="Alterar", command=self.alterarCliente)
        self.botao2.pack(side="left")

        self.botao3 = Button(self.janela11, width=10, text="Excluir", command=self.excluirCliente)
        self.botao3.pack(side="left")

        self.janela12 = Frame(master)
        self.janela12["padx"] = 20
        self.janela12.pack(pady=10)

        self.tree = ttk.Treeview(self.janela12, columns=("ID", "Nome", "Nascimento", "CPF", "Gênero", "Cidade"),
                                 show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Nascimento", text="Nascimento")
        self.tree.heading("CPF", text="CPF")
        self.tree.heading("Gênero", text="Gênero")
        self.tree.heading("Cidade", text="Cidade")
        self.tree.pack()

        self.tree.bind("<ButtonRelease-1>", self.selecionarCliente)

        self.atualizarTabela()

        self.janela13 = Frame(master)
        self.janela13["padx"] = 20
        self.janela13.pack(pady=10)

        self.botao4 = Button(self.janela13, width=10, text="Voltar", command=self.voltarmenu)
        self.botao4.pack(side="left")

        # Botão para exportar o PDF
        self.botao_exportar_pdf = Button(self.janela13, width=20, text="Exportar e Salvar PDF", command=self.exportarParaPDF)
        self.botao_exportar_pdf.pack(side="left")

    def carregarCidades(self):
        cli = Clientes()
        cidades = cli.selectCidades()
        self.cidade_combobox['values'] = cidades

    def atualizarTabela(self):
        cli = Clientes()
        clientes = cli.selectAllClientes()
        self.tree.delete(*self.tree.get_children())
        for c in clientes:
            self.tree.insert("", "end", values=(c[0], c[1], c[2], c[3], c[4], c[5]))

    def selecionarCliente(self, event):
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)
            record = item['values']
            self.idcliente.delete(0, END)
            self.idcliente.insert(0, record[0])
            self.nome.delete(0, END)
            self.nome.insert(0, record[1])
            self.nascimento.delete(0, END)
            self.nascimento.insert(0, record[2])
            self.cpf.delete(0, END)
            self.cpf.insert(0, record[3])
            self.genero.delete(0, END)
            self.genero.insert(0, record[4])
            self.cidade_combobox.set(record[5])

    def buscarCliente(self):
        cli = Clientes()
        idcliente = self.idcliente.get()
        self.autentic["text"] = cli.selectCliente(idcliente)
        self.idcliente.delete(0, END)
        self.idcliente.insert(INSERT, cli.idcliente)
        self.nome.delete(0, END)
        self.nome.insert(INSERT, cli.nome)
        self.nascimento.delete(0, END)
        self.nascimento.insert(INSERT, cli.nascimento)
        self.cpf.delete(0, END)
        self.cpf.insert(INSERT, cli.cpf)
        self.genero.delete(0, END)
        self.genero.insert(INSERT, cli.genero)
        self.cidade_combobox.set(cli.cidade)

    def inserirCliente(self):
        cli = Clientes(nome=self.nome.get(), nascimento=self.nascimento.get(), cpf=self.cpf.get(),
                       genero=self.genero.get(), cidade=self.cidade_combobox.get())
        result = cli.insertCliente()
        self.atualizarTabela()
        messagebox.showinfo("Inserir", "Cliente inserido com sucesso!")

    def alterarCliente(self):
        cli = Clientes(idcliente=self.idcliente.get(), nome=self.nome.get(), nascimento=self.nascimento.get(),
                       cpf=self.cpf.get(), genero=self.genero.get(), cidade=self.cidade_combobox.get())
        result = cli.updateCliente()
        messagebox.showinfo("Alterar", "Cliente alterado com sucesso!")
        self.atualizarTabela()

    def excluirCliente(self):
        cli = Clientes(idcliente=self.idcliente.get())
        result = cli.deleteCliente()
        messagebox.showinfo("Excluir", "Cliente excluido com sucesso!")
        self.atualizarTabela()

    def voltarmenu(self):
        self.master.destroy()

    def exportarParaPDF(self):
        # Cria um PDF e o salva no diretório do projeto
        pdf = canvas.Canvas("clientes.pdf", pagesize=letter)
        pdf.setTitle("Lista de Clientes")
        pdf.drawString(100, 750, "Lista de Clientes")
        pdf.drawString(50, 720, "ID")
        pdf.drawString(100, 720, "Nome")
        pdf.drawString(200, 720, "Nascimento")
        pdf.drawString(300, 720, "CPF")
        pdf.drawString(400, 720, "Gênero")
        pdf.drawString(500, 720, "Cidade")

        y = 700
        for item in self.tree.get_children():
            valores = self.tree.item(item, 'values')
            pdf.drawString(50, y, str(valores[0]))
            pdf.drawString(100, y, valores[1])
            pdf.drawString(200, y, valores[2])
            pdf.drawString(300, y, valores[3])
            pdf.drawString(400, y, valores[4])
            pdf.drawString(500, y, valores[5])
            y -= 20
        pdf.save()

        messagebox.showinfo("Exportar PDF", "PDF gerado e salvo com sucesso!")

# Inicializa a aplicação
if __name__ == "__main__":
    root = Tk()
    app = Cliente(master=root)
    root.mainloop()
