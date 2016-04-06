class FieldTree:
    class Node:
        def __init__(self, name, children=None, next=None):
            self.name = name
            if children is None:
                self.children = []
            else:
                self.children = children
            self.next = next

        def __str__(self):
            return str(self.name)

    def __init__(self, root):
        self.__root = self.Node(root)
        self.stringRepr = ''

    def str_inner(self, node):
        self.stringRepr += str(node)
        if len(node.children) > 0:
            self.stringRepr += '('
        for i, child in enumerate(node.children):
            self.str_inner(child)
            if i is not len(node.children) - 1:
                self.stringRepr += ', '
        if len(node.children) > 0:
            self.stringRepr += ')'
        return self.stringRepr

    def __str__(self):
        result = self.str_inner(self.root)
        self.stringRepr = ''
        return result

    @property
    def root(self):
        return self.__root

    @root.setter
    def root(self, root):
        self.__root = root

    def search_inner(self, node, search_value):
        if node.name == search_value:
            return node
        for child in node.children:
            found = self.search_inner(child, search_value)
            if found is not None:
                return found
        return None

    def search(self, search_value):
        return self.search_inner(self.root, search_value)

    def add_child(self, parentName, nodeName):
        if self.search(nodeName) is not None:
            raise Exception('Elements must be unique: ', nodeName)
        found = self.search(parentName)
        if found is not None:
            new_child = self.Node(nodeName)
            found.children.append(new_child)
        else: raise Exception('Cannot find parent element: ', parentName)


