import os
from colorama import Fore, Style, init

# Inicializar colorama
init(autoreset=True)

# Definições de cores
RED = Fore.RED
BLACK = Fore.RESET

class TNo:
    def __init__(self, chave=None):
        self.esq = None
        self.dir = None
        self.pai = None
        self.cor = True  # True para vermelho, False para preto
        self.chave = chave

class TArvore:
    def __init__(self):
        self.raiz = None

def rotacao_esq(arvore, no):
    direito = no.dir
    no.dir = direito.esq
    if direito.esq:
        direito.esq.pai = no
    direito.pai = no.pai
    if not no.pai:
        arvore.raiz = direito
    elif no == no.pai.esq:
        no.pai.esq = direito
    else:
        no.pai.dir = direito
    direito.esq = no
    no.pai = direito

def rotacao_dir(arvore, no):
    esquerdo = no.esq
    no.esq = esquerdo.dir
    if esquerdo.dir:
        esquerdo.dir.pai = no
    esquerdo.pai = no.pai
    if not no.pai:
        arvore.raiz = esquerdo
    elif no == no.pai.dir:
        no.pai.dir = esquerdo
    else:
        no.pai.esq = esquerdo
    esquerdo.dir = no
    no.pai = esquerdo

def inserir_fixup(arvore, no):
    while no.pai and no.pai.cor:
        if no.pai == no.pai.pai.esq:
            tio = no.pai.pai.dir
            if tio and tio.cor:
                no.pai.cor = False
                tio.cor = False
                no.pai.pai.cor = True
                no = no.pai.pai
            else:
                if no == no.pai.dir:
                    no = no.pai
                    rotacao_esq(arvore, no)
                no.pai.cor = False
                no.pai.pai.cor = True
                rotacao_dir(arvore, no.pai.pai)
        else:
            tio = no.pai.pai.esq
            if tio and tio.cor:
                no.pai.cor = False
                tio.cor = False
                no.pai.pai.cor = True
                no = no.pai.pai
            else:
                if no == no.pai.esq:
                    no = no.pai
                    rotacao_dir(arvore, no)
                no.pai.cor = False
                no.pai.pai.cor = True
                rotacao_esq(arvore, no.pai.pai)
    arvore.raiz.cor = False

def insere_no(arvore, chave):
    no = TNo(chave)
    raiz = arvore.raiz
    pai = None

    while raiz:
        pai = raiz
        if no.chave < raiz.chave:
            raiz = raiz.esq
        else:
            raiz = raiz.dir

    no.pai = pai

    if not pai:
        arvore.raiz = no
    elif no.chave < pai.chave:
        pai.esq = no
    else:
        pai.dir = no

    no.esq = None
    no.dir = None
    no.cor = True  # Nó inserido sempre é vermelho

    inserir_fixup(arvore, no)

def transplantar(arvore, u, v):
    if not u.pai:
        arvore.raiz = v
    elif u == u.pai.esq:
        u.pai.esq = v
    else:
        u.pai.dir = v
    if v:
        v.pai = u.pai

def minimo(no):
    while no.esq:
        no = no.esq
    return no

def deletar_fixup(arvore, no):
    while no != arvore.raiz and not no.cor:
        if no == no.pai.esq:
            irmao = no.pai.dir
            if irmao.cor:
                irmao.cor = False
                no.pai.cor = True
                rotacao_esq(arvore, no.pai)
                irmao = no.pai.dir
            if (not irmao.esq or not irmao.esq.cor) and (not irmao.dir or not irmao.dir.cor):
                irmao.cor = True
                no = no.pai
            else:
                if not irmao.dir or not irmao.dir.cor:
                    if irmao.esq:
                        irmao.esq.cor = False
                    irmao.cor = True
                    rotacao_dir(arvore, irmao)
                    irmao = no.pai.dir
                irmao.cor = no.pai.cor
                no.pai.cor = False
                if irmao.dir:
                    irmao.dir.cor = False
                rotacao_esq(arvore, no.pai)
                no = arvore.raiz
        else:
            irmao = no.pai.esq
            if irmao and irmao.cor:
                irmao.cor = False
                no.pai.cor = True
                rotacao_dir(arvore, no.pai)
                irmao = no.pai.esq
            if (not irmao.esq or not irmao.esq.cor) and (not irmao.dir or not irmao.dir.cor):
                irmao.cor = True
                no = no.pai
            else:
                if not irmao.esq or not irmao.esq.cor:
                    if irmao.dir:
                        irmao.dir.cor = False
                    irmao.cor = True
                    rotacao_esq(arvore, irmao)
                    irmao = no.pai.esq
                irmao.cor = no.pai.cor
                no.pai.cor = False
                if irmao.esq:
                    irmao.esq.cor = False
                rotacao_dir(arvore, no.pai)
                no = arvore.raiz
    no.cor = False

