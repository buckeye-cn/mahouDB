def compare(v1: tuple, v2: tuple) -> int:
    if (v1[0] < v2[0]):
        return -1
    elif (v1[0] > v2[0]):
        return 1
    else:
        return 0 if v1[1] == v2[1] else -1 if v1[1] < v2[1] else 1

class Node():
    def __init__(self,
                 data: tuple,
                 is_black,
                 parent=None,
                 left=None,
                 right=None):
        """Constructor for a Red-Black Tree Node

        Keyword arguments:
        data -- the data in the node
        is_black -- color of the node, True for black, False for Red
        parent -- parent node
        left -- left subtree
        right -- right subtree
        """
        self._data = data
        self._parent = parent
        self._left = left
        self._right = right
        self._is_black = is_black

    def print_node_dot(self):
        node_name = "node%s" % id(self)
        color = "black" if self._is_black else "red"
        print(""" %s [ label="%s", fillcolor="%s" ];""" % (node_name, self._data, color))

        if self._left != None:
            self._left.print_node_dot()
            print(""" %s -> node%s;""" % (node_name, id(self._left)))
        else:
            print(""" NoneL%s [ shape="box", label="NIL", fontsize="10", fillcolor="black" ];""" % (node_name))
            print(""" %s -> NoneL%s;""" % (node_name, node_name))
        if self._right != None:
            self._right.print_node_dot()
            print(""" %s -> node%s;""" % (node_name, id(self._right)))
        else:
            print(""" NoneR%s [ shape="box", label="NIL", fontsize="10", fillcolor="black" ];""" % (node_name))
            print(""" %s -> NoneR%s;""" % (node_name, node_name))

    def contains(self, data):
        if self._data == data:
            return True
        elif data < self._data:
            if self._left == None:
                return False
            else:
                return self._left.contains(data)
        else:
            if self._right == None:
                return False
            else:
                return self._right.contains(data)

    def min(self):
        check = True
        copy = self
        copyP = self._parent
        while check:
            if copy._left != None:
                copyP = copy
                copy = copy._left
            else:
                check = False
            copy._parent = copyP
        return copy

    def change_color(self):
        left_check = True
        right_check = True
        left = self._left
        leftP = self
        right = self._right
        rightP = self
        if left_check:
            if left._is_black:
                left._is_black = False
                left_check = False
            else:
                left._parent = leftP
                change_color(left)
        if right_check:
            if right._is_black:
                right._is_black = False
                right_check = False
            else:
                right._parent = rightP
                change_color(right)

