import mysql.connector                          
# mysql.connector é o driver que conecta python+sql , as vezes da problema , então salve feche e reabra o Vscode
from PyQt5 import uic, QtWidgets                
# PyQt é uma biblioteca que une Python e Qt ; uic importa recursos de interface; QtWidgets importa os widgets Qt

import sys, os, traceback
from PyQt5.QtCore import QTimer


def resource_path(relative_path):
    """Retorna o caminho correto do arquivo, tanto em .py quanto no .exe"""
    if hasattr(sys, '_MEIPASS'):
        # quando o PyInstaller empacota, os arquivos vão pra uma pasta temporária
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)




# (conexao é uma variavel que recebe dados do banco de dados) ,com esse comando eu abro parenteses para informar os dados de onde está e o nome do meu banco de dados
conexao = mysql.connector.connect(        

    host = '127.0.0.1',                   
    # host é o local onde esta meu banco de dados ,la no mysql
    user = 'dev',                              
    # user é o nome de usuário onde esta o banco
    password = '9584',                         
    # senha para entrar no usuario la do mysql
    database = 'cadastro_credito'            
    # database é o nome que foi dado para o banco la na programação do mysql
)

# (def) é um comando que aplica alguma função dentro do programa... (inserir_dados) é o nome dessa função
def inserir_dados():                                     

    # revalida tudo antes de salvar (impede burlar) --------------------------
    # pega valores e tenta converter para os tipos corretos, e verifica se nenhum está vazio
    nome = cadastro.txtNome.text().strip()
    cpf = cadastro.txtCpf.text().strip()
    idade = to_int_safe(cadastro.txtIdade.text().strip())
    renda = to_float_safe(cadastro.txtRenda.text().strip())
    situacao = cadastro.txtAnalise.text().strip()



# --------------------------- SALVAMENTO DOS DADOS LÁ NO MYSQL (INSERTO INTO) ----------------------------------------

    cursor = conexao.cursor()                                                                                                  
    # criamos uma variavel cursor que recebe dados do banco conexao e executa o comando cursor (que esta explicado no caderno de estudos)
    comando_SQL = 'insert into clientes(nome,cpf,idade,renda,situacao) values(%s,%s,%s,%s,%s)'                                      
    # criamos uma variavel(comando_SQL) que vai receber as instruções em SQL ,                        
    # # %s - está ai para informar ao insert into (incrementador de tabela) que ainda não sabemos o valor de cada variavel, pois ela vai ser incrementada pelo usuário
    dados = (str(nome),str(cpf),str(idade),str(renda),str(situacao))        
    # criamos a variavel (dados) como uma forma de organizar os dados que serão recebidos em uma variavel que recebe as insformações em entre parenteses.     
    # str = string   ( É USADO STRING MESMO , POR SE TRATAR DE CAIXA DE TEXTO DA INTERFACE)                                                                     
    cursor.execute(comando_SQL,dados)                           
    # com esse comando( cursor.execute) eu falo para o cursor executar e levar tanto o insert into quanto os dados para o banco de dados para o SQL                                                                              
    
    
    conexao.commit()                
    # é um comando de verificação , para saber se esta tudo batendo certinho com o Nosso banco de dados no SQL

    cadastro.txtNome.setText('')
    cadastro.txtCpf.setText('')
    cadastro.txtIdade.setText('')
    cadastro.txtRenda.setText('')
    cadastro.txtAnalise.setText('')
    cadastro.txtSituacao.setText('Dados foram salvos')

     # ativa a supressão de atualizações por 2 segundos
     # O nome suppress_updates foi escolhido porque descreve bem o que faz:  “suprimir (pausar) as atualizações”.
     # O prefixo _ (underline) é só uma convenção em Python que significa: “essa variável é para uso interno, não faz parte da interface pública do objeto.”
     #  quando é true ele para temporariamente ( através de um timer , estabelecido) as atualizações de mensagem na def atualização , focando na ultima mensagem.
    cadastro._suppress_updates = cadastro.txtSituacao.setText('Dados foram salvos')

    def fim_do_salvamento():
        cadastro._suppress_updates = False
        # depois que liberar, reavalia o estado (mostrar OK ou outra mensagem)
        atualizar_estado_ui()

    QTimer.singleShot(2000, fim_do_salvamento)
    


    






# -------------------------------- VERIFICAÇÃO DOS DADOS PREENCHIDOS PELO USUÁRIO ----------------------------------------

