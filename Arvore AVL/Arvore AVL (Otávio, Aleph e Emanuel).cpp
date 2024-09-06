#include <stdio.h>
#include <stdlib.h>

typedef struct no {
    struct no *esq, *dir;
    int chave;
    int altura;
} TNo;

void inicializa(TNo **ptr) {
    *ptr = NULL;
}

int altura(TNo *ptr) {
    if (ptr == NULL)
        return 0;
    return ptr->altura;
}

int max(int a, int b) {
    return (a > b) ? a : b;
}

int fatorBalanceamento(TNo *ptr) {
    if (ptr == NULL)
        return 0;
    return altura(ptr->esq) - altura(ptr->dir);
}

TNo* rotacaoDireita(TNo *y) {
    TNo *x = y->esq;
    TNo *T2 = x->dir;

    x->dir = y;
    y->esq = T2;

    y->altura = max(altura(y->esq), altura(y->dir)) + 1;
    x->altura = max(altura(x->esq), altura(x->dir)) + 1;

    return x;
}

TNo* rotacaoEsquerda(TNo *x) {
    TNo *y = x->dir;
    TNo *T2 = y->esq;

    y->esq = x;
    x->dir = T2;

    x->altura = max(altura(x->esq), altura(x->dir)) + 1;
    y->altura = max(altura(y->esq), altura(y->dir)) + 1;

    return y;
}

TNo* balancear(TNo *ptr) {
    ptr->altura = 1 + max(altura(ptr->esq), altura(ptr->dir));
    int fb = fatorBalanceamento(ptr);

    if (fb > 1 && fatorBalanceamento(ptr->esq) >= 0)
        return rotacaoDireita(ptr);

    if (fb > 1 && fatorBalanceamento(ptr->esq) < 0) {
        ptr->esq = rotacaoEsquerda(ptr->esq);
        return rotacaoDireita(ptr);
    }

    if (fb < -1 && fatorBalanceamento(ptr->dir) <= 0)
        return rotacaoEsquerda(ptr);

    if (fb < -1 && fatorBalanceamento(ptr->dir) > 0) {
        ptr->dir = rotacaoDireita(ptr->dir);
        return rotacaoEsquerda(ptr);
    }

    return ptr;
}

TNo* insere(TNo *ptr, int chave) {
    if (ptr == NULL) {
        TNo *novo = (TNo *)malloc(sizeof(TNo));
        novo->chave = chave;
        novo->esq = NULL;
        novo->dir = NULL;
        novo->altura = 1;
        return novo;
    }

    if (chave < ptr->chave)
        ptr->esq = insere(ptr->esq, chave);
    else if (chave > ptr->chave)
        ptr->dir = insere(ptr->dir, chave);
    else
        return ptr;

    return balancear(ptr);
}

TNo* antecessor(TNo *ptr) {
    TNo *atual = ptr;
    while (atual->dir != NULL)
        atual = atual->dir;
    return atual;
}

TNo* retira(TNo *ptr, int chave) {
    if (ptr == NULL) {
        printf("\nA chave #%d nao esta na arvore!", chave);
        return ptr;
    }

    if (chave < ptr->chave)
        ptr->esq = retira(ptr->esq, chave);
    else if (chave > ptr->chave)
        ptr->dir = retira(ptr->dir, chave);
    else {
        if ((ptr->esq == NULL) || (ptr->dir == NULL)) {
            TNo *temp = ptr->esq ? ptr->esq : ptr->dir;
            if (temp == NULL) {
                temp = ptr;
                ptr = NULL;
            } else
                *ptr = *temp;
            free(temp);
        } else {
            TNo *temp = antecessor(ptr->esq);
            ptr->chave = temp->chave;
            ptr->esq = retira(ptr->esq, temp->chave);
        }
    }

    if (ptr == NULL)
        return ptr;

    return balancear(ptr);
}

void altera(TNo **ptr, int chaveAntiga, int chaveNova) {
    *ptr = retira(*ptr, chaveAntiga);
    *ptr = insere(*ptr, chaveNova);
}

void imprimeEstrutura(TNo *ptr, int nivel) {
    int i;
    if (ptr == NULL) {
        return;
    }

    imprimeEstrutura(ptr->dir, nivel + 1);

    for (i = 0; i < nivel; i++) {
        printf("    ");
    }
    printf("%d\n", ptr->chave);

    imprimeEstrutura(ptr->esq, nivel + 1);
}

void salvarArquivo(TNo *ptr, FILE *arquivo) {
    if (ptr == NULL) {
        return;
    }
    salvarArquivo(ptr->esq, arquivo);
    fprintf(arquivo, "%d\n", ptr->chave);
    salvarArquivo(ptr->dir, arquivo);
}

void carregarArquivo(TNo **ptr, FILE *arquivo) {
    int chave;
    while (fscanf(arquivo, "%d", &chave) != EOF) {
        *ptr = insere(*ptr, chave);
    }
}

int main() {
    TNo *ptr;
    inicializa(&ptr);

    int opcao, valor, chaveAntiga, chaveNova;
    FILE *arquivo;

    do {
        printf("\n\nMenu:");
        printf("\n1. Inserir");
        printf("\n2. Remover");
        printf("\n3. Alterar");
        printf("\n4. Mostrar arvore em estrutura");
        printf("\n5. Salvar arvore em arquivo");
        printf("\n6. Carregar arvore de arquivo");
        printf("\n7. Sair");
        printf("\nEscolha uma opcao: ");
        scanf("%d", &opcao);

        switch (opcao) {
            case 1:
                printf("Digite o valor a ser inserido: ");
                scanf("%d", &valor);
                ptr = insere(ptr, valor);
                break;
            case 2:
                printf("Digite o valor a ser removido: ");
                scanf("%d", &valor);
                ptr = retira(ptr, valor);
                break;
            case 3:
                printf("Digite o valor que deseja alterar: ");
                scanf("%d", &chaveAntiga);
                printf("Digite o novo valor: ");
                scanf("%d", &chaveNova);
                altera(&ptr, chaveAntiga, chaveNova);
                break;
            case 4:
                printf("Estrutura da arvore:\n");
                imprimeEstrutura(ptr, 0);
                break;
            case 5:
                arquivo = fopen("arvore.txt", "w");
                if (arquivo != NULL) {
                    salvarArquivo(ptr, arquivo);
                    fclose(arquivo);
                    printf("Arvore salva em 'arvore.txt'.\n");
                } else {
                    printf("Erro ao abrir o arquivo.\n");
                }
                break;
            case 6:
                arquivo = fopen("arvore.txt", "r");
                if (arquivo != NULL) {
                    inicializa(&ptr);  // Limpa a árvore antes de carregar do arquivo
                    carregarArquivo(&ptr, arquivo);
                    fclose(arquivo);
                    printf("Arvore carregada de 'arvore.txt'.\n");
                } else {
                    printf("Erro ao abrir o arquivo.\n");
                }
                break;
            case 7:
                printf("Saindo...\n");
                break;
            default:
                printf("Opcao invalida!\n");
        }
    } while (opcao != 7);

    return 0;
}
