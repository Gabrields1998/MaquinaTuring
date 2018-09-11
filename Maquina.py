import sys
from copy import deepcopy

#--------------------------------------------------------------
class Maquina():
    def __init__(self, arquivo, entrada): # função construtora
        try:
            arq = open(arquivo,'r') # abre o arquivo
        except:
            print("arquivo não encontrado")
            exit(1)

        linhas = [lin.strip() for lin in arq.readlines()] #strip= elimina todos os caracteres dentro do (), caso vazio, elimina os \n
        # inicializa e atribui o valor de todas as variáveis de acordo com as especificações do Moodle :
        self.__alfabEntrada = linhas[0].split() # split separa todos os elementos da string e os torna elementos de um vetor
        self.__alfabTrab = linhas[1].split() #alfabeto de trabalho
        self.__branco = linhas[2] # simbolo "branco"
        self.__Q = linhas[3].split() #Estados da maquina (sem uso)
        self.__q0 = linhas[4] # Estado inicial
        self.__qAtual = self.__q0 # Estado atual da maquina apos cada transicao
        self.__qf = linhas[5].split() # Estados finais de aceitacao
        self.__qtdFita = linhas[6]
        self.__Fita = Fita(self.__branco, entrada)
        self.__vetTransicoes = [] # Vetor das transicoes que possivelmente se tornara uma nova execucao
        self.__transicoes = [] #vetor de toda transicao
        for tran in linhas[7:]:
            self.__transicoes.append(Transicoes(tran.split())) # 7: referência tudo o que vier depois do 7
        self.__nomeMaquina = 0
        arq.close()
        # for i in range (0, len(self.__transicoes)):
        #     print(self.__transicoes[i].imprime())
        

    def verificaBifurcacao(self): # Salva as transacoes que possivelmente se tornaram uma nova bifurcacao
        del self.__vetTransicoes[:]
        for i in range (0,len(self.__transicoes)): # flag == 1 se for armazenar transicao/ 0 se nao for
            flag = self.__transicoes[i].verificaTransicao(self.__qAtual, self.__Fita) #verifica se nesse estado irá ocorrer uma transição

            if flag == 1 :
                self.__vetTransicoes.append(self.__transicoes[i]) # inclui no fim do vetor 
        
        if len(self.__vetTransicoes) == 0:
            return -1 
        
        return self.__vetTransicoes

    def realizaTransicao(self, transicao):
        self.__qAtual = transicao.executaTransicao(self.__Fita)
        for j in range (0, len(self.__qf)):
            if self.__qAtual == self.__qf[j]: #caso o estado atual seja igual a um dos estados finais, retorna "verdade"
                return 1
        return 0 #retorna: continue o processo

    def alteraFita(self):
        self.__Fita = deepcopy(self.__Fita)

    def setNome(self, nome):
        self.__nomeMaquina = nome

    def getNome(self):
        return self.__nomeMaquina

    def imprimeFita(self):
        self.__Fita.imprime()



#-------------------------------------------------------------------------------------------------------------------
class Transicoes():
    def __init__(self, transicoes):
        self.__estadoAtual = transicoes[0]
        self.__estadoDestino = transicoes[1]
        self.__simbAtual = transicoes[2]
        self.__simbNovo = transicoes[3]
        self.__sentidoMov = transicoes[4]

    def verificaTransicao(self, estadoAtual, fita):
        if self.__estadoAtual == estadoAtual: #Verifica se e o estado correspondênte
            if self.__simbAtual == fita.getSimbAtual(): # Verifica se e o símbolo correspondente
                return 1
        return 0

    def executaTransicao(self, fita):
        fita.setSimbAtual(self.__simbNovo) #Atualiza o Símbolo pelo novo
        fita.setPosAtual(self.__sentidoMov)# Corre a fita pra direita ou esquerda
        return self.__estadoDestino

    def getEstadoAtual(self):
        return self.__estadoAtual

    def imprime(self):
        print("novosimbolo", self.__simbNovo)
        print(self.__estadoAtual + self.__estadoDestino + self.__simbAtual + self.__simbNovo + self.__sentidoMov)