def verifica_vazio(widget):
     
    """Retorna True se o campo tem texto não vazio."""
    # widget.text() pega o texto atual do campo (QLineEdit)
    # .strip() remove espaços antes e depois
    # bool(...) converte string vazia para False e string não-vazia para True
    return bool(widget.text().strip())

def to_float_safe(text):
    # tenta converter uma string para float; se falhar retorna None ao invés de lançar exceção
    try:
        return float(text)
    except Exception:
        return None
    
def to_int_safe(text):
    # tenta converter uma string para int; se falhar retorna None ao invés de lançar exceção
    try:
        return int(text)
    except Exception:
        return None
   

# ---------------------- FUNÇÃO CENTRAL DE ATUALIZAÇÃO DE INFORMAÇÕES DIGITADAS ---------------------------




def atualizar_estado_ui():
   
 

      # se está suprimindo updates, sai sem tocar na mensagem/estado
    if getattr(cadastro, '_suppress_updates', False):
        return
 



    
   

    """
        Deve ser chamada:
      - sempre que qualquer campo mudar (textChanged)
      - após executar ações (analise, salvar, etc.)
    Ela decide a mensagem (com prioridade) e habilita/desabilita botões.
    """

    # checagens atuais ----------------------------------------------------
    # verifica_vazio(cadastro.txtNome) verifica se o campo nome contém texto não vazio
    nome = cadastro.txtNome.text().strip()

    cpf = cadastro.txtCpf.text().strip()

    # pega o texto bruto do campo idade e remove espaços extras (usado para validação/parse)
    idade = cadastro.txtIdade.text().strip()

    # pega o texto bruto do campo renda e remove espaços extras
    renda = cadastro.txtRenda.text().strip()

    situacao = cadastro.txtAnalise.text().strip()

    # tenta parsear idade/renda para números de forma segura (None se inválido)
    
    idade_val = to_int_safe(idade)
    renda_val = to_float_safe(renda)

    nome_preenchido = (nome != "")          # True se nome tem algo
    cpf_limpo = "".join(filter(str.isdigit, cpf))
    idade_preenchido = (idade != "")        # True se usuário digitou algo (mesmo que inválido)
    renda_preenchido = (renda != "")        # True se usuário digitou algo
    situacao_preenchido = (situacao != "")  # True se o campo analise/observacao tem algo

    analise_pronta = (idade_val is not None) and (renda_val is not None) 

    todos_preenchidos = (nome_preenchido and cpf_limpo and idade_preenchido and renda_preenchido and situacao_preenchido)

    nenhum_preenchido = (nome == "" and cpf_limpo == "" and idade == "" and renda == "" and situacao == "")
    
# ---------------------------------- HABILITA OU NÃO BOTÕES (ANALISE E SALVAR) ------------------------------------------


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

        


# Se todos estiverem preenchidos, ativa o botão
    if todos_preenchidos and (idade_val is not None) and (renda_val is not None):
        cadastro.btnSalvar.setEnabled(True)
        cadastro.btnSalvar.setStyleSheet("background-color: #2ecc71; color: white;")
        cadastro.todos = True
        tudo_ok()
    else:
        cadastro.btnSalvar.setEnabled(False)
        cadastro.btnSalvar.setStyleSheet("background-color: #bdc3c7; color: black;")
        cadastro.todos = False





    if (todos_preenchidos is not True) and (cadastro.AVISO_ANALISE is not True) or (analise_pronta is not True) :
     
        
        cadastro.nenhum = True

        cadastro.todos = False
        cadastro.HABILITADO_ANALISE = False
        nenhum_ok()

        




    
   

      
# ------------------------ESCOLHA A MENSAGEM TRANSMITIDA POR PRIORIDADE: -----------------------------------



            

            
           
  
def botao_analise_clicado():
    
    cadastro.HABILITADO_ANALISE = True
    cadastro.todos = False
    cadastro.AVISO_ANALISE = False
    analise()

def desabilita_analise ():

    cadastro.HABILITADO_ANALISE = False

    atualizar_estado_ui()


def aviso_analise():

      if cadastro.AVISO_ANALISE :

        cadastro.nenhum = False
        cadastro.HABILITADO_ANALISE = False
        cadastro.txtSituacao.setText('Botão de Análise habilitado')


        return  
        


