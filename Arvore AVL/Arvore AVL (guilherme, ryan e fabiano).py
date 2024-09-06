auxprint = 0  # Variável global para controlar a exibição da árvore
auxprint2 =0

auxprint3 = 0  # Variável global para controlar a exibição da árvore
auxprint4 =0

class NoAVL:
    def __init__(self, chave):
        self.esquerda = None  # Referência ao filho à esquerda
        self.direita = None   # Referência ao filho à direita
        self.valor = chave    # Valor armazenado no nó
        self.altura = 1       # Altura do nó na árvore

class ArvoreAVL:
    def __init__(self):
        self.raiz = None  # Raiz da árvore AVL, inicialmente vazia

    def _altura(self, no):
        if no is None:
            return 0  # Nó nulo tem altura 0
        return no.altura  # Retorna a altura do nó

    def _fator_balanceamento(self, no):
        if no is None:
            return 0  # Fator de balanceamento de um nó nulo é 0
        return self._altura(no.esquerda) - self._altura(no.direita)  # Diferença de altura entre subárvores

    def _rotacao_direita(self, y):
        x = y.esquerda  # Novo nó raiz após rotação
        T2 = x.direita  # Subárvore que será movida
        x.direita = y   # Executa a rotação
        y.esquerda = T2
        y.altura = max(self._altura(y.esquerda), self._altura(y.direita)) + 1  # Atualiza a altura
        x.altura = max(self._altura(x.esquerda), self._altura(x.direita)) + 1
        return x  # Retorna o novo nó raiz

    def _rotacao_esquerda(self, x):
        y = x.direita  # Novo nó raiz após rotação
        T2 = y.esquerda  # Subárvore que será movida
        y.esquerda = x   # Executa a rotação
        x.direita = T2
        x.altura = max(self._altura(x.esquerda), self._altura(x.direita)) + 1  # Atualiza a altura
        y.altura = max(self._altura(y.esquerda), self._altura(y.direita)) + 1
        return y  # Retorna o novo nó raiz

    def inserir(self, chave):
        if not self.raiz:
            self.raiz = NoAVL(chave)  # Cria a raiz se a árvore estiver vazia
        else:
            self.raiz = self._inserir_recursivo(self.raiz, chave)  # Insere o valor na árvore de forma recursiva

    def _inserir_recursivo(self, no, chave):
        global auxprint
        global auxprint2
        if no is None:
            return NoAVL(chave)  # Cria um novo nó se o nó atual for nulo

        if chave < no.valor:
            no.esquerda = self._inserir_recursivo(no.esquerda, chave)  # Insere na subárvore esquerda se a chave for menor
        else:
            no.direita = self._inserir_recursivo(no.direita, chave)  # Insere na subárvore direita se a chave for maior

        no.altura = 1 + max(self._altura(no.esquerda), self._altura(no.direita))  # Atualiza a altura do nó
        
        if auxprint == 0 and auxprint2 == 1:
            arvore.exibir()  # Exibe a árvore
            auxprint = 2

        balanceamento = self._fator_balanceamento(no)  # Calcula o fator de balanceamento do nó

        if balanceamento > 1 and chave < no.esquerda.valor:
            return self._rotacao_direita(no)  # Rotação à direita se a árvore está desbalanceada para a esquerda

        if balanceamento < -1 and chave > no.direita.valor:
            return self._rotacao_esquerda(no)  # Rotação à esquerda se a árvore está desbalanceada para a direita

        if balanceamento > 1 and chave > no.esquerda.valor:
            no.esquerda = self._rotacao_esquerda(no.esquerda)  # Rotação dupla esquerda-direita
            return self._rotacao_direita(no)

        if balanceamento < -1 and chave < no.direita.valor:
            no.direita = self._rotacao_direita(no.direita)  # Rotação dupla direita-esquerda
            return self._rotacao_esquerda(no)

        return no  # Retorna o nó atualizado
    
    def inserir_vetor(self, valores):
            #Insere todos os valores do vetor na árvore AVL.
            for valor in valores:
                self.inserir(valor)

    def remover(self, chave):
        if not self.raiz:
            return  # Se a árvore estiver vazia, não há nada para remover
        self.raiz = self._remover_recursivo(self.raiz, chave)  # Remove o valor de forma recursiva

    def _remover_recursivo(self, no, chave):
        global auxprint3
        global auxprint4
        if no is None:
            return no  # Se o nó for nulo, apenas retorna

        if chave < no.valor:
            no.esquerda = self._remover_recursivo(no.esquerda, chave)  # Busca na subárvore esquerda
        elif chave > no.valor:
            no.direita = self._remover_recursivo(no.direita, chave)  # Busca na subárvore direita
        else:
            if no.esquerda is None:
                return no.direita  # Retorna a subárvore direita se o nó não tiver filho à esquerda
            elif no.direita is None:
                return no.esquerda  # Retorna a subárvore esquerda se o nó não tiver filho à direita

            temp = self._no_valor_minimo(no.direita)  # Encontra o menor valor na subárvore direita
            no.valor = temp.valor  # Substitui o valor do nó pelo menor valor
            no.direita = self._remover_recursivo(no.direita, temp.valor)  # Remove o nó substituído

        if no is None:
            return no  # Se o nó for nulo após a remoção, apenas retorna

        if auxprint3 == 0 and auxprint4 == 1:
            arvore.exibir()  # Exibe a árvore
            auxprint3 = 2

        no.altura = max(self._altura(no.esquerda), self._altura(no.direita)) + 1  # Atualiza a altura
        balanceamento = self._fator_balanceamento(no)  # Calcula o fator de balanceamento

        if balanceamento > 1 and self._fator_balanceamento(no.esquerda) >= 0:
            return self._rotacao_direita(no)  # Rotação à direita

        if balanceamento > 1 and self._fator_balanceamento(no.esquerda) < 0:
            no.esquerda = self._rotacao_esquerda(no.esquerda)  # Rotação dupla esquerda-direita
            return self._rotacao_direita(no)

        if balanceamento < -1 and self._fator_balanceamento(no.direita) <= 0:
            return self._rotacao_esquerda(no)  # Rotação à esquerda

        if balanceamento < -1 and self._fator_balanceamento(no.direita) > 0:
            no.direita = self._rotacao_direita(no.direita)  # Rotação dupla direita-esquerda
            return self._rotacao_esquerda(no)

        return no  # Retorna o nó atualizado

    def _no_valor_minimo(self, no):
        atual = no
        while atual.esquerda is not None:
            atual = atual.esquerda  # Navega para o nó mais à esquerda
        return atual  # Retorna o nó com o menor valor

    def exibir(self, no=None, prefixo="", eh_esquerda=True):
        if self.raiz is None:
            print("Árvore está vazia")  # Mensagem se a árvore estiver vazia
            return
        
        if no is None:
            no = self.raiz  # Começa pela raiz se nenhum nó for passado

        if no.direita is not None:
            novo_prefixo = prefixo + ("│   " if eh_esquerda else "    ")
            self.exibir(no.direita, novo_prefixo, False)  # Exibe a subárvore direita

        print(prefixo + ("└── " if eh_esquerda else "┌── ") + str(no.valor))  # Exibe o nó atual

        if no.esquerda is not None:
            novo_prefixo = prefixo + ("    " if eh_esquerda else "│   ")
            self.exibir(no.esquerda, novo_prefixo, True)  # Exibe a subárvore esquerda

    def salvar_em_arquivo(self, nome_arquivo):
        with open(nome_arquivo, 'w') as arquivo:
            self._salvar_recursivo(self.raiz, arquivo)  # Salva a árvore em um arquivo

    def _salvar_recursivo(self, no, arquivo):
        if no is None:
            arquivo.write("#\n")  # Indicador de nó nulo
            return
        arquivo.write(str(no.valor) + '\n')  # Salva o valor do nó
        self._salvar_recursivo(no.esquerda, arquivo)  # Salva a subárvore esquerda
        self._salvar_recursivo(no.direita, arquivo)  # Salva a subárvore direita

    def carregar_de_arquivo(self, nome_arquivo):
        with open(nome_arquivo, 'r') as arquivo:
            linhas = iter(arquivo.readlines())  # Lê todas as linhas do arquivo
            self.raiz = self._carregar_recursivo(linhas)  # Carrega a árvore do arquivo

    def _carregar_recursivo(self, linhas):
        try:
            valor = next(linhas).strip()
            if valor == "#":
                return None  # Nó nulo indicado por "#"
            no = NoAVL(int(valor))  # Cria um novo nó
            no.esquerda = self._carregar_recursivo(linhas)  # Carrega a subárvore esquerda
            no.direita = self._carregar_recursivo(linhas)  # Carrega a subárvore direita
            no.altura = 1 + max(self._altura(no.esquerda), self._altura(no.direita))  # Atualiza a altura
            return no
        except StopIteration:
            return None  # Fim das linhas