def deleta_no(arvore, chave):
    no = pesquisa(arvore.raiz, chave)
    if not no:
        print("\n→ Valor não encontrado na árvore!")
        return

    y = no
    y_cor_original = y.cor
    if not no.esq:
        x = no.dir
        transplantar(arvore, no, no.dir)
    elif not no.dir:
        x = no.esq
        transplantar(arvore, no, no.esq)
    else:
        y = minimo(no.dir)
        y_cor_original = y.cor
        x = y.dir
        if y.pai == no:
            if x:
                x.pai = y
        else:
            transplantar(arvore, y, y.dir)
            y.dir = no.dir
            y.dir.pai = y
        transplantar(arvore, no, y)
        y.esq = no.esq
        y.esq.pai = y
        y.cor = no.cor
    if not y_cor_original:
        if x:
            deletar_fixup(arvore, x)
        else:
            deletar_fixup(arvore, TNo(None))  # Nó sentinela

def pesquisa(no, chave):
    while no and no.chave != chave:
        if chave < no.chave:
            no = no.esq
        else:
            no = no.dir
    return no

def exibe_chave(no):
    if no.cor:
        print(f"{RED}{no.chave} ", end="")
    else:
        print(f"{BLACK}{no.chave} ", end="")

def in_ordem(no, arquivo=None):
    if no:
        in_ordem(no.esq, arquivo)
        if arquivo:
            arquivo.write(f"{no.chave} {int(no.cor)}\n")
        else:
            exibe_chave(no)
        in_ordem(no.dir, arquivo)

def pre_ordem(no, arquivo=None):
    if no:
        if arquivo:
            arquivo.write(f"{no.chave} {int(no.cor)}\n")
        else:
            exibe_chave(no)
        pre_ordem(no.esq, arquivo)
        pre_ordem(no.dir, arquivo)

def pos_ordem(no, arquivo=None):
    if no:
        pos_ordem(no.esq, arquivo)
        pos_ordem(no.dir, arquivo)
        if arquivo:
            arquivo.write(f"{no.chave} {int(no.cor)}\n")
        else:
            exibe_chave(no)


def exibir(no, prefixo="", eh_esquerda=True):
    if no is None:
        return

    if no.dir is not None:
        novo_prefixo = prefixo + ("│   " if eh_esquerda else "    ")
        exibir(no.dir, novo_prefixo, False)

    print(prefixo + ("└── " if eh_esquerda else "┌── ") + (f"{RED}{no.chave}" if no.cor else f"{BLACK}{no.chave}"))

    if no.esq is not None:
        novo_prefixo = prefixo + ("    " if eh_esquerda else "│   ")
        exibir(no.esq, novo_prefixo, True)


def salva_arvore(arvore, nome_arquivo, ordem):
    with open(nome_arquivo, "w") as arquivo:
        if ordem == 1:
            pre_ordem(arvore.raiz, arquivo)
        elif ordem == 2:
            in_ordem(arvore.raiz, arquivo)
        elif ordem == 3:
            pos_ordem(arvore.raiz, arquivo)

def carrega_arvore(arvore, arquivo):
    for linha in arquivo:
        chave_cor = linha.strip().split()
        if len(chave_cor) == 2:
            chave, cor = chave_cor
            chave = int(chave)
            cor = bool(int(cor))
            insere_no(arvore, chave)
            no = pesquisa(arvore.raiz, chave)
            no.cor = cor
    if arvore.raiz:
        arvore.raiz.cor = False

def salva_estrutura_arvore(no, arquivo):
    if no:
        if no.pai:  # Verifica se o nó tem pai
            posicao = 1 if no == no.pai.esq else 0
            arquivo.write(f"{no.chave} {int(no.cor)} {no.pai.chave} {posicao}\n")
        else:  # Se o nó não tiver pai, é a raiz
            arquivo.write(f"{no.chave} {int(no.cor)} None Root\n")
        salva_estrutura_arvore(no.esq, arquivo)
        salva_estrutura_arvore(no.dir, arquivo)

'''
valor do no - cor (0 preto/ 1 vermelho) - pai do no - posiçao (1 esquerda/ 0 direita)
30 0 None Root
6 0 30 1
2 1 6 1
40 0 30 0

'''

def carrega_estrutura_arvore(arvore, arquivo):
    nos = {}
    for linha in arquivo:
        chave, cor, pai_chave, posicao = linha.strip().split()
        chave = int(chave)
        cor = bool(int(cor))
        no = TNo(chave)
        no.cor = cor
        nos[chave] = no

        if pai_chave != 'None':
            pai_chave = int(pai_chave)
            no.pai = nos[pai_chave]
            if posicao == '1':
                nos[pai_chave].esq = no
            else:
                nos[pai_chave].dir = no
        else:
            arvore.raiz = no

    if arvore.raiz:
        arvore.raiz.cor = False  # A raiz sempre deve ser preta