class Tree():
    """A Red Black Tree for indexing

    root -- the root of the tree
    insert(self, data) -- insert a new data into the tree
    delete(self, data) -- delete a node given the data
    find(self, data) -- find a node given the data
    """

    def __init__(self):
        """Constructor for a Red-Black Tree, with an empty tree"""
        self.root = None

    def print_tree_dot(self):
        print("digraph {")
        print(""" node [ style="filled", fontcolor="white" ]""")
        if self.root != None:
            self.root.print_node_dot()
        print("}")

    def contains(self, data):
        if self.root == None:
            return False
        else:
            return self.root.contains(data)

    def left_rotate(self, node):
        new_node = node._right
        if node == self.root:
            self.root = new_node
        else:
            if node == node._parent._left:
                node._parent._left = new_node
            else:
                node._parent._right = new_node
        new_node._parent = node._parent
        node._right = new_node._left
        if new_node._left != None:
            new_node._left._parent = node
        new_node._left = node
        node._parent = new_node

    def right_rotate(self, node):
        new_node = node._left
        if node == self.root:
            self.root = new_node
        else:
            if node == node._parent._left:
                node._parent._left = new_node
            else:
                node._parent._right = new_node
        new_node._parent = node._parent
        node._left = new_node._right
        if new_node._right != None:
            new_node._right._parent = node
        new_node._right = node
        node._parent = new_node

    def insert(self, data):
        # reference: CLRS
        if self.root == None:
            self.root = Node(data, True, None)
        else:
            x = self.root
            done = False
            while not done:
                if data < x._data:
                    if x._left == None:
                        x._left = Node(data, False, x)
                        done = True
                    x = x._left
                else:
                    if x._right == None:
                        x._right = Node(data, False, x)
                        done = True
                    x = x._right
            while x._parent != None and x._parent._parent != None and not x._parent._is_black:
                parent = x._parent
                grandparent = parent._parent
                sibling_of_parent = None
                if parent == grandparent._left:
                    sibling_of_parent = grandparent._right
                elif parent == grandparent._right:
                    sibling_of_parent = grandparent._left
                # Case 1
                if sibling_of_parent != None and not sibling_of_parent._is_black:
                    parent._is_black = True
                    sibling_of_parent._is_black = True
                    grandparent._is_black = False
                    x = grandparent
                # Case 2
                elif parent == grandparent._left:
                    if x == parent._right:  # Case 2.5
                        self.left_rotate(parent)
                        # child became parent
                        temp = x
                        x = parent
                        parent = temp
                    parent._is_black = True
                    grandparent._is_black = False
                    # Perform right rotation on grandparent
                    self.right_rotate(grandparent)
                # Case 3
                elif parent == grandparent._right:
                    if x == parent._left:  # Case3.5
                        self.right_rotate(parent)
                        temp = x
                        x = parent
                        parent = temp
                    parent._is_black = True
                    grandparent._is_black = False
                    # Perform left rotation on grandparent
                    self.left_rotate(grandparent)
                # After running Case 2 or 3(right-hand version of 2),
                # parent(x._parent) will be black, the original grandparent and x will be red,
                # the original sibling_of_parent is black since Case 1 is not the case,
                # and the original sibling of x(now a child of original grandparent) is black if its parent is red,
                # which satisfies the rules.
            self.root._is_black = True

    def rb_transplant(self, n1, n2):
        if n1._parent == None:
            self.root = n2
        elif n1 == n1._parent._left:
            n1._parent._left = n2
        else:
            n1._parent._right = n2
        n2._parent = n1._parent

    def find_node(self, data):
        x = self.root
        target = x
        while target._data != data:
            if data < target._data:
                target = x._left
                target._paretn = x
                x = x._left
            else:
                target = x._right
                target._parent = x
                x = x._right
        return target

    def delete(self, data):
        del_node = self.find_node(data)
        y = del_node
        y._parent = del_node._parent
        y_original_color = y._is_black
        if del_node._left == None and del_node._right == None:
            if del_node._parent == None and del_node._is_black:
                self.root = None
            elif del_node._is_black and not del_node._parent._is_black:
                del_node._parent._is_black = True
                if del_node == del_node._parent._right:
                    del_node._parent._left._is_black = False
                    del_node._parent._right = None
                else:
                    del_node._parent._right._is_black = False
                    del_node._parent._left = None
            elif not del_node._is_black:
                if del_node == del_node._parent._right:
                    del_node._parent._right = None
                else:
                    del_node._parent._left = None
            elif del_node._is_black and del_node._parent._is_black:
                if del_node == del_node._parent._right:
                    if del_node._parent._left != None and not del_node._parent._left._is_black:
                        del_node._parent._left._is_black = True
                        del_node._parent._left._right._is_black = False
                        temp = del_node._parent
                        temp._parent._parent = del_node._parent._parent
                        del_node._parent._right = None
                        self.right_rotate(temp)
                    elif del_node._parent._left != None and del_node._parent._left._is_black:
                        temp1 = del_node._parent
                        temp1._parent = del_node._parent._parent
                        del_node._parent._right = None
                        copyTemp = temp1
                        coypTemp = temp1._parent
                        if copyTemp != None and copyTemp._parent != None:
                            if not copyTemp._parent._right._is_black:
                                copyTemp._parent._right.change_color()
                            copyTemp._parent._right._is_black = False
                            temp2 = copyTemp._parent
                            temp2 = copyTemp._parent._parent
                            copyTemp = temp2
                            if temp2 != None:
                                copyTemp._parent = temp2._parent
                        self.right_rotate(temp1)
                        temp1._is_black = False
                else:
                    if del_node._parent._right != None and not del_node._parent._right._is_black:
                        del_node._parent._right._is_black = True
                        del_node._parent._right._left._is_black = False
                        temp = del_node._parent
                        temp._parent._parent = del_node._parent._parent
                        del_node._parent._left = None
                        self.left_rotate(temp)
                    elif del_node._parent._right != None and del_node._parent._right._is_black:
                        temp1 = del_node._parent
                        temp1._parent = del_node._parent._parent
                        del_node._parent._left = None
                        copyTemp = temp1
                        coypTemp = temp1._parent
                        if copyTemp != None and copyTemp._parent != None:
                            if not copyTemp._parent._left._is_black:
                                copyTemp._parent._left.change_color()
                            copyTemp._parent._left._is_black = False
                            temp2 = copyTemp._parent
                            temp2 = copyTemp._parent._parent
                            copyTemp = temp2
                            if temp2 != None:
                                copyTemp._parent = temp2._parent
                        self.left_rotate(temp1)
                        temp1._is_black = False
        else:
            if del_node._left == None:
                x = del_node._right
                if del_node != None and del_node._right != None:
                   self.rb_transplant(del_node, del_node._right)
            elif del_node._right == None:
               x = del_node._left
               if del_node != None and del_node._left != None:
                   self.rb_transplant(del_node, del_node._left)
            else:
                y = del_node._right.min()
                j = del_node._right.min()._parent
                y_original_color = y._is_black
                x = y._right
                if y._parent == del_node and x != None:
                    x._parent = y
                elif y._parent == del_node and del_node._is_black and del_node._parent._is_black:
                    if del_node == del_node._parent._right:
                        if del_node._parent._left != None and del_node._parent._left._is_black:
                            del_node._parent._left._is_black = False
                            del_node._right._is_black = False
                    else:
                        if del_node._parent._right != None and del_node._parent._right._is_black:
                            del_node._parent._right._is_black = False
                            del_node._left._is_black = False
                else:
                   if y._right != None:
                       self.rb_transplant(y, y._right)
                       y._right = del_node._right
                       y._right._parent = y
                   else:
                       temp = y
                       temp._parent = y._parent
                       if y == y._parent._left:
                           temp._parent._left = None
                       else:
                           temp._parent._right = None
                       y._right = del_node._right
                       if y._right != None:
                          y._right._parent = y
                self.rb_transplant(del_node,y)
                y._left = del_node._left
                y._left._parent = y
                y._is_black = del_node._is_black
                if y_original_color and x == None:
                    self.left_rotate(j)
                    self.left_rotate(j)
                    j._is_black = False
                    temp._left._is_black = False
                    temp._is_black = True
            if y_original_color and x != None:
                self.rb_delete_fixup(x)

    def rb_delete_fixup(self, x):
        while x != self.root and x._is_black and x._left != None and x._right != None:
            if x == x._parent._left:
                w = x._parent._right
                # case 1
                if not w._is_black:
                    w._is_black = True
                    x._parent._is_black = False
                    self.left_rotate(x._parent)
                    w = x._parent._right
                # case 2
                if w._left._is_black and w._right._is_black:
                    w._is_black = False
                    x = x._parent
                # case 3
                else:
                    if w._right._is_black:
                        w._left._is_black = True
                        w._is_black = False
                        self.right_rotate(w)
                        w = x._parent._right
                # case 4
                    w._is_black = x._parent._is_black
                    x._parent._is_black = True
                    w._right._is_black = True
                    self.left_rotate(x._parent)
                    x = self.root
            else:
                w = x._parent._left
                if not w._is_black:
                    w._is_black = True
                    x._parent._is_black = False
                    self.right_rotate(x._parent)
                    w = x._parent._left
                if w._right._is_black and w._left._is_black:
                    w._is_black = False
                    x = x._parent
                else:
                    if w._left._is_black:
                         w._right._is_black = True
                         w._is_black = False
                         self.left_rotate(w)
                         w = x._parent._left
                    w._is_black = x._parent._is_black
                    x._parent._is_black = True
                    w._left._is_black = True
                    self.right_rotate(x._parent)
                    x = self.root
        if x != None:
           x._is_black = True

    def find(self, data):
        pass


if __name__ == '__main__':
    tree = Tree()

    tree.insert(10)
    tree.insert(3)
    tree.insert(14)
    tree.insert(17)
    tree.insert(24)
    tree.insert(42)
    tree.insert(0)
    tree.insert(25)
    tree.insert(43)
    tree.insert(45)
    tree.insert(46)
    tree.insert(44)
    tree.insert(26)
    tree.insert(222)
    tree.insert(90)
    tree.insert(55)
    #tree.delete(24)
    #tree.delete(44)
    #tree.delete(45)
    #tree.delete(43)
    #tree.delete(10)
    #tree.delete(14)
    #tree.delete(42)
    #tree.delete(46)
    #tree.delete(17)
    #tree.delete(26)
    #tree.delete(3)
    #tree.delete(0)
    #tree.delete(25)
    tree.delete(90)
    tree.print_tree_dot()
