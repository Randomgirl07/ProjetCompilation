import analyse_semantique as asem
def optim():
    A = asem.anasem()
    optimisation_arbre(A)    
    return A
def optimisation_arbre(A):
    
    for el in A.enfants:
            match el.type_nd:
                case"nd_add":
                    if len(el.enfants)>=2:
                        if el.enfants[0].type_nd=="nd_const" and el.enfants[1].type_nd=="nd_const":
                                    el.valeur_nd=el.enfants[0].valeur_nd+el.enfants[1].valeur_nd
                                    el.enfants.pop(0)
                                    el.enfants.pop(0)
                                    el.type_nd="nd_const"
                case "nd_sub":
                    if len(el.enfants)>=2:
                        if el.enfants[0].type_nd=="nd_const" and el.enfants[1].type_nd=="nd_const":
                                
                            el.valeur_nd=el.enfants[0].valeur_nd-el.enfants[1].valeur_nd
                            el.enfants.pop(0)
                            el.enfants.pop(0)
                            el.type_nd="nd_const"
                case"nd_multi":
                    if len(el.enfants)>=2:
                        if el.enfants[0].type_nd=="nd_const" and el.enfants[1].type_nd=="nd_const":                            
                            el.valeur_nd=el.enfants[0].valeur_nd*el.enfants[1].valeur_nd
                            el.enfants.pop(0)
                            el.enfants.pop(0)
                            el.type_nd="nd_const"
            optimisation_arbre(el)