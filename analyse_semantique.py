import analyse_syntaxique as asyn
class sym : 
    
    name : str
    index: int 
    type_sym:str
    nb_args :int
    def __init__(self,n):
        self.name=n
        self.index=None
        self.type_sem=None
        self.nb_args= None

pile=[]
top=1
nbVar = 0
def begin():
    pile.append({})
def end():
    pile.pop()


# def begin():
#     global tab
#     global I
#     global top
#     I.append(I[top-1])  
#     top+=1
# def end():
#     global top
#     print("end: top: "+str(top))
#     top-=1

# def find(name:str):
#     global pile 
    
#     for i in range (len(pile)-1,-1,-1):  
    
#         if name in pile[i]:
            
#             return pile[i][name] 
#     raise Exception(name +" pas trouvé")
def find(name:str,t:str):
    global pile 
    
    for i in range (len(pile)-1,-1,-1):  
    
        if name in pile[i] and pile[i][name].type_sym==t:
            
            return pile[i][name] 
    raise Exception(name +" pas trouvé")
def declare(name:str,t:str):
    global pile 
    
    if name in pile[len(pile)-1]  :
        s= pile[len(pile)-1][name]
        if s.type_sym==t:
            raise Exception(name+" existe déja")
    s=sym(name)
    s.type_sym=t
    pile[len(pile)-1][name]= s
    return s
    
# def declare(name:str,type:str):
#     global pile 
    
#     if name in pile[len(pile)-1] :

#         raise Exception("la variable "+name+" existe déja ")
#     s=sym(name)
#     pile[len(pile)-1][name]= s
#     return s

# def declare(name:str):
#     global tab
#     global I
#     global top 
#     print("top declar "+str(top))
#     print("name : "+name)
#     indice_fin_T=I[top-1]
#     indice_debut_T=I[top-2]
   
#     for i in range(indice_debut_T,indice_fin_T,+1):
#             if tab[i]==name:
#                  raise Exception("name existe déjà")
#     s=sym(name)
#     tab.append(s)
#     I[top-1] +=1
#     return s

# def find(name:str):

    
#     i= I[top-1]-1
#     print("top: "+str(top))
#     while i>=0:
#         print(name, "==", tab[i].name, "???"+" i=: "+str(i))
#         if tab[i].name == name:
#             return tab[i]
#         i=i-1
#     raise Exception("name pas trouvé")
 

def anasem():
    global nbVar
    A = asyn.F()
    nbVar = 0
    semnode(A)
    return A

def semnode(N : asyn.nd) :
    global nbVar
    
    match N.type_nd : 
        case "nd_block":
            begin()
            for i in range(len(N.enfants)):
                semnode(N.enfants[i])
            end()
        case"nd_affect":
            if (N.enfants[0].type_nd!="nd_ref" and N.enfants[0].type_nd!="nd_ind"):
                raise Exception("erreur pas de fils ref " )
            for i in range(len(N.enfants)):
                semnode(N.enfants[i])
        case"nd_decl":
            s=declare(N.chaine_nd,"sym_var")  
            s.index=nbVar
            nbVar +=1    
        case "nd_ref" :
            t= "sym_func" if N.valeur_nd==2 else "sym_var"
            s = find(N.chaine_nd,t)  
            N.index = s.index
        case "nd_appel" : 
            for i in range(len(N.enfants)):
                semnode(N.enfants[i])
            temp=None
            temp=find(N.enfants[0].chaine_nd,"sym_func")
            if N.enfants[0].type_nd != "nd_ref" :
                raise Exception("Exception levée, pas de référence pour l'appel de fonction dans l'arbre")
            if temp==None  :
                raise Exception("fonction " + N.enfants[0].chaine_nd + " non trouvée")
            if len(N.enfants)-1 != temp.nb_args:
                raise Exception("Nombre d'arguments invalide, on en attendait " + str(temp.nb_args) + " au lieu de " + str(len(N.enfants)-1))
        case "nd_func" :
            s=declare(N.chaine_nd,"sym_func")  
            s.nb_args=len(N.enfants)-1   
            nbVar = 0
            begin()
            #boucle sur les enfants
            for enfant in N.enfants :
                semnode(enfant)
            end()
            N.valeur_nd = nbVar - (len(N.enfants) - 1)
        case _:   
            for i in range(len(N.enfants)):
                semnode(N.enfants[i])          