def menu():
    arvore = TArvore()

    while True:
        print("\n" + f"{RED}={BLACK}="*20)
        print(f"    Árvore {RED}Rubro-{BLACK}Negra")
        print(f"{RED}={BLACK}="*20)
        print("1. Inserir valor")
        print("2. Remover valor")
        print("3. Exibir árvore visualmente")
        print("4. Exibir árvore em ordem")
        print("5. Exibir árvore em pré-ordem")
        print("6. Exibir árvore em pós-ordem")
        print("7. Salvar árvore pré,in,pós")
        print("8. Salvar árvore com estrutura")
        print("9. Carregar árvore de um arquivo")
        print("10. Carregar árvore com estrutura")
        print("11. Sair")
        

        escolha = input("\nEscolha uma opção: ")

        if escolha == "1":  # Inserir valor
            while True:
                valor = input("\nDigite um valor a ser inserido (ou 'sair' para voltar ao menu): ")
                if valor.lower() == 'sair':
                    break
                try:
                    valor_int = int(valor)
                    insere_no(arvore, valor_int)  # Insere o valor na árvore
                    print("\n→ Árvore após inserção:")
                    exibir(arvore.raiz)  # Exibe a árvore após a inserção
                except ValueError:
                    print("\n→ Por favor, insira um número válido.")
            input("\nPressione <enter> para continuar")

        elif escolha == "2":  # Remover valor
            while True:
                valor = input("\nDigite um valor a ser removido (ou 'sair' para voltar ao menu): ")
                if valor.lower() == 'sair':
                    break
                try:
                    valor_int = int(valor)
                    deleta_no(arvore, valor_int)  # Remove o valor da árvore
                    print("\n→ Árvore após remoção:")
                    exibir(arvore.raiz)  # Exibe a árvore após a remoção
                except ValueError:
                    print("\n→ Por favor, insira um número válido.")
            input("\nPressione <enter> para continuar")

        elif escolha == "3":
            if arvore.raiz:
                print("\n→ Exibindo a árvore visualmente:")
                exibir(arvore.raiz)
                print()
            else:
                print("\n→ A árvore está vazia.")
        
        elif escolha == "4":
            print("\n→ Exibindo a árvore em ordem:")
            exibir(arvore.raiz)
            print()
            in_ordem(arvore.raiz)
            print()

        elif escolha == "5":
            print("\n→ Exibindo a árvore em pré-ordem:")
            exibir(arvore.raiz)
            print()
            pre_ordem(arvore.raiz)
            print()

        elif escolha == "6":
            print("\n→ Exibindo a árvore em pós-ordem:")
            exibir(arvore.raiz)
            print()
            pos_ordem(arvore.raiz)
            print()
        elif escolha == "7":
            caminho = input("\nDigite o caminho do arquivo para salvar a árvore: ")
            print("\n→ Escolha a ordem de salvamento:")
            print("1. Pré-ordem")
            print("2. Em ordem")
            print("3. Pós-ordem")
            ordem = int(input("\nEscolha a ordem: "))
            if ordem in [1, 2, 3]:
                salva_arvore(arvore, caminho, ordem)
                print(f"\n→ Árvore salva com sucesso em {caminho}.")
            else:
                print("\n→ Ordem inválida. Tente novamente.")


        elif escolha == "8":
            caminho = input("\nDigite o caminho do arquivo para salvar a árvore com estrutura: ")
            with open(caminho, "w") as arquivo:
                salva_estrutura_arvore(arvore.raiz, arquivo)
            print(f"\n→ Árvore salva com sucesso em {caminho}.")

        
        elif escolha == "9":
            caminho = input("\nDigite o caminho do arquivo para carregar a árvore: ")
            try:
                with open(caminho, "r") as arquivo:
                    arvore = TArvore()  # Cria uma nova árvore para limpar a atual
                    carrega_arvore(arvore, arquivo)
                    print("\n→ Árvore carregada com sucesso.")
            except FileNotFoundError:
                print("\n→ Arquivo não encontrado. Tente novamente.")

        
        elif escolha == "10":
            caminho = input("\nDigite o caminho do arquivo para carregar a árvore com estrutura: ")
            try:
                with open(caminho, "r") as arquivo:
                    arvore = TArvore()  # Cria uma nova árvore para limpar a atual
                    carrega_estrutura_arvore(arvore, arquivo)
                    print("\n→ Árvore carregada com sucesso.")
            except FileNotFoundError:
                print("\n→ Arquivo não encontrado. Tente novamente.")


        elif escolha == "11":
            print("\n→ Saindo do programa.")
            break

        else:
            print("\n→ Escolha inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
