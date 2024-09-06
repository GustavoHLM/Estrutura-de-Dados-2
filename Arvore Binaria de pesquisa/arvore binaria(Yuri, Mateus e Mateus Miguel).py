import turtle

class TreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if self.root is None:
            self.root = TreeNode(key)
            self._redraw_node(self.root, 0, 0, None)
        else:
            self._insert(self.root, key, 0, 0, 100)

    def _insert(self, node, key, x, y, offset):
        if key < node.key:
            if node.left is None:
                node.left = TreeNode(key)
                self._redraw_node(node.left, x - offset, y - 60, (x, y))
            else:
                self._insert(node.left, key, x - offset, y - 60, offset // 2)
        else:
            if node.right is None:
                node.right = TreeNode(key)
                self._redraw_node(node.right, x + offset, y - 60, (x, y))
            else:
                self._insert(node.right, key, x + offset, y - 60, offset // 2)

    def delete(self, key):
        self.root, _ = self._delete(self.root, key)
        self.redraw()

    def _delete(self, node, key):
        if node is None:
            return node, None
        
        if key < node.key:
            node.left, deleted = self._delete(node.left, key)
        elif key > node.key:
            node.right, deleted = self._delete(node.right, key)
        else:
            if node.left is None:
                return node.right, node
            elif node.right is None:
                return node.left, node
            temp = self._min_value_node(node.right)
            node.key = temp.key
            node.right, _ = self._delete(node.right, temp.key)
            deleted = node

        return node, deleted

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current
    def redraw(self):
        turtle.clear()
        self._redraw(self.root, 0, 0, 100)
        turtle.update()

    def _redraw(self, node, x, y, offset):
        if node is not None:
            self._redraw_node(node, x, y, None)
            if node.left:
                draw_connection(x, y, x - offset, y - 60)
                self._redraw(node.left, x - offset, y - 60, offset // 2)
            if node.right:
                draw_connection(x, y, x + offset, y - 60)
                self._redraw(node.right, x + offset, y - 60, offset // 2)

    def _redraw_node(self, node, x, y, parent_coords):
        turtle.penup()
        turtle.goto(x, y)
        turtle.pendown()
        
        if parent_coords:
            draw_connection(parent_coords[0], parent_coords[1], x, y)
        
        turtle.color("blue")
        turtle.begin_fill()
        turtle.circle(20)
        turtle.end_fill()
        turtle.color("black")
        
        turtle.penup()
        turtle.goto(x, y - 10)
        turtle.write(node.key, align="center", font=("Arial", 12, "normal"))
        turtle.penup()

def draw_connection(x1, y1, x2, y2):
    turtle.pencolor("black")
    turtle.pensize(2)
    turtle.penup()
    turtle.goto(x1, y1)
    turtle.pendown()
    turtle.goto(x2, y2)
    turtle.penup()

def draw_menu():
    turtle.penup()
    turtle.goto(-200, 250)
    turtle.pendown()
    turtle.color("black")
    turtle.write("Menu:", align="left", font=("Arial", 16, "bold"))
    turtle.penup()
    turtle.goto(-200, 220)
    turtle.pendown()
    turtle.write("1. Inserir", align="left", font=("Arial", 14, "normal"))
    turtle.penup()
    turtle.goto(-200, 190)
    turtle.pendown()
    turtle.write("2. Remover", align="left", font=("Arial", 14, "normal"))
    turtle.penup()
    turtle.goto(-200, 160)
    turtle.pendown()
    turtle.write("3. Sair", align="left", font=("Arial", 14, "normal"))
    def get_input(prompt):
    return turtle.textinput("Input", prompt)

def main():
    bst = BinarySearchTree()
    turtle.speed(0)
    turtle.hideturtle()
    turtle.tracer(0, 0)
    draw_menu()
    turtle.update()

    def continue_prompt():
        choice = get_input("Escolha uma opção (1, 2 ou 3):")
        if choice == '1':
            values = get_input("Digite os valores a serem inseridos, separados por vírgula:")
            if values:
                for value in values.split(','):
                    bst.insert(int(value.strip()))
        elif choice == '2':
            value = get_input("Digite o valor a ser removido:")
            if value:
                bst.delete(int(value.strip()))
        elif choice == '3':
            turtle.bye()
            return
        else:
            turtle.penup()
            turtle.goto(-200, 130)
            turtle.pendown()
            turtle.write("Opção inválida. Tente novamente.", align="left", font=("Arial", 14, "normal"))
            turtle.update()
        
        turtle.ontimer(continue_prompt, 500)

    continue_prompt()
    turtle.done()

if __name__ == "__main__":
    main()