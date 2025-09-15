import analyse_lexicale as al
import analyse_syntaxique as asyn
import analyse_semantique as asem
import optimisateur as op

nbLab = 0
ll=0


def gencode():
    A=op.optim()
    print("resn " + str(asem.nbVar))
    gennode(A)
    print("drop  " +str(asem.nbVar))

# nodes=["nd_eof","nd_const","nd_ident","nd_plus","nd_moins","nd_multi","nd_div","nd_modulo","nd_and","nd_or",
# "nd_not","nd_equal","nd_not_equal","nd_low","nd_gre","nd_leq","nd_geq","nd_par_open","nd_par_close","nd_bra_open","nd_bra_close",
# "nd_cur_open","nd_cur_close","nd_semicolon","nd_affect","nd_adress","nd_int","nd_void","nd_return","nd_if","nd_for","nd_else","nd_do",
# "nd_while","nd_continue","nd_break","nd_send","nd_debug","nd_receive","nd_comma","nd_sub"]
class nf_element:
    suffixe:str
    prefixe: str

   
    def __init__(self,s,p):
        self.suffixe=s
        self.prefixe=p
        
NF={
    "nd_not":nf_element("not",""),
    "nd_add":nf_element("add",""),
    "nd_moins":nf_element("sub","push 0"),
    "nd_sub":nf_element("sub",""),
    "nd_multi": nf_element("mul",""),
    "nd_div": nf_element("div",""),
    "nd_modulo": nf_element("mod",""),
    "nd_and": nf_element("and",""),
    "nd_or": nf_element("or",""),
    "nd_equal":nf_element("cmpeq",""),
    "nd_not_equal":nf_element("cmpne",""),
    "nd_low":nf_element("cmplt",""),
    "nd_gre":nf_element("cmpgt",""),
    "nd_leq":nf_element("cmple",""),
    "nd_geq":nf_element("cmpge",""),
    "nd_debug":nf_element("dbg",""),
    "nd_block":nf_element("",""),
    "nd_seq":nf_element("",""),
    "nd_drop":nf_element("drop 1",""),
    "nd_decl":nf_element("","")

}
def gennode(A : asyn.nd):
    global nbLab
    type_node = asyn.nodes[A.type_nd]
    global NF
    global ll
    if type_node in NF:
        print(NF[type_node].prefixe) if NF[type_node].prefixe else None
        for i in range(len(A.enfants)):
            gennode(A.enfants[i])
        print(NF[type_node].suffixe) if NF[type_node].suffixe else None
        return    


    match type_node:
        case "nd_const":
            print("push "+str(A.valeur_nd))
        case "nd_affect":
            for i in range(len(A.enfants)):
                gennode(A.enfants[i])
            print("set "+str(A.enfants[0].index))
        case "nd_ref":
            print("get "+str(A.index))
        case "nd_cond" : 
            l = nbLab + 1
            nbLab +=1
            gennode(A.enfants[0])
            print("jumpf l" + str(l) + "a")
            gennode(A.enfants[1])
            print("jumpf l" + str(l) + "b")
            print(".l"+str(l)+"a")
            if (len(A.enfants) == 3) :
                gennode(A.enfants[2])
            print(".l"+str(l)+"b")
        case "nd_loop":
            
            temp=ll
            ll=nbLab+1
            nbLab +=1
            print(".l"+str(ll)+"a")
            for fils in A.enfants:
                gennode(fils)
            print("jump l"+str(ll)+"a")
            print(".l"+str(ll)+"b")
            ll=temp
        case "nd_break":
        
            print("jump l"+str(ll)+ "b")
        case "nd_continue":
            print("jump l"+str(ll)+ "c")
        case "nd_target":
            print(".l"+str(ll)+ "c")