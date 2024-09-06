#include <stdio.h>
#include <stdlib.h>

typedef enum { VERMELHO, PRETO } Cor;

typedef struct no {
    struct no *esq, *dir, *pai;
    int chave;
    Cor cor;
} TNo;

void inicializa(TNo **ptr) {
    *ptr = NULL;
}

TNo* criaNo(int chave) {
    TNo *novo = (TNo *)malloc(sizeof(TNo));
    novo->chave = chave;
    novo->esq = NULL;
    novo->dir = NULL;
    novo->pai = NULL;
    novo->cor = VERMELHO;  // Novos nós são sempre vermelhos inicialmente
    return novo;
}

TNo* rotacaoEsquerda(TNo *raiz, TNo *x) {
    TNo *y = x->dir;
    x->dir = y->esq;
    if (y->esq != NULL) y->esq->pai = x;
    y->pai = x->pai;
    if (x->pai == NULL) raiz = y;
    else if (x == x->pai->esq) x->pai->esq = y;
    else x->pai->dir = y;
    y->esq = x;
    x->pai = y;
    return raiz;
}

TNo* rotacaoDireita(TNo *raiz, TNo *y) {
    TNo *x = y->esq;
    y->esq = x->dir;
    if (x->dir != NULL) x->dir->pai = y;
    x->pai = y->pai;
    if (y->pai == NULL) raiz = x;
    else if (y == y->pai->esq) y->pai->esq = x;
    else y->pai->dir = x;
    x->dir = y;
    y->pai = x;
    return raiz;
}

TNo* balancearInsercao(TNo *raiz, TNo *z) {
    while (z != raiz && z->pai->cor == VERMELHO) {
        if (z->pai == z->pai->pai->esq) {
            TNo *tio = z->pai->pai->dir;
            if (tio != NULL && tio->cor == VERMELHO) {
                z->pai->cor = PRETO;
                tio->cor = PRETO;
                z->pai->pai->cor = VERMELHO;
                z = z->pai->pai;
            } else {
                if (z == z->pai->dir) {
                    z = z->pai;
                    raiz = rotacaoEsquerda(raiz, z);
                }
                z->pai->cor = PRETO;
                z->pai->pai->cor = VERMELHO;
                raiz = rotacaoDireita(raiz, z->pai->pai);
            }
        } else {
            TNo *tio = z->pai->pai->esq;
            if (tio != NULL && tio->cor == VERMELHO) {
                z->pai->cor = PRETO;
                tio->cor = PRETO;
                z->pai->pai->cor = VERMELHO;
                z = z->pai->pai;
            } else {
                if (z == z->pai->esq) {
                    z = z->pai;
                    raiz = rotacaoDireita(raiz, z);
                }
                z->pai->cor = PRETO;
                z->pai->pai->cor = VERMELHO;
                raiz = rotacaoEsquerda(raiz, z->pai->pai);
            }
        }
    }
    raiz->cor = PRETO;
    return raiz;
}

TNo* insere(TNo *raiz, int chave) {
    TNo *novo = criaNo(chave);
    TNo *y = NULL;
    TNo *x = raiz;

    while (x != NULL) {
        y = x;
        if (novo->chave < x->chave)
            x = x->esq;
        else
            x = x->dir;
    }

    novo->pai = y;

    if (y == NULL)
        raiz = novo;
    else if (novo->chave < y->chave)
        y->esq = novo;
    else
        y->dir = novo;

    return balancearInsercao(raiz, novo);
}

TNo* antecessor(TNo *ptr) {
    TNo *atual = ptr;
    while (atual->dir != NULL)
        atual = atual->dir;
    return atual;
}

