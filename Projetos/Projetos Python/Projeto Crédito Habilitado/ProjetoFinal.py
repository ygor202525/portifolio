import mysql.connector
from PyQt5 import uic, QtWidgets
import sys, os
from PyQt5.QtCore import QTimer


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


conexao = mysql.connector.connect(
    host='127.0.0.1',
    user='dev',
    password='9584',
    database='cadastro_credito'
)


def inserir_dados():
    nome = cadastro.txtNome.text().strip()
    cpf = cadastro.txtCpf.text().strip()
    idade = to_int_safe(cadastro.txtIdade.text().strip())
    renda = to_float_safe(cadastro.txtRenda.text().strip())
    situacao = cadastro.txtAnalise.text().strip()

    cursor = conexao.cursor()
    comando_SQL = 'insert into clientes(nome,cpf,idade,renda,situacao) values(%s,%s,%s,%s,%s)'
    dados = (str(nome), str(cpf), str(idade), str(renda), str(situacao))
    cursor.execute(comando_SQL, dados)
    conexao.commit()

    cadastro.txtNome.setText('')
    cadastro.txtCpf.setText('')
    cadastro.txtIdade.setText('')
    cadastro.txtRenda.setText('')
    cadastro.txtAnalise.setText('')
    cadastro.txtSituacao.setText('Dados foram salvos')

    cadastro._suppress_updates = cadastro.txtSituacao.setText('Dados foram salvos')

    def fim_do_salvamento():
        cadastro._suppress_updates = False
        atualizar_estado_ui()

    QTimer.singleShot(2000, fim_do_salvamento)



def verifica_vazio(widget):
    return bool(widget.text().strip())


def to_float_safe(text):
    try:
        return float(text)
    except Exception:
        return None


def to_int_safe(text):
    try:
        return int(text)
    except Exception:
        return None



def atualizar_estado_ui():
    if getattr(cadastro, '_suppress_updates', False):
        return

    nome = cadastro.txtNome.text().strip()
    cpf = cadastro.txtCpf.text().strip()
    idade = cadastro.txtIdade.text().strip()
    renda = cadastro.txtRenda.text().strip()
    situacao = cadastro.txtAnalise.text().strip()

    idade_val = to_int_safe(idade)
    renda_val = to_float_safe(renda)

    nome_preenchido = (nome != "")
    cpf_limpo = "".join(filter(str.isdigit, cpf))
    idade_preenchido = (idade != "")
    renda_preenchido = (renda != "")
    situacao_preenchido = (situacao != "")

    analise_pronta = (idade_val is not None) and (renda_val is not None)
    todos_preenchidos = (nome_preenchido and cpf_limpo and idade_preenchido and renda_preenchido and situacao_preenchido)
    nenhum_preenchido = (nome == "" and cpf_limpo == "" and idade == "" and renda == "" and situacao == "")

    if analise_pronta:
        cadastro.btnAnalise.setStyleSheet("background-color: #2ecc71; color: white;")
        cadastro.btnAnalise.setEnabled(True)
        cadastro.AVISO_ANALISE = True
        cadastro.nenhum = False
        aviso_analise()
    else:
        cadastro.btnAnalise.setStyleSheet("background-color: #bdc3c7; color: black;")
        cadastro.btnAnalise.setEnabled(False)
        cadastro.HABILITADO_ANALISE = False

    if todos_preenchidos and (idade_val is not None) and (renda_val is not None):
        cadastro.btnSalvar.setEnabled(True)
        cadastro.btnSalvar.setStyleSheet("background-color: #2ecc71; color: white;")
        cadastro.todos = True
        tudo_ok()
    else:
        cadastro.btnSalvar.setEnabled(False)
        cadastro.btnSalvar.setStyleSheet("background-color: #bdc3c7; color: black;")
        cadastro.todos = False

    if (todos_preenchidos is not True) and (cadastro.AVISO_ANALISE is not True) or (analise_pronta is not True):
        cadastro.nenhum = True
        cadastro.todos = False
        cadastro.HABILITADO_ANALISE = False
        nenhum_ok()



def botao_analise_clicado():
    cadastro.HABILITADO_ANALISE = True
    cadastro.todos = False
    cadastro.AVISO_ANALISE = False
    analise()


def desabilita_analise():
    cadastro.HABILITADO_ANALISE = False
    atualizar_estado_ui()


def aviso_analise():
    if cadastro.AVISO_ANALISE:
        cadastro.nenhum = False
        cadastro.HABILITADO_ANALISE = False
        cadastro.txtSituacao.setText('Botão de Análise habilitado')
        return


def analise():
    if cadastro.HABILITADO_ANALISE:
        cadastro.AVISO_ANALISE = False

        idade_text = cadastro.txtIdade.text().strip()
        renda_text = cadastro.txtRenda.text().strip()

        idade = to_int_safe(idade_text)
        renda = to_float_safe(renda_text)

        if renda and idade and cadastro.HABILITADO_ANALISE:
            if renda >= 3500 and idade >= 21:
                mensagem = ' Cadastro com chances de crédito!'
            else:
                mensagem = ' Cadastro não está apto para adquirir crédito.'

            cadastro.txtSituacao.mensagem_analise = mensagem
            cadastro.txtSituacao.pos = 0

            cadastro.txtSituacao.timer = QTimer()
            cadastro.txtSituacao.timer.timeout.connect(lambda: mover_texto(cadastro.txtSituacao))
            cadastro.txtSituacao.timer.start(170)

            QTimer.singleShot(2000, parar_timer)



def mover_texto(widget):
    cadastro.mensagem_analise = widget.mensagem_analise
    widget.pos += 1

    if widget.pos > len(cadastro.mensagem_analise):
        widget.pos = 0

    cadastro.mensagem_analise = cadastro.mensagem_analise[widget.pos:] + "   " + cadastro.mensagem_analise[:widget.pos]
    widget.setText(cadastro.mensagem_analise)