def analise():

    if cadastro.HABILITADO_ANALISE :
     
     cadastro.AVISO_ANALISE = False

         # 1) LEITURA (sempre criar variáveis locais antes de qualquer uso)
     idade_text = cadastro.txtIdade.text().strip()
     renda_text = cadastro.txtRenda.text().strip()

    # 2) CONVERSÃO SEGURA (funções to_int_safe / to_float_safe devem existir)
     idade = to_int_safe(idade_text)
     renda = to_float_safe(renda_text)

     if renda and idade and cadastro.HABILITADO_ANALISE  :

      if renda >= 3500 and idade >= 21:
        mensagem = ' Cadastro com chances de crédito!'
      else:
        mensagem = ' Cadastro não está apto para adquirir crédito.'

       
     
      cadastro.txtSituacao.mensagem_analise = mensagem
      cadastro.txtSituacao.pos = 0        #Posição inicial do texto
    

      if mensagem is not None :
      # if not has attr = verifica se o objeto tem ou não um atributo(attr) chamado 'timer', no caso o objeto é o qwidget txtSituacao la do cadastro
      #Fazemos isso para não criar múltiplos timers toda vez que analise() for chamada. Só criamos o timer na primeira vez.
    
            cadastro.txtSituacao.timer = QTimer()                       #Cria um QTimer e guarda ele como atributo do próprio widget txtSituacao. Isso facilita controlar o timer só a partir do widget (start/stop).
            cadastro.txtSituacao.timer.timeout.connect(lambda: mover_texto(cadastro.txtSituacao))       #conecta o timeout(que é o relógio do qtimer que esta contando o tempo que foi estabelecido) na função mover_texto quando o tempo de 170ms se concluir
             
# lambda é uma função anonima , ela serve para chamar a função mover_texto sempre que o timer acabar , loop . ou seja ela não deixa a função entrar automaticamente.
    # Reinicia o timer (a cada 170 ms o texto desliza)
            cadastro.txtSituacao.timer.start(170)

            
            QTimer.singleShot(2000, parar_timer)
            

      

    
    
    
    

  
    

def mover_texto(widget):
        """Função auxiliar que faz o texto deslizar horizontalmente."""
        cadastro.mensagem_analise = widget.mensagem_analise           #variavel recebe  a mensagem da def analise
        widget.pos += 1             # +1 serve para indicar movimento para direita do texto
    
    # Quando o contador (widget.pos) é maior que o tamanho do texto (len(texto)), significa que o texto chegou ao fim.
    #Então o código reseta o contador para 0, fazendo o texto começar de novo — criando o efeito contínuo (loop infinito).
    # len é a quantidade de caraceres que tem no texto
        if widget.pos > len(cadastro.mensagem_analise):
            widget.pos = 0          # widget.pos é um contador (inteiro) que aumenta de 1 em 1 a cada chamada do QTimer. com a pos =0 , significa que vai aparecer a mensagem inteira só ai aparecera outra mensagem em seguida.

   
    #essa parte faz a rotação da mensagem 
    #texto[widget.pos:] → pega do ponto atual até o fim da mensagem inteira
    # " " → adiciona um pequeno espaço para dar separação visual (como se o texto “passasse” na tela).
     #Depois, junta tudo (+) — criando uma string “girada”.
        cadastro.mensagem_analise = cadastro.mensagem_analise[widget.pos:] + "   " + cadastro.mensagem_analise[:widget.pos]
        widget.setText(cadastro.mensagem_analise)           # set no movimento novamente , com o widget.pos (loop)


def parar_timer():
    
  
    


    cadastro.txtSituacao.timer.stop()

    cadastro.txtSituacao.setText (cadastro.txtSituacao.mensagem_analise)

 
        

    
        



def tudo_ok ():

    if  cadastro.todos and (cadastro.HABILITADO_ANALISE is not True) :
      # apenas mantenha a mensagem atual (não sobrescreve)

        cadastro.HABILITADO_ANALISE = False


        cadastro.txtSituacao.setText('Ok, todos os campos foram preenchidos')
       
        return

def nenhum_ok():

    if cadastro.nenhum and (cadastro.HABILITADO_ANALISE is not True) and (cadastro.todos is not True):


        cadastro.txtSituacao.setText("Preencha todos os dados.")










  
    




   




  

    





