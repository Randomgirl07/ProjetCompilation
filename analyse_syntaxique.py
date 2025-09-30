import analyse_lexicale as al
# nodes=["nd_eof","nd_const","nd_ident","nd_plus","nd_moins","nd_multi","nd_div","nd_modulo","nd_and","nd_or","nd_ref",
# "nd_not","nd_equal","nd_not_equal","nd_low","nd_gre","nd_leq","nd_geq","nd_bra_open","nd_bra_close","nd_appel",
# "nd_cur_open","nd_cur_close","nd_semicolon","nd_affect","nd_adress","nd_int","nd_void","nd_return","nd_cond","nd_loop","nd_seq",
# "nd_continue","nd_break","nd_send","nd_debug","nd_receive","nd_comma","nd_sub","nd_add","nd_block","nd_drop","nd_decl","nd_target"]

        
class op_element : 
    prio : int
    parg : int
    type_node : str
    def __init__(self,prio,parg,t):
        self.prio = prio
        self.parg = parg
        self.type_node = t

OP={
    "tok_plus" : op_element(5,6,"nd_add"),
    "tok_moins" : op_element(5,6,"nd_sub"),
    "tok_multi" : op_element(6,7,"nd_multi"),
    "tok_div" : op_element(6,7,"nd_div"),
    "tok_modulo" : op_element(6,7,"nd_modulo"),
    "tok_equal" : op_element(4,5,"nd_equal"),
    "tok_not_equal" : op_element(4,5,"nd_not_equal"),
    "tok_low" : op_element(4.5,5,"nd_low"),
    "tok_gre" : op_element(4.5,5,"nd_gre"),
    "tok_leq" : op_element(4.5,5,"nd_leq"),
    "tok_geq" : op_element(4.5,5,"nd_geq"),
    "tok_or" : op_element(2,3,"nd_or"),
    "tok_and" : op_element(3,4,"nd_and"),
    "tok_affect" : op_element(1,1,"nd_affect")
}
class nd:
    type_nd:str
    valeur_nd: int
    chaine_nd: str
    enfants : list
    index : int 
    __match_args__ = ("type", "valeur", "chaine")
    def __init__(self,type_nd,valeur_nd,chaine_nd):
        self.type_nd=type_nd
        self.valeur_nd=valeur_nd
        self.chaine_nd=chaine_nd
        self.enfants=[]
        self.index=0
    def set_fils1(self,fils1): 
        if fils1!=None:
            self.enfants.append(fils1)
    def set_fils2(self,fils1,fils2):
        if fils1!=None:
            self.enfants.append(fils1)
        if fils2!=None:
            self.enfants.append(fils2)

def E(prio : int):
    N = P()
   
    while al.T.type_token in OP  : 
        if OP[al.T.type_token].prio < prio :
            break
        op = al.T.type_token
        al.next_token() 
        M = E(OP[op].parg)
        X=N
        N=nd(OP[op].type_node, None,None)
        N.set_fils2(X,M)
    return N

def S():
    Atome = A()
    if al.check("tok_bra_open") :
        N = nd("nd_appel",None,None)
        N.set_fils1(Atome)
        # boucle
        if not al.check("tok_bra_close") :
            while True : 
                fils = E(0)
                N.set_fils1(fils)
                if not al.check("tok_comma") :
                    break
            al.accept("tok_bra_close")
        return N
    else : 
        return Atome
        
        
def F():
    
    if not al.check("tok_int"):
        al.accept("tok_void")
    
    al.accept("tok_ident")
    N=nd("nd_func",None,al.Last.chaine_token)
    al.accept("tok_bra_open")
    if not al.check("tok_bra_close"):
        while True:
            al.accept("tok_int")
            al.accept("tok_ident")
            N.set_fils1(nd("nd_decl",None,al.Last.chaine_token))
            if not al.check("tok_comma"):
                break 
        al.accept("tok_bra_close")
    temp=I()
    N.set_fils1(temp)
    return N
    