TNo* balancearRemocao(TNo *raiz, TNo *x) {
    while (x != raiz && x->cor == PRETO) {
        if (x == x->pai->esq) {
            TNo *w = x->pai->dir;
            if (w->cor == VERMELHO) {
                w->cor = PRETO;
                x->pai->cor = VERMELHO;
                raiz = rotacaoEsquerda(raiz, x->pai);
                w = x->pai->dir;
            }
            if ((w->esq == NULL || w->esq->cor == PRETO) &&
                (w->dir == NULL || w->dir->cor == PRETO)) {
                w->cor = VERMELHO;
                x = x->pai;
            } else {
                if (w->dir == NULL || w->dir->cor == PRETO) {
                    if (w->esq != NULL) w->esq->cor = PRETO;
                    w->cor = VERMELHO;
                    raiz = rotacaoDireita(raiz, w);
                    w = x->pai->dir;
                }
                w->cor = x->pai->cor;
                x->pai->cor = PRETO;
                if (w->dir != NULL) w->dir->cor = PRETO;
                raiz = rotacaoEsquerda(raiz, x->pai);
                x = raiz;
            }
        } else {
            TNo *w = x->pai->esq;
            if (w->cor == VERMELHO) {
                w->cor = PRETO;
                x->pai->cor = VERMELHO;
                raiz = rotacaoDireita(raiz, x->pai);
                w = x->pai->esq;
            }
            if ((w->esq == NULL || w->esq->cor == PRETO) &&
                (w->dir == NULL || w->dir->cor == PRETO)) {
                w->cor = VERMELHO;
                x = x->pai;
            } else {
                if (w->esq == NULL || w->esq->cor == PRETO) {
                    if (w->dir != NULL) w->dir->cor = PRETO;
                    w->cor = VERMELHO;
                    raiz = rotacaoEsquerda(raiz, w);
                    w = x->pai->esq;
                }
                w->cor = x->pai->cor;
                x->pai->cor = PRETO;
                if (w->esq != NULL) w->esq->cor = PRETO;
                raiz = rotacaoDireita(raiz, x->pai);
                x = raiz;
            }
        }
    }
    x->cor = PRETO;
    return raiz;
}

TNo* retira(TNo *raiz, int chave) {
    TNo *z = raiz;
    TNo *x, *y;

    while (z != NULL && z->chave != chave) {
        if (chave < z->chave)
            z = z->esq;
        else
            z = z->dir;
    }

    if (z == NULL) {
        printf("\nA chave #%d nao esta na arvore!", chave);
        return raiz;
    }

    y = z;
    Cor corOriginal = y->cor;

    if (z->esq == NULL) {
        x = z->dir;
        if (x != NULL) x->pai = z->pai;
        if (z->pai == NULL)
            raiz = x;
        else if (z == z->pai->esq)
            z->pai->esq = x;
        else
            z->pai->dir = x;
        free(z);
    } else if (z->dir == NULL) {
        x = z->esq;
        if (x != NULL) x->pai = z->pai;
        if (z->pai == NULL)
            raiz = x;
        else if (z == z->pai->esq)
            z->pai->esq = x;
        else
            z->pai->dir = x;
        free(z);
    } else {
        y = antecessor(z->esq);
        corOriginal = y->cor;
        x = y->esq;
        if (y->pai == z) {
            if (x != NULL) x->pai = y;
        } else {
            if (x != NULL) x->pai = y->pai;
            y->pai->dir = x;
            y->esq = z->esq;
            y->esq->pai = y;
        }
        if (z->pai == NULL)
            raiz = y;
        else if (z == z->pai->esq)
            z->pai->esq = y;
        else
            z->pai->dir = y;
        y->dir = z->dir;
        y->dir->pai = y;
        y->cor = z->cor;
        free(z);
    }

    if (corOriginal == PRETO && x != NULL) {
        raiz = balancearRemocao(raiz, x);
    }

    return raiz;
}

void altera(TNo **raiz, int chaveAntiga, int chaveNova) {
    *raiz = retira(*raiz, chaveAntiga);
    *raiz = insere(*raiz, chaveNova);
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
    printf("%d (%s)\n", ptr->chave, ptr->cor == VERMELHO ? "R" : "P");

    imprimeEstrutura(ptr->esq, nivel + 1);
}

int main() {
    TNo *raiz;
    inicializa(&raiz);

    int opcao, valor, chaveAntiga, chaveNova;

    do {
        printf("\n\nMenu:");
        printf("\n1. Inserir");
        printf("\n2. Remover");
        printf("\n3. Alterar");
        printf("\n4. Mostrar arvore em estrutura");
        printf("\n5. Sair");
        printf("\nEscolha uma opcao: ");
        scanf("%d", &opcao);

        switch (opcao) {
            case 1:
                printf("Digite o valor a ser inserido: ");
                scanf("%d", &valor);
                raiz = insere(raiz, valor);
                break;
            case 2:
                printf("Digite o valor a ser removido: ");
                scanf("%d", &valor);
                raiz = retira(raiz, valor);
                break;
            case 3:
                printf("Digite o valor que deseja alterar: ");
                scanf("%d", &chaveAntiga);
                printf("Digite o novo valor: ");
                scanf("%d", &chaveNova);
                altera(&raiz, chaveAntiga, chaveNova);
                break;
            case 4:
                printf("Estrutura da arvore:\n");
                imprimeEstrutura(raiz, 0);
                break;
            case 5:
                printf("Saindo...\n");
                break;
            default:
                printf("Opcao invalida!\n");
        }
    } while (opcao != 5);

    return 0;
}
,
