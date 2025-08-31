import analyse_lexicale as al
import analyse_syntaxique as asyn
import optimisateur as op
def gencode():
    A=op.optim()
    gennode(A)

def gennode(A):
    type_node = asyn.nodes[A.type_nd]
    match type_node:
        case "nd_const":
            print("push "+str(A.valeur_nd))
        case "nd_not":
            gennode(A.enfants[0])    
            print("not")
        case "nd_moins":
            print("push 0")
            gennode(A.enfants[0])
            print("sub")
