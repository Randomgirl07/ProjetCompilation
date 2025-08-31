import analyse_lexicale as al
nodes=["nd_eof","nd_const","nd_ident","nd_plus","nd_moins","nd_multi","nd_div","nd_modulo","nd_and","nd_or",
"nd_not","nd_equal","nd_not_equal","nd_low","nd_gre","nd_leq","nd_geq","nd_par_open","nd_par_close","nd_bra_open","nd_bra_close",
"nd_cur_open","nd_cur_close","nd_semicolon","nd_affect","nd_adress","nd_int","nd_void","nd_return","nd_if","nd_for","nd_else","nd_do",
"nd_while","nd_continue","nd_break","nd_send","nd_debug","nd_receive","nd_comma"]
class nd:
    type_nd:int
    valeur_nd: int
    chaine_nd: str
    enfants : list
    __match_args__ = ("type", "valeur", "chaine")
    def __init__(self,type_nd,valeur_nd,chaine_nd):
        self.type_nd=type_nd
        self.valeur_nd=valeur_nd
        self.chaine_nd=chaine_nd
        self.enfants=[]
    def set_fils1(self,fils1): 
        self.enfants.append(fils1)
    def set_fils2(self,fils1,fils2):
        self.enfants.append(fils1)
        self.enfants.append(fils2)
def afficher(A:nd):
    if A.type_nd==nodes.index("nd_const"):
        print("(" +A.valeur_nd)
    elif  A.type_nd==nodes.index("nd_not"):
        print("!" )
    elif A.type_nd==nodes.index("nd_neg"):
        print("-" +A.valeur_nd)
    for enfant in A.enfants:
        afficher(enfant)
    print(")")
def E():
    return P()

def S():
    return A()

def P():
    
    if al.check(al.tokens.index("tok_not")) : 
        n = P()
        a = nd(nodes.index("nd_not"), None,None)
        a.set_fils1(n)
        return a
    elif al.check(al.tokens.index("tok_moins")) :
        n = P()
        a = nd(nodes.index("nd_moins"), None,None)
        a.set_fils1(n)
        return a
    elif al.check(al.tokens.index("tok_plus")) : 
        return P()
    else:
        
        return S()
    

def A():
    if (al.check(al.tokens.index("tok_const"))):
        return nd(nodes.index("nd_const"),al.Last.valeur_token,None)
    elif (al.check(al.tokens.index("tok_par_open"))):
        r=E()
        al.accept(al.tokens.index("tok_par_close"))
        return r
    else:

         raise Exception("Tu t'es trompé...")
        