class Tree:
    pos = 0
    node_number = 0

    def __init__(self, value, left=None, right=None, position=0, node_nr = -1):
        self.value = value
        self.left = left
        self.right = right
        self.position = position
        self.node_nr = 'n' + str(node_nr)

    def set_pos(self,position):
        self.position = position

    def print_tree(self):
        print(self.value)
        if self.left:
            self.left.print_tree()
        if self.right:
            self.right.print_tree()


def print_level_order(root):
    h = height(root)
    for i in range(1, h + 1):
        print_given_level(root, i)

        # Print nodes at a given level


def print_given_level(root, level):
    if root is None:
        return
    if level == 1:
        if root.data != '':
            print(root.data + " -> " + str(root.position) + ", number: " + root.number)
    elif level > 1:
        print_given_level(root.left, level - 1)
        print_given_level(root.right, level - 1)


def height(node):
    if node is None:
        return 0
    else:
        # Compute the height of each subtree
        lheight = height(node.left)
        rheight = height(node.right)

        # Use the larger one
        if lheight > rheight:
            return lheight + 1
        else:
            return rheight + 1


def get_expresie():
    with open('regex.txt', 'r') as file:
        regex = file.read()

    exp = regex[0]
    in_sau = False
    for i in range(1, len(regex) - 1):
        if regex[i] not in ['(', ')', '|', '*'] and regex[i - 1] == '*' and regex[i+1] != '*':
            exp = exp + '.' + regex[i]
        elif regex[i] not in ['(', ')', '*', '|'] and regex[i - 1] not in ['(', ')', '*', '|']:
            if in_sau == True:
                exp = exp + '.' + regex[i]
            else:
                exp = '(' + exp + ').' + regex[i]
            if regex[i] not in ['(', ')', '|', '*'] and regex[i + 1] in [')', '|']:
                exp = exp + ')'
                in_sau = False
        elif regex[i] not in ['(', ')', '|', '*'] and regex[i-1] == '|' and regex[i+1] not in ['(', ')', '|', '*']:
            exp = exp + '(' + regex[i]
            in_sau = True
        elif regex[i] not in ['(', ')', '|', '*'] and regex[i+1] == ')' and regex[i-1] not in ['(', ')', '|', '*']:
            exp = exp + regex[i] + ')'
        elif regex[i-1] == '*' and regex[i] == '(':
            exp = exp + '.' + regex[i]
        elif regex[i-1] == '(' and regex[i] not in ['(', ')', '|', '*'] and regex[i+1] not in ['(', ')', '|', '*']:
            exp = exp + '(' + regex[i]
            in_sau = True
        elif regex[i-1] == ')' and (regex[i] not in ['(', ')', '|', '*'] or regex[i] == '('):
            exp = '(' + exp + '.' + regex[i] + ')'
        elif regex[i + 1] == '*' and regex[i] not in ['(', ')', '|', '*'] and regex[i-1] in ['(', ')', '|', '*']:
            exp = exp + '.(' + regex[i] + '*' + ')'
            i = i + 1
        else:
            exp = exp + regex[i]

    if i + 1 != len(regex):
        if regex[len(regex) - 1] not in ['(', ')', '|', '*'] and regex[len(regex) - 2] == '*':
            exp = '(' + exp + ').' + regex[len(regex) - 1]
        elif regex[len(regex) - 1] not in ['(', ')', '*', '|'] and regex[len(regex) - 2] not in ['(', ')', '*', '|']:
            exp = '(' + exp + ').' + regex[len(regex) - 1]
        elif regex[len(regex) - 2] == '*' and regex[len(regex) - 1] == '(':
            exp = exp + '.' + regex[len(regex) - 1]
        elif regex[len(regex) - 2] == ')' and regex[len(regex) - 1] not in ['(', ')', '|', '*']:
            exp = exp + '.' + regex[len(regex) - 1]
        else:
            exp = exp + regex[len(regex) - 1]

    exp = '(' + exp + ').#'
    exp = list(exp)
    exp.append("end")
    return exp


def get_node_numbers(expresie):
    nr_noduri = 0

    for i in expresie:
        if i not in ['(', ')']:
            nr_noduri = nr_noduri + 1

    return nr_noduri


def get_token(token_list, expected):
    if token_list[0] == expected:
        del token_list[0]
        return True
    return False


def get_leaf(token_list):
    if get_token(token_list, '('):
        x = get_concat(token_list)
        get_token(token_list, ')')
        return x
    else:
        x = token_list[0]
        if x in ['(', ')', '.', '+', '*']:
            return None
        del token_list[0]
        Tree.pos = Tree.pos + 1
        Tree.node_number = Tree.node_number - 1
        return Tree(x, None, None, Tree.pos, Tree.node_number)


def get_or(token_list):
    a = get_leaf(token_list)
    if get_token(token_list,'|'):
        b = get_or(token_list)
        Tree.node_number = Tree.node_number - 1
        return Tree('|', a, b, node_nr=Tree.node_number)
    return a


def get_concat(token_list):
    a = get_star(token_list)
    if get_token(token_list, '.'):
        b = get_concat(token_list)
        Tree.node_number = Tree.node_number - 1
        return Tree('.', a, b, node_nr=Tree.node_number)
    return a


