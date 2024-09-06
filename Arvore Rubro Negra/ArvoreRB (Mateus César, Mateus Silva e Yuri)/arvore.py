
import os
import graphviz

class No:
    def __init__(self, valor, cor="vermelho"):
        self.valor = valor
        self.cor = cor
        self.esquerda = None
        self.direita = None
        self.pai = None

class ArvoreRubroNegra:
    def __init__(self):
        self.NIL = No(valor=None, cor="preto")  
        self.NIL.esquerda = None
        self.NIL.direita = None
        self.raiz = self.NIL

    def inserir(self, valor):
        novo_no = No(valor)
        novo_no.esquerda = self.NIL
        novo_no.direita = self.NIL
        novo_no.pai = None

        if self.raiz == self.NIL:
            self.raiz = novo_no
            novo_no.cor = "preto"
        else:
            self._inserir_no(self.raiz, novo_no)
            self._consertar_insercao(novo_no)
        
        self.atualizar_imagem()  

    def _inserir_no(self, raiz, novo_no):
        pai = None
        atual = raiz

        while atual != self.NIL:
            pai = atual
            if novo_no.valor < atual.valor:
                atual = atual.esquerda
            else:
                atual = atual.direita

        novo_no.pai = pai

        if pai is None:
            self.raiz = novo_no
        elif novo_no.valor < pai.valor:
            pai.esquerda = novo_no
        else:
            pai.direita = novo_no

    def _buscar_no(self, no, valor):
        if no == self.NIL or valor == no.valor:
            return no
        if valor < no.valor:
            return self._buscar_no(no.esquerda, valor)
        else:
            return self._buscar_no(no.direita, valor)

    def _consertar_insercao(self, no):
        while no.pai and no.pai.cor == "vermelho":
            if no.pai == no.pai.pai.esquerda:
                tio = no.pai.pai.direita
                if tio.cor == "vermelho":
                    no.pai.cor = "preto"
                    tio.cor = "preto"
                    no.pai.pai.cor = "vermelho"
                    no = no.pai.pai
                else:
                    if no == no.pai.direita:
                        no = no.pai
                        self._rotacao_esquerda(no)
                    no.pai.cor = "preto"
                    no.pai.pai.cor = "vermelho"
                    self._rotacao_direita(no.pai.pai)
            else:
                tio = no.pai.pai.esquerda
                if tio.cor == "vermelho":
                    no.pai.cor = "preto"
                    tio.cor = "preto"
                    no.pai.pai.cor = "vermelho"
                    no = no.pai.pai
                else:
                    if no == no.pai.esquerda:
                        no = no.pai
                        self._rotacao_direita(no)
                    no.pai.cor = "preto"
                    no.pai.pai.cor = "vermelho"
                    self._rotacao_esquerda(no.pai.pai)
            if no == self.raiz:
                break
        self.raiz.cor = "preto"



    def _rotacao_esquerda(self, no):
        direita_no = no.direita
        no.direita = direita_no.esquerda
        if direita_no.esquerda != self.NIL:
            direita_no.esquerda.pai = no
        direita_no.pai = no.pai
        if no.pai is None:
            self.raiz = direita_no
        elif no == no.pai.esquerda:
            no.pai.esquerda = direita_no
        else:
            no.pai.direita = direita_no
        direita_no.esquerda = no
        no.pai = direita_no

    def _rotacao_direita(self, no):
        esquerda_no = no.esquerda
        no.esquerda = esquerda_no.direita
        if esquerda_no.direita != self.NIL:
            esquerda_no.direita.pai = no
        esquerda_no.pai = no.pai
        if no.pai is None:
            self.raiz = esquerda_no
        elif no == no.pai.direita:
            no.pai.direita = esquerda_no
        else:
            no.pai.esquerda = esquerda_no
        esquerda_no.direita = no
        no.pai = esquerda_no

    def remover(self, valor):
        no = self._buscar_no(self.raiz, valor)
        if no == self.NIL:
            print(f"Valor {valor} não encontrado na árvore.")
            return

        y = no
        y_cor_original = y.cor
        if no.esquerda == self.NIL:
            x = no.direita
            self._transplantar(no, no.direita)
        elif no.direita == self.NIL:
            x = no.esquerda
            self._transplantar(no, no.esquerda)
        else:
            y = self._minimo(no.direita)
            y_cor_original = y.cor
            x = y.direita
            if y.pai == no:
                x.pai = y
            else:
                self._transplantar(y, y.direita)
                y.direita = no.direita
                y.direita.pai = y
            self._transplantar(no, y)
            y.esquerda = no.esquerda
            y.esquerda.pai = y
            y.cor = no.cor
        if y_cor_original == "preto":
            self._consertar_remocao(x)

        self.atualizar_imagem() 

    def _transplantar(self, u, v):
        if u.pai is None:
            self.raiz = v
        elif u == u.pai.esquerda:
            u.pai.esquerda = v
        else:
            u.pai.direita = v
        v.pai = u.pai

    def _minimo(self, no):
        while no.esquerda != self.NIL:
            no = no.esquerda
        return no

    def _consertar_remocao(self, no):
        while no != self.raiz and no.cor == "preto":
            if no == no.pai.esquerda:
                w = no.pai.direita
                if w.cor == "vermelho":
                    w.cor = "preto"
                    no.pai.cor = "vermelho"
                    self._rotacao_esquerda(no.pai)
                    w = no.pai.direita
                if w.esquerda.cor == "preto" and w.direita.cor == "preto":
                    w.cor = "vermelho"
                    no = no.pai
                else:
                    if w.direita.cor == "preto":
                        w.esquerda.cor = "preto"
                        w.cor = "vermelho"
                        self._rotacao_direita(w)
                        w = no.pai.direita
                    w.cor = no.pai.cor
                    no.pai.cor = "preto"
                    w.direita.cor = "preto"
                    self._rotacao_esquerda(no.pai)
                    no = self.raiz
            else:
                w = no.pai.esquerda
                if w.cor == "vermelho":
                    w.cor = "preto"
                    no.pai.cor = "vermelho"
                    self._rotacao_direita(no.pai)
                    w = no.pai.esquerda
                if w.direita.cor == "preto" and w.esquerda.cor == "preto":
                    w.cor = "vermelho"
                    no = no.pai
                else:
                    if w.esquerda.cor == "preto":
                        w.direita.cor = "preto"
                        w.cor = "vermelho"
                        self._rotacao_esquerda(w)
                        w = no.pai.esquerda
                    w.cor = no.pai.cor
                    no.pai.cor = "preto"
                    w.esquerda.cor = "preto"
                    self._rotacao_direita(no.pai)
                    no = self.raiz
        no.cor = "preto"
    
    def carregar_ou_criar_arquivo(self):
        nome_arquivo = "dados.txt"
        if os.path.exists(nome_arquivo):
            print(f"Carregando dados do arquivo '{nome_arquivo}'.")
            self._reiniciar_arvore()
            self.carregar_de_arquivo(nome_arquivo)
        else:
            print(f"Arquivo '{nome_arquivo}' não encontrado. Criando novo arquivo.")
            with open(nome_arquivo, 'w') as arquivo:
                pass  #---------- Cria um arquivo vazio

    def _reiniciar_arvore(self):
        self.raiz = self.NIL
        self._remover_imagem()  

    def carregar_de_arquivo(self, nome_arquivo):
        with open(nome_arquivo, 'r') as arquivo:
            for linha in arquivo:
                valor = int(linha.strip())
                self.inserir(valor)

    def salvar_para_arquivo(self):
        nome_arquivo = "dados.txt"
        with open(nome_arquivo, 'w') as arquivo:
            self._salvar_no(self.raiz, arquivo)
        print(f"Árvore salva no arquivo '{nome_arquivo}'.")

    def _salvar_no(self, no, arquivo):
        if no != self.NIL:
            arquivo.write(f"{no.valor}\n")
            self._salvar_no(no.esquerda, arquivo)
            self._salvar_no(no.direita, arquivo)

    def atualizar_imagem(self):
        if self.raiz == self.NIL:
            print("Árvore vazia.")
            return

        dot = graphviz.Digraph()

        def adicionar_nos(no):
            if no != self.NIL:
                cor = "red" if no.cor == "vermelho" else "black"
                dot.node(str(no.valor), f"{no.valor}", color=cor, fontcolor=cor, style="filled", fillcolor="white")
                if no.esquerda != self.NIL:
                    dot.edge(str(no.valor), str(no.esquerda.valor))
                if no.direita != self.NIL:
                    dot.edge(str(no.valor), str(no.direita.valor))
                adicionar_nos(no.esquerda)
                adicionar_nos(no.direita)

        adicionar_nos(self.raiz)
        dot.render("arvore_rubro_negra", format="png", cleanup=True)
        print("Árvore gerada e salva como 'arvore_rubro_negra.png'.")

    def _remover_imagem(self):
        imagem = "arvore_rubro_negra.png"
        if os.path.exists(imagem):
            os.remove(imagem)
            print(f"Imagem '{imagem}' removida.")

    def limpar_arvore_e_arquivo(self):
        self._reiniciar_arvore()  #---------- Limpa a árvore da memória
        nome_arquivo = "dados.txt"
        open(nome_arquivo, 'w').close()#------------- Limpa o conteúdo do arquivo
        print(f"Árvore e arquivo '{nome_arquivo}' limpos.")

def menu():
    arvore = ArvoreRubroNegra()
    arvore.carregar_ou_criar_arquivo() #----------- Carrega os dados do arquivo no início

    while True:
        print("\nMenu:")
        print("1. Inserir Valor")
        print("2. Remover Valor")
        print("3. Salvar Árvore")
        print("4. Carregar Árvore")
        print("5. Limpar Árvore e Arquivo")
        print("6. Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            valor = int(input("Digite o valor a ser inserido: "))
            arvore.inserir(valor)
        elif escolha == "2":
            valor = int(input("Digite o valor a ser removido: "))
            arvore.remover(valor)
        elif escolha == "3":
            arvore.salvar_para_arquivo()
        elif escolha == "4":
            arvore.carregar_ou_criar_arquivo()
        elif escolha == "5":
            arvore.limpar_arvore_e_arquivo()  
        elif escolha == "6":
            print("Saindo do programa.")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
