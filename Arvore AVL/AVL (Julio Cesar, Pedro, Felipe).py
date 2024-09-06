import json # Módulo para manipulação de arquivos JSON
import os # Módulo para interagir com o sistema operacional (navegação de diretórios)

# Classe que define o nodo (ou nó) da árvore AVL
class Nodo:
    # Cada nodo tem uma chave, ponteiros para a esquerda e direita e sua altura
    def __init__(self, chave):
        self.chave = chave
        self.esquerda = None # Referência para o filho da esquerda
        self.direita = None # Referência para o filho da direita
        self.altura = 1  # Inicialmente, a altura do nodo é 1 (nó folha)

# Classe que define a árvore AVL
class ArvoreAVL:
    def __init__(self):
        self.raiz = None # Inicialmente, a árvore está vazia, logo a raiz é None

    # Função para inserir um valor na árvore
    def inserir(self, chave):
        # Inicia a inserção a partir da raiz da árvore
        self.raiz = self._inserir(self.raiz, chave)

    # Função recursiva que percorre a árvore para inserir o novo nodo
    def _inserir(self, nodo_atual, chave):
        # Se o nodo atual é None, o novo nodo deve ser criado aqui
        if not nodo_atual:
            return Nodo(chave)
        
        # Se a chave é menor que a do nodo atual, insere na subárvore esquerda
        if chave < nodo_atual.chave:
            nodo_atual.esquerda = self._inserir(nodo_atual.esquerda, chave)
        # Se a chave é maior, insere na subárvore direita
        elif chave > nodo_atual.chave:
            nodo_atual.direita = self._inserir(nodo_atual.direita, chave)
        # Se a chave já existe, não faz nada (nós duplicados não são permitidos)
        else:
            return nodo_atual  # Duplicatas não são permitidas

        # Atualiza a altura do nodo atual após a inserção
        nodo_atual.altura = 1 + max(self.altura(nodo_atual.esquerda), self.altura(nodo_atual.direita))

        # Calcula o fator de balanceamento do nodo atual para verificar se ele está desbalanceado
        balanceamento = self.fator_balanceamento(nodo_atual)

        # Caso de desbalanceamento à esquerda (rotação simples para a direita)
        if balanceamento > 1 and chave < nodo_atual.esquerda.chave:
            return self.rotacao_direita(nodo_atual)
        # Caso de desbalanceamento à esquerda-direita (rotação dupla: esquerda e depois direita)
        if balanceamento > 1 and chave > nodo_atual.esquerda.chave:
            nodo_atual.esquerda = self.rotacao_esquerda(nodo_atual.esquerda)
            return self.rotacao_direita(nodo_atual)
        # Caso de desbalanceamento à direita (rotação simples para a esquerda)
        if balanceamento < -1 and chave > nodo_atual.direita.chave:
            return self.rotacao_esquerda(nodo_atual)
        # Caso de desbalanceamento à direita-esquerda (rotação dupla: direita e depois esquerda)
        if balanceamento < -1 and chave < nodo_atual.direita.chave:
            nodo_atual.direita = self.rotacao_direita(nodo_atual.direita)
            return self.rotacao_esquerda(nodo_atual)

        # Retorna o nodo atual (que pode ser o novo raiz após rotações)
        return nodo_atual

    # Função para remover um valor da árvore
    def remover(self, chave):
        # Inicia a remoção a partir da raiz
        self.raiz = self._remover(self.raiz, chave)

    # Função recursiva que percorre a árvore para remover o nodo com a chave especificada
    def _remover(self, nodo_atual, chave):
        # Se o nodo atual é None, a chave não foi encontrada
        if not nodo_atual:
            return nodo_atual

        # Percorre a árvore para encontrar o nodo a ser removido
        if chave < nodo_atual.chave:
            nodo_atual.esquerda = self._remover(nodo_atual.esquerda, chave)
        elif chave > nodo_atual.chave:
            nodo_atual.direita = self._remover(nodo_atual.direita, chave)
        # Quando a chave é encontrada, o nodo precisa ser removido
        else:
            # Nodo com apenas um filho ou sem filhos
            if nodo_atual.esquerda is None:
                return nodo_atual.direita
            elif nodo_atual.direita is None:
                return nodo_atual.esquerda

            # Nodo com dois filhos: obtém o menor valor da subárvore direita
            temp = self._min_value_node(nodo_atual.direita)
            # Substitui a chave do nodo atual pela chave do menor valor encontrado
            nodo_atual.chave = temp.chave
            # Remove o menor valor da subárvore direita
            nodo_atual.direita = self._remover(nodo_atual.direita, temp.chave)

        # Se a árvore tinha apenas um nodo e este foi removido, retorna None
        if nodo_atual is None:
            return nodo_atual

        # Atualiza a altura do nodo atual após a remoção
        nodo_atual.altura = 1 + max(self.altura(nodo_atual.esquerda), self.altura(nodo_atual.direita))

        # Calcula o fator de balanceamento do nodo atual para verificar se ele está desbalanceado
        balanceamento = self.fator_balanceamento(nodo_atual)

        # Reequilibra a árvore se necessário (casos semelhantes aos da inserção)
        if balanceamento > 1 and self.fator_balanceamento(nodo_atual.esquerda) >= 0:
            return self.rotacao_direita(nodo_atual)
        if balanceamento > 1 and self.fator_balanceamento(nodo_atual.esquerda) < 0:
            nodo_atual.esquerda = self.rotacao_esquerda(nodo_atual.esquerda)
            return self.rotacao_direita(nodo_atual)
        if balanceamento < -1 and self.fator_balanceamento(nodo_atual.direita) <= 0:
            return self.rotacao_esquerda(nodo_atual)
        if balanceamento < -1 and self.fator_balanceamento(nodo_atual.direita) > 0:
            nodo_atual.direita = self.rotacao_direita(nodo_atual.direita)
            return self.rotacao_esquerda(nodo_atual)

        # Retorna o nodo atual (que pode ser o novo raiz após rotações)
        return nodo_atual

    # Função auxiliar para encontrar o nodo com o menor valor em uma subárvore
    def _min_value_node(self, nodo):
        atual = nodo
        # O menor valor está no nodo mais à esquerda
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual

    # Função auxiliar para obter a altura de um nodo
    def altura(self, nodo):
        if not nodo:
            # Se o nodo é None, a altura é 0
            return 0
        return nodo.altura

    # Função para calcular o fator de balanceamento de um nodo
    def fator_balanceamento(self, nodo):
        # O fator de balanceamento é a diferença entre as alturas das subárvores esquerda e direita
        if not nodo:
            return 0
        return self.altura(nodo.esquerda) - self.altura(nodo.direita)

    # Rotação simples à direita para corrigir desbalanceamento à esquerda
    def rotacao_direita(self, y):
        x = y.esquerda # Novo nodo raiz
        T2 = x.direita # Subárvore que será reposicionada

        # Realiza a rotação
        x.direita = y
        y.esquerda = T2

        # Atualiza as alturas dos nodos envolvidos
        y.altura = 1 + max(self.altura(y.esquerda), self.altura(y.direita))
        x.altura = 1 + max(self.altura(x.esquerda), self.altura(x.direita))

        # Retorna o novo nodo raiz
        return x
    
    # Rotação simples à esquerda para corrigir desbalanceamento à direita
    def rotacao_esquerda(self, x):
        y = x.direita # Novo nodo raiz
        T2 = y.esquerda # Subárvore que será reposicionada

        # Realiza a rotação
        y.esquerda = x
        x.direita = T2

        # Atualiza as alturas dos nodos envolvidos
        x.altura = 1 + max(self.altura(x.esquerda), self.altura(x.direita))
        y.altura = 1 + max(self.altura(y.esquerda), self.altura(y.direita))

        # Retorna o novo nodo raiz
        return y

    # Função para exibir a árvore no console (visualização em ordem reversa)
    def mostrar(self):
        if self.raiz is not None:
            self._mostrar(self.raiz)

    # Função recursiva que imprime a árvore de forma estruturada
    def _mostrar(self, nodo_atual, nivel=0):
        if nodo_atual is not None:
            # Chamada recursiva para os filhos esquerdo e direito
            self._mostrar(nodo_atual.direita, nivel + 1)
            print(' ' * 4 * nivel + '->', nodo_atual.chave)
            self._mostrar(nodo_atual.esquerda, nivel + 1)

    # Função para salvar a árvore em um arquivo JSON
    def salvar_em_json(self, nome_arquivo):
        dados = self._converter_para_dict(self.raiz)
        diretorio_script = os.path.dirname(os.path.abspath(__file__))
        diretorio = os.path.join(diretorio_script, "Arvores Salvas") # Cria o diretório se não existir
        
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)

        caminho_completo = os.path.join(diretorio, f"{nome_arquivo}.json")
        # Abre o arquivo JSON para escrita
        with open(caminho_completo, 'w') as arquivo_json:
            json.dump(dados, arquivo_json)
        print(f"Árvore salva com sucesso em {caminho_completo}.")

    # Função recursiva para converter a árvore em um dicionário para salvar em JSON
    def _converter_para_dict(self, nodo):
        if nodo is None:
            return None # Retorna None se o nodo não existir
        return {
            'chave': nodo.chave,
            'esquerda': self._converter_para_dict(nodo.esquerda),
            'direita': self._converter_para_dict(nodo.direita)
        }

    # Função para carregar a árvore a partir de um arquivo JSON
    def carregar_de_json(self, nome_arquivo):
        # Obtém o caminho completo do arquivo JSON
        diretorio_script = os.path.dirname(os.path.abspath(__file__))
        diretorio = os.path.join(diretorio_script, "Arvores Salvas")
        caminho_completo = os.path.join(diretorio, f"{nome_arquivo}.json")

        # Verifica se o arquivo existe
        if os.path.exists(caminho_completo):
            with open(caminho_completo, 'r') as arquivo_json:
                dados = json.load(arquivo_json) # Carrega os dados do arquivo JSON
                self.raiz = self._converter_de_dict(dados) # Converte os dados de volta para a árvore
                self.recalcular_altura(self.raiz)  # Recalcula as alturas após carregar a árvore
            print(f"Árvore carregada com sucesso de {caminho_completo}.")
        else:
            print(f"Arquivo {caminho_completo} não encontrado.")

    # Função para converter um dicionário em uma árvore
    def _converter_de_dict(self, dados):
        if dados is None:
            return None # Retorna None se os dados forem None
        nodo = Nodo(dados['chave']) # Cria um novo nodo com a chave
        nodo.esquerda = self._converter_de_dict(dados['esquerda']) # Converte a subárvore esquerda
        nodo.direita = self._converter_de_dict(dados['direita']) # Converte a subárvore direita
        return nodo
    
    # Função para recalcular a altura dos nodos na árvore
    def recalcular_altura(self, nodo):
        if nodo is None:
            return 0 # Retorna 0 se o nodo não existir
        # Recalcula a altura do nodo com base nas alturas das subárvores
        nodo.altura = 1 + max(self.recalcular_altura(nodo.esquerda), self.recalcular_altura(nodo.direita))
        return nodo.altura

    # Função para limpar a árvore
    def limpar(self):
        self.raiz = None # Define a raiz como None
        print("Árvore foi limpa.")

