class token:
    type_token: int
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

tokens = [
    "tok_eof", "tok_const", "tok_ident", "tok_plus", "tok_moins", "tok_multi", "tok_div", "tok_modulo", "tok_and", "tok_or",
    "tok_not", "tok_equal", "tok_not_equal", "tok_low", "tok_gre", "tok_leq", "tok_geq", "tok_par_open", "tok_par_close", "tok_bra_open", "tok_bra_close",
    "tok_cur_open", "tok_cur_close", "tok_semicolon", "tok_affect", "tok_adress", "tok_int", "tok_void", "tok_return", "tok_if", "tok_for", "tok_else", "tok_do",
    "tok_while", "tok_continue", "tok_break", "tok_send", "tok_debug", "tok_receive", "tok_comma"
]

lines = []
Last = token(None, None, None, 0, 0)
T = token(None, None, None, 0, 0)

chiffres = [str(i) for i in range(10)]
lettres = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
           'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
           'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
           'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
mots_cles = ["int", "void", "return", "if", "else", "do", "while", "break", "continue", "for"]

current_line_idx = 0
current_char_idx = 0

def init(nom_fichier):
    global lines, current_line_idx, current_char_idx
    with open(nom_fichier, 'r') as file:
        for line in file:
            lines.append(line.rstrip('\n'))
    current_line_idx = 0
    current_char_idx = 0
    next_token()

def get_char():
    global current_line_idx, current_char_idx

    # Ignorer les lignes vides en avançant l'index de ligne
    while current_line_idx < len(lines) and current_char_idx >= len(lines[current_line_idx]):
        current_line_idx += 1
        current_char_idx = 0
        # Quand on change de ligne, si la nouvelle ligne n'est pas la fin du fichier,
        # on peut considérer que le caractère "consommé" est un saut de ligne.
        # Cela aide `next_token` à voir des espaces.
        if current_line_idx < len(lines):
            return '\n' # Retourne un saut de ligne symbolique pour être traité comme un espace

    if current_line_idx >= len(lines):
        return None # Fin du fichier

    char = lines[current_line_idx][current_char_idx]
    current_char_idx += 1
    return char

def peek_char():
    global current_line_idx, current_char_idx

    temp_line_idx = current_line_idx
    temp_char_idx = current_char_idx

    # Tente d'avancer la position temporaire
    # Il faut être prudent car current_char_idx est déjà le caractère *suivant*
    # dans le flux après un get_char(). Donc peek_char doit regarder à temp_char_idx.
    
    # Pour peek_char, si current_char_idx est à la fin de la ligne,
    # le 'next' char est potentiellement sur la ligne suivante.
    if temp_char_idx >= len(lines[temp_line_idx]):
        temp_line_idx += 1
        temp_char_idx = 0
        
        # Sauter les lignes vides temporairement pour le peek
        while temp_line_idx < len(lines) and len(lines[temp_line_idx]) == 0:
            temp_line_idx += 1
            temp_char_idx = 0

        if temp_line_idx >= len(lines):
            return None # Fin du fichier
        else:
            # Si la nouvelle ligne est non vide, retourne son premier caractère.
            # Sinon (si elle est vide), le caractère suivant "logique" est un saut de ligne.
            return lines[temp_line_idx][temp_char_idx] if len(lines[temp_line_idx]) > 0 else '\n'
            
    return lines[temp_line_idx][temp_char_idx]


