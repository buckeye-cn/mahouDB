def compare(v1: tuple, v2: tuple) -> int:
    if (v1[0] < v2[0]):
        return -1
    elif (v1[0] > v2[0]):
        return 1
    else:
        return 0 if v1[1] == v2[1] else -1 if v1[1] < v2[1] else 1

def tree_values(root_node):
    return_value = []
    task_list = []
    if not root_node is None and not root_node._data is None:
        task_list.append(root_node)
    while len(task_list) > 0:
        current_node = task_list.pop()
        append_or_extend(return_value, current_node._data[1])
        if not current_node._left is None and not current_node._left._data is None:
            task_list.append(current_node._left)
        if not current_node._right is None and not current_node._right._data is None:
            task_list.append(current_node._right)
    return return_value
        
def append_or_extend(l: list, item):
    if type(item) is list:
        l.extend(item)
    else:
        l.append(item)
        
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

        if not self._left._data is None:
            self._left.print_node_dot()
            print(""" %s -> node%s;""" % (node_name, id(self._left)))
        else:
            print(""" NoneL%s [ shape="box", label="NIL", fontsize="10", fillcolor="black" ];""" % (node_name))
            print(""" %s -> NoneL%s;""" % (node_name, node_name))
        if not self._right._data is None:
            self._right.print_node_dot()
            print(""" %s -> node%s;""" % (node_name, id(self._right)))
        else:
            print(""" NoneR%s [ shape="box", label="NIL", fontsize="10", fillcolor="black" ];""" % (node_name))
            print(""" %s -> NoneR%s;""" % (node_name, node_name))

    def contains(self, key):
        if self._data[0] == key:
            return True
        elif key < self._data[0]:
            if self._left._data is None:
                return False
            else:
                return self._left.contains(key)
        else:
            if self._right._data is None:
                return False
            else:
                return self._right.contains(key)

    def min(self):
        check = True
        copy = self
        while check:
            if not copy._left._data is None:
                copy = copy._left
            else:
                check = False
        return copy

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
        if not self.root is None:
            self.root.print_node_dot()
        print("}")

    def contains(self, key):
        if self.root is None:
            return False
        else:
            return self.root.contains(key)

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
        new_node._right._parent = node
        new_node._right = node
        node._parent = new_node

    def insert(self, data):
        if self.root is None:
            self.root = Node(data, True, None)
            self.root._left = Node(None, True, self.root)
            self.root._right = Node(None, True, self.root)
        else:
            x = self.root
            done = False
            while not done:
                if data[0] < x._data[0]:
                    x = x._left
                else:
                    x = x._right
                if x._data is None:
                    x._data = data
                    x._is_black = False
                    x._left = Node(None, True, x)
                    x._right = Node(None, True, x)
                    done = True     
            while not x._parent is None and not x._parent._parent is None and not x._parent._is_black:
                parent = x._parent
                grandparent = parent._parent
                sibling_of_parent = None
                if parent == grandparent._left:
                    sibling_of_parent = grandparent._right
                elif parent == grandparent._right:
                    sibling_of_parent = grandparent._left
                # Case 1
                if not sibling_of_parent._data is None and not sibling_of_parent._is_black:
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
        if n1._parent is None:
            self.root = n2
        elif n1 == n1._parent._left:
            n1._parent._left = n2
        else:
            n1._parent._right = n2
        n2._parent = n1._parent

    def find_node(self, data):
        target = self.root
        while target._data[0] != data:
            if data < target._data[0]:
                target = target._left
            else:
                target = target._right
        return target

    def delete(self, data):
        del_node = self.find_node(data)
        removed_color = del_node._is_black
        x = None
        if del_node._left._data is None:
            x = del_node._right
            self.rb_transplant(del_node, del_node._right)
        elif del_node._right._data is None:
            x = del_node._left
            self.rb_transplant(del_node, del_node._left)
        else:
            min_node = del_node._right.min()
            removed_color = min_node._is_black
            x=min_node._right
            self.rb_transplant(min_node, min_node._right) # The left most node does not have a left child.
            self.rb_transplant(del_node, min_node)
            
            min_node._left=del_node._left
            min_node._left._parent = min_node
            min_node._right=del_node._right
            min_node._right._parent = min_node
            
            min_node._is_black=del_node._is_black # Substitute the color
        if removed_color:
            self.rb_delete_fixup(x)
        if self.root is None or self.root._data is None:
            self.root = None

    def rb_delete_fixup(self, x):
        # heavily rely on the algorithm on CLRS
        while x != self.root and x._is_black:
            if x == x._parent._left and not x._parent._right._data is None:
                w = x._parent._right
                # case 1
                if not w._is_black:
                    w._is_black = True
                    x._parent._is_black = False
                    self.left_rotate(x._parent)
                    w = x._parent._right
                # case 2
                if not w._data is None and w._left._is_black and w._right._is_black:
                    w._is_black = False
                    x = x._parent
                # case 3
                elif not w._data is None:
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
            elif x == x._parent._right and not x._parent._left._data is None:
                w = x._parent._left
                if not w._is_black:
                    w._is_black = True
                    x._parent._is_black = False
                    self.right_rotate(x._parent)
                    w = x._parent._left
                if not w._data is None and w._right._is_black and w._left._is_black:
                    w._is_black = False
                    x = x._parent
                elif not w._data is None:
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
        if not x is None:
            x._is_black = True

    def find(self, data):
        return_value = None
        if not data is None:
            done = False
            current_node = self.root
            while not current_node is None and not current_node._data is None and not done:
                current_data = current_node._data[0]
                if current_data == data:
                    return_value = current_node._data[1]
                    done = True
                elif data < current_data:
                    current_node = current_node._left
                else:
                    current_node = current_node._right
        return return_value
    
    def lower_bound(self, value):
        return_value = []
        current_node = self.root
        while not current_node is None and not current_node._data is None:
            current_data = current_node._data
            if current_data[0] >= value:
                append_or_extend(return_value, current_data[1])
                return_value.extend(tree_values(current_node._right))
                current_node = current_node._left
            else:
                current_node = current_node._right
        return return_value
        
    def upper_bound(self, value):
        return_value = []
        current_node = self.root
        while not current_node is None and not current_node._data is None:
            current_data = current_node._data
            if current_data[0] <= value:
                append_or_extend(return_value, current_data[1])
                return_value.extend(tree_values(current_node._left))
                current_node = current_node._right
            else:
                current_node = current_node._left
        return return_value
        
    def range(self, lower_bound, upper_bound):
        return_value = []
        current_node = self.root
        while not current_node is None and not current_node._data is None and (current_node._data[0] > upper_bound or current_node._data[0] < lower_bound):
            if current_node._data[0] > upper_bound:
                current_node = current_node._left
            else:
                current_node = current_node._right
        if not current_node is None and not current_node._data is None:
            append_or_extend(return_value, current_node._data[1])
            left_subtree = Tree()
            left_subtree.root = current_node._left
            right_subtree = Tree()
            right_subtree.root = current_node._right
            return_value.extend(left_subtree.lower_bound(lower_bound))
            return_value.extend(right_subtree.upper_bound(upper_bound))
        return return_value
    
    def keys(self):
        return_value = []
        task_list = []
        if not self.root is None and not self.root._data is None:
            task_list.append(self.root)
        while len(task_list) > 0:
            current_node = task_list.pop()
            return_value.append(current_node._data[0])
            if not current_node._left is None and not current_node._left._data is None:
                task_list.append(current_node._left)
            if not current_node._right is None and not current_node._right._data is None:
                task_list.append(current_node._right)
        return return_value