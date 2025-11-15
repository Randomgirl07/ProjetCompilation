class token:
    type_token: str
    valeur_token: int
    chaine_token: str
    x: int
    y: int

    def __init__(self, t, v, c, x, y):
        self.type_token = t
        self.valeur_token = v
        self.chaine_token = c
        self.x = x
        self.y = y
lines = []
Last = token(None, None, None, 0, 0)
T = token(None, None, None, 0, 0)

chiffres = [str(i) for i in range(10)]
lettres = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
           'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
           'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
           'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
mots_cles = ["int", "void", "return", "if", "else", "do", "while", "break", "continue", "for","debug", "send","recv"]

current_line_idx = 0
current_char_idx = 0

def init(nom_fichier):
    global lines, current_line_idx, current_char_idx
    lines=[]
    with open(nom_fichier, 'r') as file:
        for line in file:
            lines.append(line.rstrip('\n'))
    current_line_idx = 0
    current_char_idx = 0
    next_token()

def get_char():
    global current_line_idx, current_char_idx
    while current_line_idx < len(lines) and current_char_idx >= len(lines[current_line_idx]):
        current_line_idx += 1
        current_char_idx = 0
        if current_line_idx < len(lines):
            return '\n'

    if current_line_idx >= len(lines):
        return None 

    char = lines[current_line_idx][current_char_idx]
    current_char_idx += 1
    return char

def peek_char():
    global current_line_idx, current_char_idx

    temp_line_idx = current_line_idx
    temp_char_idx = current_char_idx
    if temp_char_idx >= len(lines[temp_line_idx]):
        temp_line_idx += 1
        temp_char_idx = 0
        while temp_line_idx < len(lines) and len(lines[temp_line_idx]) == 0:
            temp_line_idx += 1
            temp_char_idx = 0

        if temp_line_idx >= len(lines):
            return None 
        else:
            return lines[temp_line_idx][temp_char_idx] if len(lines[temp_line_idx]) > 0 else '\n'
            
    return lines[temp_line_idx][temp_char_idx]


def next_token():
    global T, Last, current_line_idx, current_char_idx
    Last = T 
    start_x = current_line_idx
    start_y = current_char_idx
    char = get_char()
    while char is not None and (char.isspace() or (char == '/' and peek_char() == '/')):
        if char == '/' and peek_char() == '/':
            current_line_idx += 1
            current_char_idx = 0
            char = get_char()
            start_x = current_line_idx
            start_y = current_char_idx
        else:
            char = get_char()
            start_x = current_line_idx
            start_y = current_char_idx 
        
    if char is None:
        T = token("tok_eof", None, None, current_line_idx, current_char_idx)
        return

    T = token(None, None, None, start_x, start_y - 1) 

    if char in chiffres:
        temp = ""
        current_token_line = current_line_idx
        while char is not None and char in chiffres and current_line_idx == current_token_line:
            temp += char
            char = get_char()
        T.valeur_token = int(temp)
        T.type_token = "tok_const"
        
        if char is not None and (char not in chiffres or current_line_idx != current_token_line):
            current_char_idx -= 1
            if current_char_idx < 0: 
                current_line_idx -= 1
                if current_line_idx >= 0: 
                    current_char_idx = len(lines[current_line_idx]) 
                else: 
                    current_char_idx = 0
                    current_line_idx = 0
            
    elif char in lettres:
        temp = ""
        current_token_line = current_line_idx 
        while char is not None and (char in lettres or char in chiffres) and current_line_idx == current_token_line: 
            temp += char
            char = get_char()
        
        if temp in mots_cles:
            T.type_token = "tok_" + temp
        else:
            T.chaine_token = temp
            T.type_token = "tok_ident"
     
        if char is not None and (char not in lettres and char not in chiffres or current_line_idx != current_token_line):
            current_char_idx -= 1
            if current_char_idx < 0:
                current_line_idx -= 1
                if current_line_idx >= 0:
                    current_char_idx = len(lines[current_line_idx])
                else:
                    current_char_idx = 0
                    current_line_idx = 0
            
    else:
        if char == '&' and peek_char() == '&':
            get_char() 
            T.type_token = "tok_and"
        elif char == '|' and peek_char() == '|':
            get_char() 
            T.type_token = "tok_or"
        elif char == '=' and peek_char() == '=':
            get_char() 
            T.type_token = "tok_equal"
        elif char == '<' and peek_char() == '=':
            get_char() 
            T.type_token = "tok_leq"
        elif char == '>' and peek_char() == '=':
            get_char() 
            T.type_token = "tok_geq"
        elif char == '!' and peek_char() == '=':
            get_char() 
            T.type_token = "tok_not_equal"
        else:
            match char:
                case "+": T.type_token = "tok_plus"
                case "-": T.type_token = "tok_moins"
                case "*": T.type_token = "tok_multi"
                case "/": T.type_token = "tok_div"
                case "%": T.type_token = "tok_modulo"
                case "&": T.type_token = "tok_adress"
                case "<": T.type_token = "tok_low"
                case ">": T.type_token = "tok_gre"
                case "=": T.type_token = "tok_affect"
                case "(": T.type_token = "tok_bra_open"
                case ")": T.type_token = "tok_bra_close"
                case "[": T.type_token = "tok_hook_open"
                case "]": T.type_token = "tok_hook_close"
                case "{": T.type_token = "tok_cur_open"
                case "}": T.type_token = "tok_cur_close"
                case ";": T.type_token = "tok_semicolon"
                case "!": T.type_token = "tok_not"
                case ",": T.type_token = "tok_comma"
                case _:
                    raise Exception(f"Caractère inattendu: '{char}' à la ligne {start_x} colonne {start_y}")
    
    T.x = current_line_idx
    T.y = current_char_idx
    
    

def check(type_token: str) :
    global T
    if T.type_token==type_token : 
        next_token()
        return True
    return False

def accept(type_token: str) : 
    global T
    if not check(type_token) : 
        raise Exception("Tu t'es trompé, j'attendais " + type_token + " et j'ai eu " + T.type_token + " à la ligne " + str(T.x + 1) + " colonne " + str(T.y + 1))