package binaria;

public class BuscaBinaria {

    // Função de busca binária recursiva
    public static int buscaBinaria(int[] array,int alvo) {
        return buscaBinariaRecursiva(array, alvo, 0, array.length- 1);
    }

    private static int buscaBinariaRecursiva(int[] array,int alvo,int inicio, int fim) {
        if (inicio>fim) {
            return -1; // Elemento não encontrado
        }

        int meio = (inicio+fim) / 2;

        if (array[meio]==alvo) {
            return meio; // Elemento encontrado
        } else if (array[meio] < alvo) {
            return buscaBinariaRecursiva(array, alvo, meio + 1, fim); // Busca na metade direita
        } else {
            return buscaBinariaRecursiva(array, alvo, inicio, meio - 1); // Busca na metade esquerda
        }
    }

    public static void main(String[] args) {
        int[] array = {1, 3, 5, 7, 9, 11, 13, 15, 17, 19};
        int alvo=8;
        int indice = buscaBinaria(array, alvo);
        if (indice != -1) {
            System.out.println("Elemento " + alvo +" encontrado no indice " + indice);
        } else {
            System.out.println("Elemento " + alvo +" nao encontrado no array");
        }
    }
}