def relatorio():
    relatorio.show()

    cursor = conexao.cursor()
    #com esse comando conseguimos conectar um comando la do mySQL, levando para a variavel comando_SQL, com o cursor e dentro da def relatorio
    comando_SQL = 'select * from clientes'
    #a variavel comando_SQL recebe a tabela de clientes la do SQL
    cursor.execute(comando_SQL)
    #EXECUTA a variavel comando_SQL la no mySQL
    leitura_clientes = cursor.fetchall()
    #A VARIAVEL leitura_clientes recebe as colunas(as informações) da tabela la do mySQL , atraves do comando cursor.fetchall
    relatorio.tableClientes.setRowCount(len(leitura_clientes))
    #esse comando diz que na interface relatorio tem uma tabela(tableClientes)e com o comando setRowCount(len)(inicia contagem de linhas)
    relatorio.tableClientes.setColumnCount(6)
    #esse informa a quantidade de colunas (6)
    for i in range (0,len(leitura_clientes)):
        for j in range(0,6):
    # aqui estou dando o nome i para as linhas e j para as colunas , range significa procurar/pesquisar entre 0 até a ultima linha ou coluna.
            relatorio.tableClientes.setItem(i,j, QtWidgets.QTableWidgetItem(str(leitura_clientes[i][j])))
            #esse comando é o de organização que faz o set dos itens acumulado e ja com as informações das quantidades de linhas e colunas da tabela , e distribui de forma ordenada para i e para j, formando a tabela corretamente.

numero_id_geral = 0
#criei uma variavel fora de todos os DEFs, ou seja todo o programa pode-se utilizar dessa variavel, e inicialmente seu valor é 0.

def begin_alterar():

    global numero_id_geral
    #informei meu def que a variavel numero_id_geral existe.

    dados = relatorio.tableClientes.currentRow()
    #currentRow é quando o usuario clica em alguma LINHA(ativa) da tabela , essa informação será capturada pela variavel dados.
    cursor = conexao.cursor()
    cursor.execute('select id from clientes')
    #aqui estamos selecionando os dados da coluna id la na tabela cliente no banco de dados SQL
    leitura_clientes = cursor.fetchall()
    #o fetchall vai pegar todas as informações dos id na tabela clientes e entrega ao python em forma de LISTA.
    id_ativo = leitura_clientes[dados] [0]
    # vamos acumular essa lista em id_ativo que vai estar recebendo na hora o id clicado pelo usuario e mandando para ordem 0 que é o id[0] da tabela
    cursor.execute('select * from clientes where id='+str(id_ativo))
    #executa com o cursor a tabela clientes onde esta as string do id_ativo(os dados da linha id onde o usuario clicou)
    leitura_clientes = cursor.fetchall()
    #aqui temos que chamar dnv o fetchall, pois nós vamos isolar apenas a informação contida no id_ativo


    editar_tabela.show()

    numero_id_geral = id_ativo
    #fazendo isso a variavel criada que antes valia 0 , agora recebe os dados da variavel id_ativo que esta na def begin_alterar

    editar_tabela.txtAlterarId.setText(str(leitura_clientes[0][0]))
    #aqui dizemos ao programa que na tela editar_tabela temos uma cx de mensagem chamada txtAlterarId e que ESTAMOS mandando para esse espaço a informação do leitura_clientes juntamente com sua devida posição.
    editar_tabela.txtAlterarNome.setText(str(leitura_clientes[0][1]))
    editar_tabela.txtAlterarCpf.setText(str(leitura_clientes[0][2]))
    editar_tabela.txtAlterarIdade.setText(str(leitura_clientes[0][3]))
    editar_tabela.txtAlterarRenda.setText(str(leitura_clientes[0][4]))
    editar_tabela.txtAlterarAnalise.setText(str(leitura_clientes[0][5]))
#todos são string iguais (mesma lógica), porém em colchetes primeiro é o numero da posição da linha , e em segundo é o numero da posição da coluna , tudo na tabela base la do SQL.

def finally_alterar ():

    global numero_id_geral
    #aqui estou chamando a variavel criada anteriormente fora das DEFs , PORÉM AGORA por questão de ordem de leitura do programa ela ja vem com o valor que esta aplicado la na DEF begin_alterar.

    id  = editar_tabela.txtAlterarId.text()
    nome = editar_tabela.txtAlterarNome.text()
    cpf = editar_tabela.txtAlterarCpf.text()
    idade = editar_tabela.txtAlterarIdade.text()
    renda = editar_tabela.txtAlterarRenda.text()
    situacao = editar_tabela.txtAlterarAnalise.text()
    #aqui abrimos uma nova def com a função de alterar manualmente cada caixa de texto que esta na janela de alterar.ui, ja com os dados captados pela def begin_alterar, que é o passo inicial.
    #essa alteração é possivel pelo código de ''''''''''.text

    cursor = conexao.cursor()
    #VAMOS chamaR a conexão com o banco de dados la do SQL, para poder dar o UPDATE dessa edição
    cursor.execute("update clientes set id = '{}',nome = '{}',Cpf = '{}',IDADE = '{}',renda = '{}',situacao = '{}' where id = {}".format(id,nome,cpf,idade,renda,situacao,numero_id_geral))
    #com o cursor.execute estamos executando uma query, que nada mais é um comando feito aqui no python que acontece la no MySQL , no nosso banco de dados
    #dentro dessa query estamos dizendo que na linha id clicada pelo usuario vai ser setada para novas informações que vão ser realocadas no lugar das informações antigas que estavam na tabela.


    #VAMOS FAZER UM REFRESH DE UPDATE , que nada mais é que fechar as janelas e abrir novamente depois de salvo uma alteração (atualizar)
    editar_tabela.close()
    relatorio.close()
    cadastro.show()


    conexao.commit()

