class FieldTree:
    class Node:
        def __init__(self, name, child=None, next=None):
            self.name = name
            self.child = child
            self.next = next

        def __str__(self):
            return str(self.name)

        def get_children(self):
            children = []
            current = self.child
            while current is not None:
                children.append(current)
                current = current.next
            return children

    def __init__(self, root):
        self.__root = self.Node(root)

    def __str__(self):
        def str_inner(node, result):
            if node is None:
                result += ')'
                return result
            for child in node.get_children():
                result += str(child)
                result += ','
                str_inner(child, result)
            return result
        return str_inner(self.root, '(')

    @property
    def root(self):
        return self.__root

    @root.setter
    def root(self, root):
        self.__root = root

    def search(self, search_value):
        def search_inner(node):
            if node is None:
                return None
            if search_value == node.name:
                return node
            [self.search_inner(child) for child in node.get_children()]
        return search_inner(self.root)

    def add_child(self, parent, node):
        found = self.search(parent)
        if found is not None:
            new_child = self.Node(node)
            children = found.get_children()
            if len(children) == 0:
                found.child = new_child
            else:
                children[len(children) - 1].next = new_child
        else: raise Exception('Cannot find parent element: ', parent)