def get_star(token_list):
    a = get_or(token_list)
    if get_token(token_list, '*'):
        # b = get_star(token_list)
        Tree.node_number = Tree.node_number - 1
        return Tree('*', a, None, node_nr=Tree.node_number)
    return a


def print_tree_postorder(tree):
    if tree is None:
        return
    print_tree_postorder(tree.left)
    print_tree_postorder(tree.right)
    print(tree.value + ",position: " + str(tree.position) + ", number: " + tree.node_nr)


nodes = {} # nodurile frunza
V = [] # alfabetul expresiei


def make_nodes(regex):
    nr = 1
    for i in regex:
        if i not in ['(', ')', '|', '+', '*', '.', 'end']:
            new_node = {nr: i}
            if i not in V and i != '#':
                V.append(i)
            nr = nr + 1
            nodes.update(new_node)


nullables = {}
first_poss = {}
last_poss = {}
follow_poss = {}


def nullable(node):
    if not node.left and not node.right:
        if node.value == "lambda":
            return True
        elif node.value != '':
            return False
    elif node.value == '|':
        return nullable(node.left) or nullable(node.right)
    elif node.value == '.':
        return nullable(node.left) and nullable(node.right)
    elif node.value == '*':
        return True


def first_pos(node):
    if not node.left and not node.right:
        if node.value == "lambda":
            return set()
        elif node.value != '':
            return {node.position}
    elif node.value == '|':
        return set(first_pos(node.left)) | set(first_pos(node.right))
    elif node.value == '.':
        if nullable(node.left):
            return set(first_pos(node.left)) | set(first_pos(node.right))
        else:
            return set(first_pos(node.left))
    elif node.value == '*':
        return first_pos(node.left)


def last_pos(node):
    if not node.left and not node.right:
        if node.value == "lambda":
            return set()
        elif node.value != '':
            return {node.position}
    elif node.value == '|':
        return set(last_pos(node.left)) | set(last_pos(node.right))
    elif node.value == '.':
        if nullable(node.right):
            return set(last_pos(node.left)) | set(last_pos(node.right))
        else:
            return set(last_pos(node.right))
    elif node.value == '*':
        return last_pos(node.left)


def follow_pos(node):
    if node.position != 0:
        follow_poss[node.position] = set()
    elif node.value == '.':
        for i in range(1, get_max_nodes()+1):
            if i in last_poss[node.left.node_nr]:
                follow_poss[i] = follow_poss[i] | first_poss[node.right.node_nr]
    elif node.value == '*':
        for i in range(1, get_max_nodes() + 1):
            if i in last_poss[node.left.node_nr]:
                follow_poss[i] = follow_poss[i] | first_poss[node.left.node_nr]


def sdr(tree):
    if tree.left:
        sdr(tree.left)
    if tree.right:
        sdr(tree.right)
    if tree.value != '':
        n = {tree.node_nr: nullable(tree)}
        fp ={tree.node_nr: first_pos(tree)}
        lp ={tree.node_nr: last_pos(tree)}
        #folp = {tree.node_nr: follow_pos(tree)}

        nullables.update(n)
        first_poss.update(fp)
        last_poss.update(lp)
        follow_pos(tree)
        #follow_poss.update(folp)


def get_max_nodes():
    maxim = 0
    for key, value in nodes.items():
        if key > maxim:
            maxim = key
    return maxim


exp = get_expresie()
Tree.node_number = get_node_numbers(exp)
make_nodes(exp)
print(V)
tree = get_concat(exp)
sdr(tree)
print_tree_postorder(tree)

radacina = tree.node_nr
poz = get_max_nodes()
q0 = first_poss[radacina]
visited = {}

for key, value in first_poss.items():
    node_number = int(key[1:])
    visited[node_number] = 0

Q = [first_poss[radacina]]

nr = 0
for key, value in visited.items():
    if key > nr:
        nr = key

visited.update({str(list(Q[0])): 0})

# visited.update({nr: 0})
tranzitii = [] # va fi un vector cu elemente de forma : (stare_initiala, caracter, stare_urmatoare)
if poz in first_poss[radacina]:
    F = [first_poss[radacina]]
else:
    F = []

T = list(Q[0])
for T in Q:
    if visited[str(list(T))] == 0:
        visited[str(list(T))] = 1
        for a in V:
            U = set()
            for i in list(T):
                if nodes[i] == a:
                    U = U | follow_poss[i]
            if U not in Q and U != set():
                Q.append(U)
                visited.update({str(list(U)): 0})
                if poz in U:
                    F.append(U)
            if U != set():
                tranzitie_curenta = (T, a, U)
                tranzitii.append(tranzitie_curenta)
print(Q)
print(F)
for i in tranzitii:
    print(i)
#

# cum la suma in stanga pot avea un produs si in dreapta o suma, sau doar un produs, asa si la * cu . si |: in stanga
# lui . pot avea * si in dreapta ., sau doar *
# in stanga lui * pot avea | sau doar o frunza, * nu are dreapta(operator unar)