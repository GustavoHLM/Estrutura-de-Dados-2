import java.util.Scanner;

public class BuscaBinariaRecursiva {

    // Função para realizar a busca binária recursiva
    public static int buscaBinariaRecursiva(int[] vetor, int inicio, int fim, int item) {

        // Casos base: Item não encontrado ou vetor vazio
        if (inicio > fim) {
            System.out.println("Item não encontrado no array.");
            return -1;
        }

        // Exibe o intervalo atual de busca
        System.out.println("Intervalo: [" + inicio + ", " + fim + "]");

        // Calcula o índice do meio
        int meio = (inicio + fim) / 2;

        // Se o item for encontrado, retorna seu índice
        if (vetor[meio] == item) {
            System.out.println("Item encontrado na posição " + meio + ".");
            return meio;
        }

        // Exibe o valor do elemento do meio
        System.out.println("Elemento do meio: " + vetor[meio]);

        // Chamadas recursivas para procurar no subvetor apropriado
        if (vetor[meio] < item) {
            // Procura no subvetor da direita
            return buscaBinariaRecursiva(vetor, meio + 1, fim, item);
        } else {
            // Procura no subvetor da esquerda
            return buscaBinariaRecursiva(vetor, inicio, meio - 1, item);
        }
    }

    public static void main(String[] args) {

        // Array a ser pesquisado
        int[] vetor = {1, 3, 5, 7, 9, 11, 13, 15, 18, 19, 20, 22, 23, 24, 27, 29, 30, 31, 34, 38, 41, 42, 43, 45, 47, 48, 49, 51, 54, 56, 58, 61, 64, 65, 67, 69, 70, 72, 74, 76, 78, 79, 81, 83, 85, 89, 92, 95, 98, 99};

        Scanner scanner = new Scanner(System.in);

        try {
            // Solicita o item a ser pesquisado
            System.out.print("Digite o item a ser pesquisado: ");
            int item = scanner.nextInt();

            // Realiza a busca binária recursiva
            int indice = buscaBinariaRecursiva(vetor, 0, vetor.length - 1, item);

            // Exibe o array com o item encontrado marcado com asterisco
            if (indice != -1) {
                System.out.print("\n{");
                for (int i = 0; i < vetor.length; i++) {
                    if (i == indice) {
                        System.out.print("*" + vetor[i] + "* ");
                    } else {
                        System.out.print(vetor[i] + " ");
                    }
                }
                System.out.println("}");
            }
        } finally {
            scanner.close();
        }
    }
}