def excluir():

     excluir = relatorio.tableClientes.currentRow()
     relatorio.tableClientes.removeRow(excluir)
     #faz o comando de excluir a linha que foi clicada pelo ussuário, mas apenas a linha visual da interface , e não a do banco de dados.
     cursor = conexao.cursor()
     cursor.execute('select id from clientes')
     leitura_clientes = cursor.fetchall()
    #o fetchall vai pegar todas as informações dos id na tabela clientes e entrega ao python em forma de LISTA.
     id_ativo = leitura_clientes[excluir] [0]

     cursor.execute('delete from clientes where id='+str(id_ativo))
     # essa query faz com que la no SQL , delete da table clientes onde o id recebe a variavel id_ativo , ou seja onde o usuario clicou.

     conexao.commit()


# ---------------------------------   atual , proximo .  if atual(txt) nao for vazia proximo.setFocus , ao apertar o 'ENTER' pula para o proximo txt ja estabelecido la no lambda --------------------------------------------
def pular_campo(atual, proximo):
    if atual.text() != "":
        proximo.setFocus()





app= QtWidgets.QApplication([])                         
# o (app) é uma variavel , que recebe os widgets la do Qt, e o .QApplication([]) faz com que essa variavel seja aplicavel, ou seja , dinamica.

cadastro = uic.loadUi(resource_path('Projeto_CadastroQT.ui'))    
# O (cadastro) é uma variavel que recebe a tela do Qtdesigner, o .loadUi('Projeto_CadastroQT.ui') permite carregar exatamente a interface que queremos.


# Desabilita o botão no início
cadastro.btnSalvar.setEnabled(False)
cadastro.btnAnalise.setEnabled(False)

cadastro.HABILITADO_ANALISE = False
cadastro.todos = False
cadastro.nenhum = False
cadastro.AVISO_ANALISE = False

#clicked.connect da uma função de clique no botão e leva para o  o def -->inserir_dados
cadastro.btnAnalise.clicked.connect(botao_analise_clicado)
cadastro.btnSalvar.clicked.connect(inserir_dados)

# esse leva para o def ---> analise

# Aqui temos uma jogada interessante, na interface cadastro(1ªinterface), dizemos ao programa que quando clicado o botao relatorio, ele deve excecutar/connectar a função def(relatorio),
# também colocamos o load da interface relatorio depois da função do btn , para não ter risco do programa abrir antes do clicar do botao relatorio.
cadastro.btnRelatorio.clicked.connect(relatorio)
relatorio = uic.loadUi(resource_path('RelatoriosClientes.ui'))

relatorio.btnExcluir.clicked.connect(excluir)

relatorio.btnEditar.clicked.connect(begin_alterar)
editar_tabela = uic.loadUi(resource_path('Alterar.ui'))

editar_tabela.btnAlterar.clicked.connect(finally_alterar)




# ---------------------- conectar textChanged para revalidar dinamicamente ------------------------

# cada vez que o usuário digitar ou apagar, atualizar_estado_ui será chamado
cadastro.txtNome.textChanged.connect(atualizar_estado_ui)
cadastro.txtCpf.textChanged.connect(atualizar_estado_ui)
cadastro.txtIdade.textChanged.connect(atualizar_estado_ui)
cadastro.txtRenda.textChanged.connect(atualizar_estado_ui)
cadastro.txtAnalise.textChanged.connect(desabilita_analise)



# -------------  lambda que conecta a def pular_campo -----------------------------------------
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



 



# ------------------------------------ inicializa estado -----------------------------------------------------

# guarda um espaço para o resultado da última análise; None significa "sem resultado"

cadastro.show()             
# mostra / apresenta  a interface  cadastro.ui
app.exec()                      
# executa os parametros/ dinamismo da interface grafica