def parar_timer():
    cadastro.txtSituacao.timer.stop()
    cadastro.txtSituacao.setText(cadastro.txtSituacao.mensagem_analise)


def tudo_ok():
    if cadastro.todos and (cadastro.HABILITADO_ANALISE is not True):
        cadastro.HABILITADO_ANALISE = False
        cadastro.txtSituacao.setText('Ok, todos os campos foram preenchidos')
        return


def nenhum_ok():
    if cadastro.nenhum and (cadastro.HABILITADO_ANALISE is not True) and (cadastro.todos is not True):
        cadastro.txtSituacao.setText("Preencha todos os dados.")



def relatorio():
    relatorio.show()
    cursor = conexao.cursor()
    comando_SQL = 'select * from clientes'
    cursor.execute(comando_SQL)
    leitura_clientes = cursor.fetchall()

    relatorio.tableClientes.setRowCount(len(leitura_clientes))
    relatorio.tableClientes.setColumnCount(6)

    for i in range(0, len(leitura_clientes)):
        for j in range(0, 6):
            relatorio.tableClientes.setItem(i, j, QtWidgets.QTableWidgetItem(str(leitura_clientes[i][j])))


numero_id_geral = 0


def begin_alterar():
    global numero_id_geral

    dados = relatorio.tableClientes.currentRow()
    cursor = conexao.cursor()
    cursor.execute('select id from clientes')
    leitura_clientes = cursor.fetchall()
    id_ativo = leitura_clientes[dados][0]

    cursor.execute('select * from clientes where id=' + str(id_ativo))
    leitura_clientes = cursor.fetchall()

    editar_tabela.show()

    numero_id_geral = id_ativo

    editar_tabela.txtAlterarId.setText(str(leitura_clientes[0][0]))
    editar_tabela.txtAlterarNome.setText(str(leitura_clientes[0][1]))
    editar_tabela.txtAlterarCpf.setText(str(leitura_clientes[0][2]))
    editar_tabela.txtAlterarIdade.setText(str(leitura_clientes[0][3]))
    editar_tabela.txtAlterarRenda.setText(str(leitura_clientes[0][4]))
    editar_tabela.txtAlterarAnalise.setText(str(leitura_clientes[0][5]))


def finally_alterar():
    global numero_id_geral

    id = editar_tabela.txtAlterarId.text()
    nome = editar_tabela.txtAlterarNome.text()
    cpf = editar_tabela.txtAlterarCpf.text()
    idade = editar_tabela.txtAlterarIdade.text()
    renda = editar_tabela.txtAlterarRenda.text()
    situacao = editar_tabela.txtAlterarAnalise.text()

    cursor = conexao.cursor()
    cursor.execute("update clientes set id = '{}',nome = '{}',Cpf = '{}',IDADE = '{}',renda = '{}',situacao = '{}' where id = {}".format(
        id, nome, cpf, idade, renda, situacao, numero_id_geral))

    editar_tabela.close()
    relatorio.close()
    cadastro.show()

    conexao.commit()


def excluir():
    excluir = relatorio.tableClientes.currentRow()
    relatorio.tableClientes.removeRow(excluir)

    cursor = conexao.cursor()
    cursor.execute('select id from clientes')
    leitura_clientes = cursor.fetchall()
    id_ativo = leitura_clientes[excluir][0]

    cursor.execute('delete from clientes where id=' + str(id_ativo))
    conexao.commit()


def pular_campo(atual, proximo):
     if atual.text() != "":
        proximo.setFocus()





app= QtWidgets.QApplication([])                         

cadastro = uic.loadUi(resource_path('Projeto_CadastroQT.ui'))    



cadastro.btnSalvar.setEnabled(False)
cadastro.btnAnalise.setEnabled(False)

cadastro.HABILITADO_ANALISE = False
cadastro.todos = False
cadastro.nenhum = False
cadastro.AVISO_ANALISE = False

cadastro.btnAnalise.clicked.connect(botao_analise_clicado)
cadastro.btnSalvar.clicked.connect(inserir_dados)
cadastro.btnRelatorio.clicked.connect(relatorio)


relatorio = uic.loadUi(resource_path('RelatoriosClientes.ui'))

relatorio.btnExcluir.clicked.connect(excluir)

relatorio.btnEditar.clicked.connect(begin_alterar)
editar_tabela = uic.loadUi(resource_path('Alterar.ui'))

editar_tabela.btnAlterar.clicked.connect(finally_alterar)




cadastro.txtNome.textChanged.connect(atualizar_estado_ui)
cadastro.txtCpf.textChanged.connect(atualizar_estado_ui)
cadastro.txtIdade.textChanged.connect(atualizar_estado_ui)
cadastro.txtRenda.textChanged.connect(atualizar_estado_ui)
cadastro.txtAnalise.textChanged.connect(desabilita_analise)




cadastro.txtNome.returnPressed.connect(
    lambda: pular_campo(cadastro.txtNome, cadastro.txtCpf)
)

cadastro.txtCpf.returnPressed.connect(
    lambda: pular_campo(cadastro.txtCpf, cadastro.txtIdade)
)

cadastro.txtIdade.returnPressed.connect(
    lambda: pular_campo(cadastro.txtIdade, cadastro.txtRenda)
)

cadastro.txtRenda.returnPressed.connect(
    lambda: pular_campo(cadastro.txtRenda, cadastro.txtAnalise)
)

cadastro.txtAnalise.returnPressed.connect(
    lambda: pular_campo(cadastro.txtAnalise, cadastro.txtNome)
)



 





cadastro.show()             

app.exec()                      