#-------------------------------------------------------------------------------------------------------------------
class Fita():
    def __init__(self, branco, entrada):
        self.__branco = branco
        self.__fita = ['...',branco,branco] + [ini for ini in entrada] + [branco, branco, '...']# separa cada caractere em um espaço do vetor
        self.__posicaoAtual = 3


    def getSimbAtual(self):
        return self.__fita[self.__posicaoAtual]

    def setSimbAtual(self, simbNovo):
       self.__fita[self.__posicaoAtual] = simbNovo

    def setPosAtual(self, sentido):
        if sentido == 'L':
            if self.__fita[self.__posicaoAtual-1] == "...": #garante que o processo nunca ultrapassará o limite esquerdo
                self.__fita[self.__posicaoAtual-1] = self.__branco
                self.__fita = ['...', self.__branco, self.__branco].append(self.__fita)

            self.__posicaoAtual -= 1

        elif sentido == 'R':
            if self.__fita[self.__posicaoAtual+1] == "...": #garante que o processo nunca ultrapassará o limitie direito
                self.__fita[self.__posicaoAtual+1] = self.__branco
                self.__fita.append(self.__branco)
                self.__fita.append("...")
            self.__posicaoAtual += 1
        

    def imprime(self):
        for i in range(0, len(self.__fita)):
            if(i == self.__posicaoAtual):

                print ('\033[31m'+'' + self.__fita[i] + ''+'\033[0;0m', end = ' ')
            else:
                print(self.__fita[i], end = ' ')
        print()

#-------------------------------------------------------------------------------------------------------------------
listaMaq = []
listaMaq.append(Maquina(sys.argv[1],sys.argv[2])) # recebe do terminal o nome do arquivo texto = sys.argv[1] # recebe do terminal a entrada
indice = 0
nomeMaq = 0

while indice == 0:
    maquina = listaMaq.pop(0) #retira da fila o primeiro elemento
    nome = maquina.getNome()  #pega o nome para printar
    status = 0  # variavel de controle da execução de cada máquina
                # if status == 1 then maquina sem transição
    #--------------------------PRINT TRANSIÇÃO---------------------------
    print("-----------------------------------------------")
    print("Maquina", nome, "Executando")
    print()
    maquina.imprimeFita()
    print()
    
    transicao = maquina.verificaBifurcacao()


    transicao = maquina.verificaBifurcacao() #recebe as transições que devem ser executadas

    if transicao == -1: #caso não haja transição a ser executada
        if len(listaMaq) == 0: # caso não haja mais maquinas rodando
            print ('\033[1;31;40m'+'' + "falso!" + ''+'\033[0;0m')
            print()
            exit(0) #fim do processo
        print("maquina",nome, "morta")
        print()
        status = 1 # finaliza a maquina

    elif len(transicao) == 1: # realiza uma unica transição
        indice = maquina.realizaTransicao(transicao[0])
        
    
    elif len(transicao) > 1:
        # print(len(transicao))
        
        for j in range(1,len(transicao)):
            newMaquina = deepcopy(maquina)
            newMaquina.imprimeFita()
            newMaquina.alteraFita()
            nomeMaq += 1
            newMaquina.setNome(nomeMaq)
            indice = newMaquina.realizaTransicao(transicao[j]) #realiza uma transição diferente por máquina
            if indice == 1:
                print("verdade")
                exit(0)
            listaMaq.append(newMaquina)  
        indice = maquina.realizaTransicao(transicao[0])

    if indice == 1:
        print()
        print('\x1b[1;32;40m'+'' + "Verdade!" + ''+'\x1b[0m')
        print()
        exit(0)
    if status == 0:
        listaMaq.append(maquina) # guarda a máquina que esta rodando na vez no final da fila

    del transicao # reseta o vetor de transições