if __name__ == "__main__":

    arvore = ArvoreAVL()  # Cria uma nova árvore AVL

    while True:
        
        try:
            opcao = int(input("\nEscolha uma opção: \n" +
                              "[1] - Inserir apenas um número\n" +
                              "[2] - Remover apenas um número\n" +
                              "[3] - Exibir\n" +
                              "[4] - Adicionar vetor inteiro\n" +
                              "[5] - Remover vetor inteiro\n" +
                              "[6] - Salvar árvore em arquivo\n" +
                              "[7] - Carregar árvore de arquivo\n" +
                               "[8] - Inserir lista de números\n" + 
                              "[0] - Sair\n"))
        except ValueError:
            print("\nPor favor, insira um número válido.")
            continue

        if opcao == 0:
            print("\nSaindo do programa.")
            break

        elif opcao == 1:
            try:
                valor = int(input("\nDigite um valor a ser inserido: "))
                arvore.inserir(valor)  # Insere o valor na árvore
                arvore.exibir()  # Exibe a árvore após inserção
                input("\nPressione <enter> para continuar")
            except ValueError:
                print("\nPor favor, insira um número válido.")

        elif opcao == 2:
            try:
                valor = int(input("\nDigite um valor a ser removido: "))
                arvore.remover(valor)  # Remove o valor da árvore
                arvore.exibir()  # Exibe a árvore após remoção
                input("\nPressione <enter> para continuar")
            except ValueError:
                print("\nPor favor, insira um número válido.")

        elif opcao == 3:
            arvore.exibir()  # Exibe a árvore
            input("\nPressione <enter> para continuar")

        elif opcao == 4:
            while True:
                
                valor = input("\nDigite um valor a ser inserido (ou 'sair' para voltar ao menu): ")
                if valor.lower() == 'sair':
                    break
                try:
                    auxprint2 = 1
                    valor_int = int(valor)
                    arvore.inserir(valor_int)  # Insere o valor na árvore
                    print("\narvore balanceada")
                    arvore.exibir()  # Exibe a árvore após inserção
                    auxprint = 0
                    auxprint2 = 0
                except ValueError:
                    print("\nPor favor, insira um número válido.")
            input("\nPressione <enter> para continuar")

        elif opcao == 5:
            while True:
                arvore.exibir()  # Exibe a árvore após remoção
                valor = input("\nDigite um valor a ser removido (ou 'sair' para voltar ao menu): ")
                if valor.lower() == 'sair':
                    break
                try:
                    auxprint4 = 1
                    valor_int = int(valor)
                    arvore.remover(valor_int)  # Remove o valor da árvore
                    print("\narvore balanceada depois da remoçao")
                    arvore.exibir()  # Exibe a árvore após remoção
                    auxprint3 = 0
                    auxprint4 = 0
                except ValueError:
                    print("\nPor favor, insira um número válido.")
            input("\nPressione <enter> para continuar")

        elif opcao == 6:
            nome_arquivo = input("\nDigite o nome do arquivo para salvar a árvore: ")
            arvore.salvar_em_arquivo(nome_arquivo)  # Salva a árvore no arquivo
            print(f"\nÁrvore salva no arquivo '{nome_arquivo}'.")
            input("\nPressione <enter> para continuar")

        elif opcao == 7:
            nome_arquivo = input("\nDigite o nome do arquivo para carregar a árvore: ")
            arvore.carregar_de_arquivo(nome_arquivo)  # Carrega a árvore do arquivo
            print(f"\nÁrvore carregada do arquivo '{nome_arquivo}'.")
            arvore.exibir()  # Exibe a árvore após carregamento
            input("\nPressione <enter> para continuar")
        
        elif opcao == 8:
            valores_str = input("\nDigite os valores separados por espaço: ")
            valores = list(map(int, valores_str.split()))
            arvore.inserir_vetor(valores)
            arvore.exibir()
            input("\nPressione <enter> para continuar")
            
        else:
            print("\nOpção inválida. Tente novamente.")
