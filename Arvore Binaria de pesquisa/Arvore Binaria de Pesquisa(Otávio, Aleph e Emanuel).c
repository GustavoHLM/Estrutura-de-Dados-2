#include <stdio.h>
#include <stdlib.h>

typedef struct no {
    struct no *esq, *dir;
    int chave;
}TNo;

void inicializa(TNo**ptr) {
    *ptr = NULL;
}

void insere(TNo **ptr, int chave) {
    if (*ptr == NULL) {
        *ptr = (TNo *)malloc(sizeof(TNo));
        (*ptr)->esq = NULL;
        (*ptr)->dir = NULL;
        (*ptr)->chave = chave;
    } else {
        if (chave < (*ptr)->chave)
            insere(&(*ptr)->esq, chave);
        else if (chave > (*ptr)->chave)
            insere(&(*ptr)->dir, chave);
    }
}

void antecessor(TNo *q,TNo **r) {
    if ((*r)->dir != NULL)
        antecessor(q, &(*r)->dir);
    else {
        q->chave = (*r)->chave;
        q = (*r);
        *r = (*r)->esq;
        free(q);
    }
}

void retira(TNo **ptr, int chave) {
    if (*ptr == NULL) {
        printf("\nA chave #%d nao esta na arvore!", chave);
    } else if (chave < (*ptr)->chave) {
        retira(&(*ptr)->esq, chave);
    } else if (chave > (*ptr)->chave) {
        retira(&(*ptr)->dir, chave);
    } else {
        TNo *aux = *ptr;
        if ((*ptr)->dir == NULL) {
            *ptr = (*ptr)->esq;
            free(aux);
        } else if ((*ptr)->esq == NULL) {
            *ptr = (*ptr)->dir;
            free(aux);
        } else {
            antecessor((*ptr), &(*ptr)->esq);
        }
    }
}

void altera(TNo *ptr, int chaveAntiga, int chaveNova) {
    retira(&ptr, chaveAntiga);
    insere(&ptr, chaveNova);
}

void imprimeEstrutura(TNo *ptr, int nivel) {
	int i;
    if (ptr==NULL) {
        return;
    }

    imprimeEstrutura(ptr->dir, nivel+1);

    for ( i = 0; i < nivel; i++) {
        printf("    ");
    }
    printf("%d\n", ptr->chave);

    imprimeEstrutura(ptr->esq, nivel + 1);
}

int main() {
    TNo *ptr;
    inicializa(&ptr);

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
                insere(&ptr, valor);
                break;
            case 2:
                printf("Digite o valor a ser removido: ");
                scanf("%d", &valor);
                retira(&ptr, valor);
                break;
            case 3:
                printf("Digite o valor que deseja alterar: ");
                scanf("%d", &chaveAntiga);
                printf("Digite o novo valor: ");
                scanf("%d", &chaveNova);
                altera(ptr, chaveAntiga, chaveNova);
                break;
            case 4:
                printf("Estrutura da arvore:\n");
                imprimeEstrutura(ptr, 0);
                break;
            case 5:
                printf("Saindo...\n");
                break;
            default:
                printf("Opcao invalida!\n");
        }
    } while(opcao != 5);

    return 0;
}