# Função principal que apresenta o menu e gerencia as operações na árvore
if __name__ == "__main__":
    arvore = ArvoreAVL() # Cria uma instância da árvore AVL

    while True:
        # Exibe o menu para o usuário
        print("\nMenu:")
        print("1. Inserir valor na árvore")
        print("2. Remover valor da árvore")
        print("3. Exibir árvore completa")
        print("4. Salvar árvore em JSON")
        print("5. Carregar árvore de JSON")
        print("6. Limpar a árvore")
        print("7. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            # Insere valores na árvore
            while True:
                valor = input("Digite um valor para inserir (ou 'x' para parar): ")
                if valor == 'x':
                    break
                try:
                    arvore.inserir(int(valor))
                except ValueError:
                    print("Por favor, insira um valor numérico válido.")

        elif opcao == '2':
            # Remove valores da árvore
            while True:
                valor = input("Digite um valor para remover (ou 'x' para parar): ")
                if valor == 'x':
                    break
                try:
                    arvore.remover(int(valor))
                except ValueError:
                    print("Por favor, insira um valor numérico válido.")

        elif opcao == '3':
            arvore.mostrar() # Exibe a árvore completa

        elif opcao == '4':
            nome_arquivo = input("Digite o nome do arquivo para salvar: ")
            arvore.salvar_em_json(nome_arquivo) # Salva a árvore em um arquivo JSON

        elif opcao == '5':
            nome_arquivo = input("Digite o nome do arquivo para carregar: ")
            arvore.carregar_de_json(nome_arquivo) # Carrega a árvore de um arquivo JSON

        elif opcao == '6':
            arvore.limpar() # Limpa a árvore

        elif opcao == '7': 
            break # Sai do loop e encerra o programa

        else:
            print("Opção inválida. Tente novamente.")
