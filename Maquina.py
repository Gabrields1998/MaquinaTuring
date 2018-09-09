import sys
from copy import copy

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
        
    def verificaBifurcacao(self): # Salva as transacoes que possivelmente se tornaram uma nova bifurcacao
        del self.__vetTransicoes[:] 
        for i in range (0,len(self.__transicoes)): # flag == 1 se for armazenar transicao/ 0 se nao for
            flag = self.__transicoes[i].verificaTransicao(self.__qAtual, self.__Fita)

            if flag == 1 :
                self.__vetTransicoes.append(self.__transicoes[i]) # inclui no fim do vetor 
        if len(self.__vetTransicoes) == 0:
            return -1 
        return self.__vetTransicoes

    def realizaTransicao(self, transicao):
        self.__qAtual = transicao.executaTransicao(self.__Fita)

        for j in range (0, len(self.__qf)):
            if self.__qAtual == self.__qf[j]:   
                return 1
        return 0

    def alteraFita(self):
        self.__Fita = copy(self.__Fita)

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
        print(self.__estadoAtual + self.__estadoDestino + self.__simbNovo + self.__simbNovo + self.__sentidoMov)

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

    maquina = listaMaq.pop(0)
    nome = maquina.getNome()
    status = 0
    print("Maquina", nome, "Executando")
    maquina.imprimeFita()
    print()
    
    transicao = maquina.verificaBifurcacao() #conferir

    if transicao == -1:

        if len(listaMaq) == 0:
            print("falso")
            exit(0)
        print("maquina",nome, "morta")
        print()
        status = 1
       
    elif len(transicao) == 1:
        indice = maquina.realizaTransicao(transicao[0])
        
    
    elif len(transicao) > 1:

        for j in range(1,len(transicao)):
            newMaquina = copy(maquina)
            newMaquina.alteraFita()
            nomeMaq += 1
            newMaquina.setNome(nomeMaq)
            indice = newMaquina.realizaTransicao(transicao[j])
            if indice == 1:
                print("verdade")
                exit(0)
            listaMaq.append(newMaquina)      
        indice = maquina.realizaTransicao(transicao[0])

    if indice == 1:
        print("verdade")
        exit(0)
    if status == 0:
        listaMaq.append(maquina)

    del transicao
