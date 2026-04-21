import re

symbol_table = {'b': 'int', 'c': 'float'}

class Node:
    def __init__(self, value, left=None, right=None):
        self.value, self.left, self.right, self.type = value, left, right, None

def get_tokens(expression):
    tokens = re.findall(r'\d+|[a-zA-Z_]\w*|[=+\-*/()]', expression)
    for token in tokens:
        if token.isalnum() and token not in symbol_table:
            symbol_table[token] = 'int' if token.isdigit() else 'var'
    print(f"\n[1] Tokens List: {tokens}\n[2] Symbol Table: {symbol_table}")
    return tokens

def build_tree(tokens, min_precedence=0):
    node = Node(tokens.pop(0))
    precedence = {'=': 1, '+': 2, '-': 2, '*': 3, '/': 3}
    while tokens and precedence.get(tokens[0], 0) >= min_precedence:
        operator = tokens.pop(0)
        next_precedence = precedence[operator] + (operator != '=')
        node = Node(operator, node, build_tree(tokens, next_precedence))
    return node

def check_types(node):
    if not node: return 'void'
    if not node.left and not node.right: return symbol_table.get(node.value, 'error')
    
    left_type = check_types(node.left)
    right_type = check_types(node.right)
    
    if node.value == '=': node.type = right_type
    elif 'error' in (left_type, right_type): node.type = 'error'
    elif 'float' in (left_type, right_type): node.type = 'float'
    else: node.type = 'int'
    
    return node.type

def print_tree(node, mode="SYNTAX"):
    def get_lines(n):
        if not n: return [], 0, 0, 0
        text = f" {n.value}:{n.type} " if mode == "SEMANTIC" and n.type else f" {n.value} "
        left_lines, left_width, left_height, left_center = get_lines(n.left)
        right_lines, right_width, right_height, right_center = get_lines(n.right)
        
        total_width = max(len(text), left_width + right_width + 2)
        result = [text.center(total_width)]
        
        if n.left or n.right:
            connector = (' '*(left_center+1) + '┌' + '─'*(left_width-left_center-1)) if n.left else (' '*(total_width//2))
            connector += '┴' if n.left and n.right else '┘' if n.left else '└'
            result.append((connector + ('─'*right_center + '┐' if n.right else '')).center(total_width))
            
        for i in range(max(left_height, right_height)):
            left_str = left_lines[i] if i < left_height else ' ' * left_width
            right_str = right_lines[i] if i < right_height else ' ' * right_width
            result.append(left_str + '  ' + right_str)
            
        return result, total_width, len(result), total_width // 2
        
    print(f"\n--- {mode} TREE ---")
    if node: print("\n".join(get_lines(node)[0]))

if __name__ == "__main__":
    tokens = get_tokens(input("Enter Code: ") or "a = b * 10 / 5")
    root_node = build_tree(tokens)
    print_tree(root_node, "SYNTAX")
    
    print(f"\n[3] Semantic Result: Result type is '{check_types(root_node)}'")
    print_tree(root_node, "SEMANTIC")








import re

class Node:
    def __init__(self, value, left=None, right=None):
        self.value, self.left, self.right = value, left, right

def get_tokens(expression):
    tokens = re.findall(r'\d+|[a-zA-Z_]\w*|[=+\-*/()]', expression)
    print(f"\n[1] Tokens List: {tokens}")
    return tokens

def build_tree(tokens, min_precedence=0):
    node = Node(tokens.pop(0))
    precedence = {'=': 1, '+': 2, '-': 2, '*': 3, '/': 3}
    
    while tokens and precedence.get(tokens[0], 0) >= min_precedence:
        operator = tokens.pop(0)
        next_precedence = precedence[operator] + (operator != '=')
        node = Node(operator, node, build_tree(tokens, next_precedence))
        
    return node

def print_tree(node):
    def get_lines(n):
        if not n: return [], 0, 0, 0
        text = f" {n.value} "
        left_lines, left_width, left_height, left_center = get_lines(n.left)
        right_lines, right_width, right_height, right_center = get_lines(n.right)
        
        total_width = max(len(text), left_width + right_width + 2)
        result = [text.center(total_width)]
        
        if n.left or n.right:
            connector = (' '*(left_center+1) + '┌' + '─'*(left_width-left_center-1)) if n.left else (' '*(total_width//2))
            connector += '┴' if n.left and n.right else '_|' if n.left else '|_'
            result.append((connector + ('─'*right_center + '-|' if n.right else '')).center(total_width))
            
        for i in range(max(left_height, right_height)):
            left_str = left_lines[i] if i < left_height else ' ' * left_width
            right_str = right_lines[i] if i < right_height else ' ' * right_width
            result.append(left_str + '  ' + right_str)
            
        return result, total_width, len(result), total_width // 2
        
    print(f"\n--- SYNTAX TREE ---")
    if node: print("\n".join(get_lines(node)[0]))

if __name__ == "__main__":
    tokens = get_tokens(input("Enter Code: ") or "a = b * 10 / 5")
    root_node = build_tree(tokens)
    print_tree(root_node)









import re

def generate_all(expr):
    lhs, rhs = expr.split('=') if '=' in expr else (None, expr)
    ops, vals, quads = [], [], []
    prec = {'+': 1, '-': 1, '*': 2, '/': 2}

    # Helper function to process operations
    def apply():
        o, b, a = ops.pop(), vals.pop(), vals.pop()
        quads.append([o, a, b, f"t{len(quads)+1}"]) 
        vals.append(quads[-1][3])

    # Parse tokens and build Quadruples dynamically
    for tk in re.findall(r'[a-zA-Z_]\w*|\d+|[+\-*/()]', rhs):
        if tk.isalnum(): vals.append(tk)
        elif tk == '(': ops.append(tk)
        elif tk == ')':
            while ops[-1] != '(': apply()
            ops.pop()
        else:
            while ops and ops[-1] in prec and prec.get(ops[-1], 0) >= prec[tk]: apply()
            ops.append(tk)
            
    while ops: apply()
    if lhs: quads.append(['=', vals[-1], '-', lhs.strip()])

    # Print 3AC
    print("\n--- Three Address Code ---")
    for q in quads: 
        print(f"{q[3]} = {q[1]} {q[0]} {q[2]}" if q[0] != '=' else f"{q[3]} = {q[1]}")
    
    # Print Quadruples using basic string formatting
    print("\n--- Quadruples ---")
    print(f"{'Op':<5} | {'Arg1':<6} | {'Arg2':<6} | {'Result'}")
    print("-" * 35)
    for q in quads: 
        print(f"{q[0]:<5} | {q[1]:<6} | {q[2]:<6} | {q[3]}")
    
    # Print Triples by dynamically swapping 'tN' with '(N-1)'
    print("\n--- Triples ---")
    sub_t = lambda v: re.sub(r't(\d+)', lambda m: f"({int(m.group(1))-1})", str(v))
    print(f"{'Idx':<5} | {'Op':<5} | {'Arg1':<6} | {'Arg2'}")
    print("-" * 35)
    for i, q in enumerate(quads):
        print(f"{i:<5} | {q[0]:<5} | {sub_t(q[1]):<6} | {sub_t(q[2] if q[0] != '=' else q[3])}")

if __name__ == "__main__":
    generate_all(input("Enter expression: ") or "x = a + b * c")






