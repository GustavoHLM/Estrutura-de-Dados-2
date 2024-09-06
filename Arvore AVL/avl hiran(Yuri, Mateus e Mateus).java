public class Node {
    int key;
    Node left, right;
    int height;

    public Node(int item) {
        key = item;
        left = right = null;
        height = 1;
    }
}
import java.io.*;
import java.util.*;
import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.image.BufferedImage;

public class AVLTree {
    private Node root;

    // Métodos para obter a altura e balanceamento
    private int height(Node N) {
        return N == null ? 0 : N.height;
    }

    private int getBalance(Node N) {
        return N == null ? 0 : height(N.left) - height(N.right);
    }

    // Rotação à direita
    private Node rightRotate(Node y) {
        Node x = y.left;
        Node T2 = x.right;

        x.right = y;
        y.left = T2;

        y.height = Math.max(height(y.left), height(y.right)) + 1;
        x.height = Math.max(height(x.left), height(x.right)) + 1;

        return x;
    }

    // Rotação à esquerda
    private Node leftRotate(Node x) {
        Node y = x.right;
        Node T2 = y.left;

        y.left = x;
        x.right = T2;

        x.height = Math.max(height(x.left), height(x.right)) + 1;
        y.height = Math.max(height(y.left), height(y.right)) + 1;

        return y;
    }

    // Inserção
    public void insert(int key) {
        root = insertRec(root, key);
    }

    private Node insertRec(Node node, int key) {
        if (node == null) {
            return new Node(key);
        }

        if (key < node.key) {
            node.left = insertRec(node.left, key);
        } else if (key > node.key) {
            node.right = insertRec(node.right, key);
        } else {
            return node; // Duplicatas não são permitidas
        }

        node.height = Math.max(height(node.left), height(node.right)) + 1;

        int balance = getBalance(node);

        // Rotacionar se necessário
        if (balance > 1 && key < node.left.key) {
            return rightRotate(node);
        }

        if (balance < -1 && key > node.right.key) {
            return leftRotate(node);
        }

        if (balance > 1 && key > node.left.key) {
            node.left = leftRotate(node.left);
            return rightRotate(node);
        }

        if (balance < -1 && key < node.right.key) {
            node.right = rightRotate(node.right);
            return leftRotate(node);
        }

        return node;
    }

    // Remoção
    public void remove(int key) {
        root = removeRec(root, key);
    }

    private Node removeRec(Node root, int key) {
        if (root == null) {
            return root;
        }

        if (key < root.key) {
            root.left = removeRec(root.left, key);
        } else if (key > root.key) {
            root.right = removeRec(root.right, key);
        } else {
            if ((root.left == null) || (root.right == null)) {
                Node temp = null;
                if (temp == root.left) {
                    temp = root.right;
                } else {
                    temp = root.left;
                }

                if (temp == null) {
                    temp = root;
                    root = null;
                } else {
                    root = temp;
                }
            } else {
                Node temp = minValueNode(root.right);
                root.key = temp.key;
                root.right = removeRec(root.right, temp.key);
            }
        }

        if (root == null) {
            return root;
        }

        root.height = Math.max(height(root.left), height(root.right)) + 1;

        int balance = getBalance(root);

        if (balance > 1 && getBalance(root.left) >= 0) {
            return rightRotate(root);
        }

        if (balance > 1 && getBalance(root.left) < 0) {
            root.left = leftRotate(root.left);
            return rightRotate(root);
        }

        if (balance < -1 && getBalance(root.right) <= 0) {
            return leftRotate(root);
        }

        if (balance < -1 && getBalance(root.right) > 0) {
            root.right = rightRotate(root.right);
            return leftRotate(root);
        }

        return root;
    }

    private Node minValueNode(Node node) {
        Node current = node;
        while (current.left != null) {
            current = current.left;
        }
        return current;
    }

    // Armazenar a árvore em um arquivo .txt
    public void saveToFile(String filename) throws IOException {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filename))) {
            saveToFileRec(root, writer);
        }
    }

    private void saveToFileRec(Node node, BufferedWriter writer) throws IOException {
        if (node != null) {
            saveToFileRec(node.left, writer);
            writer.write(node.key + "\n");
            saveToFileRec(node.right, writer);
        }
    }

    // Carregar a árvore a partir de um arquivo .txt
    public void loadFromFile(String filename) throws IOException {
        try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
            String line;
            while ((line = reader.readLine()) != null) {
                insert(Integer.parseInt(line));
            }
        }
    }

    // Gerar uma imagem da árvore
    public void generateImage(String filename) throws IOException {
        int width = 800;
        int height = 600;
        BufferedImage image = new BufferedImage(width, height, BufferedImage.TYPE_INT_RGB);
        Graphics2D g2d = image.createGraphics();
        g2d.setPaint(Color.WHITE);
        g2d.fillRect(0, 0, width, height);
        g2d.setPaint(Color.BLACK);
        drawTree(g2d, root, width / 2, 30, 200);
        g2d.dispose();
        ImageIO.write(image, "png", new File(filename));
    }

    private void drawTree(Graphics2D g2d, Node node, int x, int y, int xOffset) {
        if (node != null) {
            g2d.drawString(Integer.toString(node.key), x, y);
            if (node.left != null) {
                g2d.drawLine(x, y, x - xOffset, y + 50);
                drawTree(g2d, node.left, x - xOffset, y + 50, xOffset / 2);
            }
            if (node.right != null) {
                g2d.drawLine(x, y, x + xOffset, y + 50);
                drawTree(g2d, node.right, x + xOffset, y + 50, xOffset / 2);
            }
        }
    }
}
