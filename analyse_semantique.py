import analyse_syntaxique as asyn
class sym : 
    
    name : str
    index: int 
    type_sem:str
    def __init__(self,n):
        self.name=n
tab=[]
I=[0]
top=1
nbVar = 0
def begin():
    global tab
    global I
    global top
    I.append(I[top-1])  
    top+=1
def end():
    global top
    print("end: top: "+str(top))
    top-=1

def declare(name:str):
    global tab
    global I
    global top 
    print("top declar "+str(top))
    print("name : "+name)
    indice_fin_T=I[top-1]
    indice_debut_T=I[top-2]
   
    for i in range(indice_debut_T,indice_fin_T,+1):
            if tab[i]==name:
                 raise Exception("name existe déjà")
    s=sym(name)
    tab.append(s)
    I[top-1] +=1
    return s

def find(name:str):

    
    i= I[top-1]-1
    print("top: "+str(top))
    while i>=0:
        print(name, "==", tab[i].name, "???"+" i=: "+str(i))
        if tab[i].name == name:
            return tab[i]
        i=i-1
    raise Exception("name pas trouvé")
 

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
            
            if (N.enfants[0].type_nd!="nd_ref"):
                raise Exception("erreur pas de fils ref " )
            for i in range(len(N.enfants)):
                semnode(N.enfants[i])
        case"nd_decl":
            
            s=declare(N.chaine_nd) 
            s.index=nbVar
            #I[top-1]=len(tab)-1
            nbVar +=1    
        case "nd_ref" :
            
            s = find(N.chaine_nd)  
            N.index = s.index
        case "nd_func" :
            declare(N.chaine_nd)
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
            