class token:
    type_token:int
    valeur_token: int
    chaine_token: str
    x : int
    y : int
    def __init__(self,t,v,c,x,y):
        self.type_token=t
        self.valeur_token=v
        self.chaine_token=c
        self.x=x
        self.y=y

tokens =["tok_eof","tok_const","tok_ident","tok_plus","tok_moins","tok_multi","tok_div","tok_modulo","tok_and","tok_or",
"tok_not","tok_equal","tok_not_equal","tok_low","tok_gre","tok_leq","tok_geq","tok_par_open","tok_par_close","tok_bra_open","tok_bra_close",
"tok_cur_open","tok_cur_close","tok_semicolon","tok_affect","tok_adress","tok_int","tok_void","tok_return","tok_if","tok_for","tok_else","tok_do",
"tok_while","tok_continue","tok_break","tok_send","tok_debug","tok_receive","tok_comma"]

lines=[]
Last =token(None,None,None,0,0)
T =token(None,None,None,0,0)
chiffres=["1","2","3","4","5","6","7","8","9","0"]
lettres=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
mots_cles=["int","void","return","if","else","do","while","break","continue","for"]
def init(nom_fichier):
    global lines
    with open(nom_fichier) as file:
        for line in file:
            lines.append(line.rstrip())
    next()
   
    
def next():
    
    global lines
    global T 
    global Last
    Last=T
    i=Last.x
    j=Last.y
    #lire le char
    if j> len(lines[i])-1:
            if i>len(lines)-1:
                
                type_token=tokens.index("tok_eof")
                T=token(type_token,None,None,i,j) 
                return  
            else:
                i+=1
                j=0 
    
            
    c=lines[i][j]
    print("next "+c)
    if c=='/':
        if j<len(lines)-1:
            if lines[i][j+1]=='/':
                i+=1
                j=0
    elif c in chiffres:
        temp=""
        temp+=lines[i][j]
        stop=True
        if j+1<len(lines[i]):
            if lines[i][j+1] in chiffres:
                stop=   False
            
        while not stop :  
            j+=1
            print("j= "+str(j))
            c=lines[i][j]
            temp+=c
            if j+1<len(lines[i]):
                if lines[i][j+1] in chiffres:
                    stop=False
                else:
                    stop= True
                    
            else:
                stop=True
            
        temp=int(temp)
        T.valeur_token=temp
        if (j==0 and i==0):
            j+=1
        
        T.type_token=tokens.index("tok_const")
    elif c in lettres:
        temp=""
        while c in lettres:
            if j==len(lines[i])-1:
                i+=1
                j=0
            else:
                j+=1
            temp+=lines[i][j]
        if temp not in mots_cles:
            
            T.chaine_token=temp
            T.type_token=tokens.index("tok_ident")
        else:
            T.type_token=tokens.index("tok_"+temp)
    else:
        match c:
            case"+": T.type_token=tokens.index("tok_plus")
            case"-": 
                T.type_token=tokens.index("tok_moins")
            case"*": T.type_token=tokens.index("tok_multi")
            case"/": T.type_token=tokens.index("tok_div")
            case"%": T.type_token=tokens.index("tok_modulo")
            case"&": 
                if j< len(lines[i])-1:
                    if lines[i][j+1] == "&":
                        T.type_token= tokens.index("tok_and")
                    j+=1
                else:
                    if i<len(lines)-1:
                        i+=1
                        j=0
                    T.type_token=tokens.index("tok_adress")
            case"|": 
                if j< len(lines[i])-1:
                    if lines[i][j+1] == "|":
                        T.type_token= tokens.index("tok_or")
                    j+=1
            case "<":
                if j< len(lines[i])-1:
                    if lines[i][j+1] == "=":
                        T.type_token= tokens.index("tok_leq")
                    j+=1
                else:
                    if i<len(lines)-1:
                        i+=1
                        j=0
                    T.type_token=tokens.index("tok_low")
            case ">":
                if j< len(lines[i])-1:
                    if lines[i][j+1] == "=":
                        T.type_token= tokens.index("tok_geq")
                    j+=1
                else:
                    if i<len(lines)-1:
                        i+=1
                        j=0
                    T.type_token=tokens.index("tok_gre")
            case "=":
                if j< len(lines[i])-1:
                    if lines[i][j+1] == "=":
                        T.type_token= tokens.index("tok_equal")
                    j+=1
                else:
                    if i<len(lines)-1:
                        i+=1
                        j=0
                    T.type_token=tokens.index("tok_affect")    
            case"(": T.type_token=tokens.index("tok_par_open")
            case")": T.type_token=tokens.index("tok_par_close")
            case"[": T.type_token=tokens.index("tok_bra_open")
            case"]": T.type_token=tokens.index("tok_bra_close")
            case"{": T.type_token=tokens.index("tok_cur_open")
            case"}": T.type_token=tokens.index("tok_cur_close")
            case";": T.type_token=tokens.index("tok_semicolon")
            case"!": T.type_token=tokens.index("tok_not")
            case",": T.type_token=tokens.index("tok_comma")
        
    j+=1 
    T.x = i
    T.y = j
         
        

def check(type_token: int) :
    global T
    if T.type_token==type_token : 
        next()
        return True
    return False

def accept(type_token: int) : 
    if not check(type_token) : 
        raise Exception("Tu t'es trompé, j'attendais " + tokens[type_token] + " et j'ai eu " + tokens[T.type_token] + " à la ligne " + str(T.x) + " colonne " + str(T.y))



    