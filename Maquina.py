import sys
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
        self.__alfabTrab = linhas[1].split()
        self.__branco = linhas[2]
        self.__Q = linhas[3].split()
        self.__q0 = linhas[4]
        self.__qAtual = self.__q0
        self.__qf = linhas[5].split()
        self.__qtdFita = linhas[6]
        self.__Fita = Fita(self.__branco, entrada)
        self.__transicoes = []
        for tran in linhas[7:]:
            self.__transicoes.append(Transicoes(tran.split())) # 7: referência tudo o que vier depois do 7
        arq.close()

    def realizaTransicao(self):
        flag = 0
        for i in range (0,len(self.__transicoes)):
            if(flag == 0):
                # print(self.__transicoes[i].imprime())
                self.__qAtual = self.__transicoes[i].verificaEstado(self.__qAtual, self.__Fita)
                flag = self.__transicoes[i].getFlag()
            if(flag != 0):
                self.__transicoes[i].cleanFlag()
                return 0
            for j in range (0, len(self.__qf)):
                if(self.__qAtual == self.__qf[j]):
                    return 1
        return -1
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
        self.__flag = 0

    def verificaEstado(self, estadoAtual, fita):
        if self.__estadoAtual == estadoAtual: #Verifica se e o estado correspondênte

            if self.__simbAtual == fita.getSimbAtual(): # Verifica se o símbolo bate
                self.__flag = 1
                fita.setSimbAtual(self.__simbNovo) #Atualiza o Símbolo pelo novo
                # print(self.__sentidoMov)
                fita.setPosAtual(self.__sentidoMov)# Corre a fita pra direita ou esquerda
                return self.__estadoDestino
                
        return estadoAtual

    def cleanFlag(self):
        self.__flag = 0

    def getFlag(self):
        return self.__flag

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
            if self.__fita[self.__posicaoAtual] == "...": #garante que o processo nunca ultrapassará o limite esquerdo
                self.__fita[self.__posicaoAtual] = self.__branco
                self.__fita = ['...', self.__branco, self.__branco].append(self.__fita)
            
            self.__posicaoAtual -= 1

        elif sentido == 'R':
            if self.__fita[self.__posicaoAtual] == "...": #garante que o processo nunca ultrapassará o limitie direito
                self.__fita[self.__posicaoAtual] = self.__branco
                self.__fita.append([self.__branco, self.__branco, '...'])
            self.__posicaoAtual += 1

    def imprime(self):
        for i in range(0, len(self.__fita)):
            if(i == self.__posicaoAtual):
                
                print ('\033[31m'+'' + self.__fita[i] + ''+'\033[0;0m', end = ' ')
            else:
                print(self.__fita[i], end = ' ')
        print()

#-------------------------------------------------------------------------------------------------------------------
maq = Maquina(sys.argv[1],sys.argv[2]) # recebe do terminal o nome do arquivo texto = sys.argv[1] # recebe do terminal a entrada
i = 0
while i == 0:
    maq.imprimeFita()
    i = maq.realizaTransicao()
    if(i == 1):
        print("verdade")
    if(i == -1):
        print("falso")