def I():
    if(al.check("tok_debug")):
        N=E(0)
        al.accept("tok_semicolon")
        temp=nd("nd_debug",None,None)
        temp.set_fils1(N)
        return temp
    elif al.check("tok_cur_open"):
        
        N = nd("nd_block",None,None)
        while(not al.check("tok_cur_close")):
            N.set_fils1(I())
        return N
    elif al.check("tok_int") :
        N = nd("nd_decl", None, al.T.chaine_token)
        al.accept("tok_ident")
        al.accept("tok_semicolon")
        return N
    elif al.check("tok_if") :
        al.accept("tok_bra_open")
        E1 = E(0)
        al.accept("tok_bra_close")
        I1 = I()
        I2 = None
        if(al.check("tok_else")) : 
            I2 = I()
        N = nd("nd_cond",None,None)
        N.set_fils1(E1)
        N.set_fils1(I1)
        N.set_fils1(I2)
        return N
    elif al.check("tok_while"):
        al.accept("tok_bra_open")
        E1=E(0)
        al.accept("tok_bra_close")
        I1=I()
        N1= nd("nd_loop",None,None)
        cnd= nd("nd_cond",None,None)
        target= nd("nd_target",None,None)
        br= nd("nd_break",None,None)
        N1.set_fils1(target)
        cnd.set_fils1(E1)
        cnd.set_fils1(I1)
        cnd.set_fils1(br)
        N1.set_fils1(cnd)
        return N1
    elif al.check("tok_break"):
        al.accept("tok_semicolon")
        return nd("nd_break",None,None)
    elif al.check("tok_continue"):
        al.accept("tok_semicolon")
        return nd("nd_continue",None,None)
    elif al.check("tok_do") :
        I1 = I()
        al.accept("tok_while")
        al.accept("tok_bra_open")
        E1 = E(0)
        al.accept("tok_bra_close")
        al.accept("tok_semicolon")
        cnd = nd("nd_cond",None,None)
        loop = nd("nd_loop",None,None)
        loop.set_fils1(I1)
        loop.set_fils1(nd("nd_target",None,None))

        n=nd("nd_not",None,None)
        n.set_fils1(E1)
        cnd.set_fils1(n)
        cnd.set_fils1(nd("nd_break",None,None))
        loop.set_fils1(cnd)
        return loop
    elif al.check("tok_for"):
        al.accept("tok_bra_open")
        E1=E(0)
        al.accept("tok_semicolon")
        E2=E(0)
        al.accept("tok_semicolon")
        E3=E(0)
        al.accept("tok_bra_close")
        I1=I()
        N=nd("nd_seq",None,None)
        cnd=nd("nd_cond",None,None)
        seq=nd("nd_seq",None,None)
        target=nd("nd_target",None,None)
        br= nd("nd_break",None,None)
        loop=nd("nd_loop",None,None)
        drop1= nd("nd_drop",None,None)
        drop2=nd("nd_drop",None,None)
        seq.set_fils1(I1)
        seq.set_fils1(target)
        drop2.set_fils1(E3)
        seq.set_fils1(drop2)
        cnd.set_fils1(E2)
        cnd.set_fils1(seq)
        cnd.set_fils1(br)
        loop.set_fils1(cnd)
        drop1.set_fils1(E1)
        N.set_fils1(drop1)
        N.set_fils1(loop)
        return N
    elif al.check("tok_return") :
        E1 = E(0)
        N = nd("nd_return",None,None)
        N.set_fils1(E1)
        al.accept("tok_semicolon")
        return N
    else:
        
        N=E(0)

        al.accept("tok_semicolon")
        temp=nd("nd_drop",None,None)
        temp.set_fils1(N)
        return temp
            

def P():
    
    if al.check("tok_not") : 
        n = P()
        a = nd("nd_not", None,None)
        a.set_fils1(n)
        return a
    elif al.check("tok_moins") :
        n = P()
        a = nd("nd_moins", None,None)
        a.set_fils1(n)
        return a
    elif al.check("tok_plus") : 
        return P()
    elif al.check("tok_multi") :
        n = P()
        a = nd("nd_ind",None,None)
        a.set_fils1(n)
        return a
    elif al.check("tok_adress") :
        n = P()
        a = nd("nd_adress",None,None)
        a.set_fils1(n)
        return a
    else:
        
        return S()
    

def A():
    if (al.check("tok_const")):
        return nd("nd_const",al.Last.valeur_token,None)
    elif (al.check("tok_bra_open")):
        r=E(0)
        al.accept("tok_bra_close")
        return r
    elif(al.check("tok_ident")) :
        m=nd("nd_ref", None, al.Last.chaine_token)
        return m
    else:
        raise Exception("Tu t'es trompé..."+al.T.type_token)
        