def next_token():
    global T, Last, current_line_idx, current_char_idx
    Last = T # Enregistre le token précédent

    # Sauvegarder la position de début du token (avant de skipper les blancs/commentaires)
    start_x = current_line_idx
    start_y = current_char_idx

    char = get_char()

    # Sauter les espaces, les tabulations et les commentaires
    while char is not None and (char.isspace() or (char == '/' and peek_char() == '/')):
        if char == '/' and peek_char() == '/':
            # C'est un commentaire, on avance directement à la ligne suivante
            current_line_idx += 1
            current_char_idx = 0
            char = get_char() # Lire le premier caractère de la nouvelle ligne (ou None si EOF)
            # Après avoir sauté une ligne de commentaire, mettons à jour les start_x, start_y
            # pour que le prochain token commence à la bonne position.
            start_x = current_line_idx
            start_y = current_char_idx
        else: # C'est un espace ou un saut de ligne
            char = get_char()
            # Si on a juste consommé un blanc, la nouvelle position de début est la position actuelle.
            start_x = current_line_idx
            start_y = current_char_idx 
        
    if char is None:
        T = token(tokens.index("tok_eof"), None, None, current_line_idx, current_char_idx)
        return

    # Initialise T avec la position réelle du début du token
    # On utilise start_x et start_y car ils ont été mis à jour après les blancs/commentaires.
    T = token(None, None, None, start_x, start_y - 1) # -1 car get_char() a déjà avancé la position

    # --- PARTIE MODIFIÉE POUR LES CHIFFRES (maintenue) ---
    if char in chiffres:
        temp = ""
        current_token_line = current_line_idx # Enregistre la ligne de début du chiffre
        while char is not None and char in chiffres and current_line_idx == current_token_line:
            temp += char
            char = get_char()
        T.valeur_token = int(temp)
        T.type_token = tokens.index("tok_const")
        
        # Si le dernier 'char' lu n'était pas un chiffre ou était sur une nouvelle ligne, on le remet en arrière
        if char is not None and (char not in chiffres or current_line_idx != current_token_line):
            current_char_idx -= 1
            if current_char_idx < 0: # Gérer le cas de "dé-lire" au-delà du début de ligne
                current_line_idx -= 1
                if current_line_idx >= 0: # S'assurer qu'on ne va pas en dessous de 0
                    current_char_idx = len(lines[current_line_idx]) 
                else: # Cas extrême au tout début du fichier
                    current_char_idx = 0
                    current_line_idx = 0
    # --- FIN PARTIE MODIFIÉE ---
            
    elif char in lettres:
        temp = ""
        current_token_line = current_line_idx # Ajouté pour gérer les identifiants sur une seule ligne
        while char is not None and (char in lettres or char in chiffres) and current_line_idx == current_token_line: # Ajout de la condition de ligne
            temp += char
            char = get_char()
        
        if temp in mots_cles:
            T.type_token = tokens.index("tok_" + temp)
        else:
            T.chaine_token = temp
            T.type_token = tokens.index("tok_ident")
        
        # Le dernier 'char' lu n'est pas une lettre/chiffre d'identifiant, ou est sur une nouvelle ligne
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
        # Gérer les opérateurs et symboles (inchangé par rapport à votre version)
        if char == '&' and peek_char() == '&':
            get_char() # Consommer le deuxième '&'
            T.type_token = tokens.index("tok_and")
        elif char == '|' and peek_char() == '|':
            get_char() # Consommer le deuxième '|'
            T.type_token = tokens.index("tok_or")
        elif char == '=' and peek_char() == '=':
            get_char() # Consommer le deuxième '='
            T.type_token = tokens.index("tok_equal")
        elif char == '<' and peek_char() == '=':
            get_char() # Consommer le '='
            T.type_token = tokens.index("tok_leq")
        elif char == '>' and peek_char() == '=':
            get_char() # Consommer le '='
            T.type_token = tokens.index("tok_geq")
        elif char == '!' and peek_char() == '=':
            get_char() # Consommer le '='
            T.type_token = tokens.index("tok_not_equal")
        else:
            match char:
                case "+": T.type_token = tokens.index("tok_plus")
                case "-": T.type_token = tokens.index("tok_moins")
                case "*": T.type_token = tokens.index("tok_multi")
                case "/": T.type_token = tokens.index("tok_div")
                case "%": T.type_token = tokens.index("tok_modulo")
                case "&": T.type_token = tokens.index("tok_adress")
                case "<": T.type_token = tokens.index("tok_low")
                case ">": T.type_token = tokens.index("tok_gre")
                case "=": T.type_token = tokens.index("tok_affect")
                case "(": T.type_token = tokens.index("tok_par_open")
                case ")": T.type_token = tokens.index("tok_par_close")
                case "[": T.type_token = tokens.index("tok_bra_open")
                case "]": T.type_token = tokens.index("tok_bra_close")
                case "{": T.type_token = tokens.index("tok_cur_open")
                case "}": T.type_token = tokens.index("tok_cur_close")
                case ";": T.type_token = tokens.index("tok_semicolon")
                case "!": T.type_token = tokens.index("tok_not")
                case ",": T.type_token = tokens.index("tok_comma")
                case _:
                    raise Exception(f"Caractère inattendu: '{char}' à la ligne {start_x} colonne {start_y}")
    
    # Mettre à jour la position de fin du token
    T.x = current_line_idx
    T.y = current_char_idx

def check(type_token: int) :
    global T
    if T.type_token==type_token : 
        next_token()
        return True
    return False

def accept(type_token: int) : 
    global T
    if not check(type_token) : 
        raise Exception("Tu t'es trompé, j'attendais " + tokens[type_token] + " et j'ai eu " + tokens[T.type_token] + " à la ligne " + str(T.x) + " colonne " + str(T.y))