class Tree:
    def __init__(self, value, left=None, right=None, position = 0):
        self.value = value
        self.left = left
        self.right = right
        self.position = position

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
print(exp)

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
        return Tree(x, None, None)


def get_or(token_list):
    a = get_leaf(token_list)
    if get_token(token_list,'|'):
        b = get_or(token_list)
        return Tree('|', a, b)
    return a


def get_concat(token_list):
    a = get_star(token_list)
    if get_token(token_list, '.'):
        b = get_concat(token_list)
        return Tree('.', a, b)
    return a


def get_star(token_list):
    a = get_or(token_list)
    if get_token(token_list, '*'):
        # b = get_star(token_list)
        return Tree('*', a, None)
    return a


def print_tree_postorder(tree):
    if tree is None:
        return
    print_tree_postorder(tree.left)
    print_tree_postorder(tree.right)
    print(tree.value)

#
# token = "((a*).b*).c"
# token_list = list(token)
# token_list.append("end")


tree = get_concat(exp)
print_tree_postorder(tree)

# cum la suma in stanga pot avea un produs si in dreapta o suma, sau doar un produs, asa si la * cu . si |: in stanga
# lui . pot avea * si in dreapta ., sau doar *
# in stanga lui * pot avea | sau doar o frunza, * nu are dreapta(operator unar)