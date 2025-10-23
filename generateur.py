import analyse_lexicale as al
import analyse_syntaxique as asyn
import analyse_semantique as asem
import optimisateur as op


nbLab = 0
ll=0
gen_code_list=[]

def gencode():
    global gen_code_list
    A=op.optim()
    gen_code_list.append("resn "+str(asem.nbVar))
    
    gennode(A)
    gen_code_list.append("drop "+str(asem.nbVar))
    
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
    "nd_receive":nf_element("recv",""),
    "nd_send":nf_element("send","")
}
def gennode(A : asyn.nd):
    global nbLab
    type_node = A.type_nd
    global NF
    global ll
    global gen_code_list
    if type_node in NF:

        gen_code_list.append(NF[type_node].prefixe)if NF[type_node].prefixe else None
        
        for i in range(len(A.enfants)):
            gennode(A.enfants[i])
        gen_code_list.append(NF[type_node].suffixe)if NF[type_node].suffixe else None
        
        return    


    match type_node:
        case "nd_const":
            gen_code_list.append("push "+str(A.valeur_nd))
            
        case "nd_affect":
            if(A.enfants[0].type_nd == "nd_ref") :
                for i in range(len(A.enfants)):
                    gennode(A.enfants[i])
                gen_code_list.append("set "+str(A.enfants[0].index))
            elif(A.enfants[0].type_nd == "nd_ind") :
                gennode(A.enfants[1])
                gen_code_list.append("dup")
                gennode(A.enfants[0].enfants[0])
                gen_code_list.append("write")
        case "nd_ref":
            gen_code_list.append("get "+str(A.index))
            
        case "nd_cond" : 
            l = nbLab + 1
            nbLab +=1
            gennode(A.enfants[0])
            gen_code_list.append("jumpf l" + str(l) + "a")
            
            gennode(A.enfants[1])
            gen_code_list.append("jumpf l" + str(l) + "b")
            
            gen_code_list.append(".l"+str(l)+"a")
            
            if (len(A.enfants) == 3) :
                gennode(A.enfants[2])
            gen_code_list.append(".l"+str(l)+"b")
        case "nd_appel":
            gen_code_list.append("prep "+A.enfants[0].chaine_nd)
            for i in range(1,len(A.enfants)):
                gennode(A.enfants[i])
            gen_code_list.append("call "+str(len(A.enfants)-1))

        case "nd_loop":
            
            temp=ll
            ll=nbLab+1
            nbLab +=1
            gen_code_list.append(".l"+str(ll)+"a")
            
            for fils in A.enfants:
                gennode(fils)
            gen_code_list.append("jump l"+str(ll)+"a")
            
            gen_code_list.append(".l"+str(ll)+"b")
            
            ll=temp
        case "nd_break":
            gen_code_list.append("jump l"+str(ll)+ "b")
           
        case "nd_continue":
            gen_code_list.append("jump l"+str(ll)+ "c")
            
        case "nd_target":
            gen_code_list.append(".l"+str(ll)+ "c")
        case "nd_return":
            for enfant in A.enfants:
                gennode(enfant)
            gen_code_list.append("ret")
        case "nd_func":
          
            gen_code_list.append("."+A.chaine_nd)
            gen_code_list.append("resn "+str(A.valeur_nd))
            for enfant in A.enfants:
                gennode(enfant)
            gen_code_list.append("push 0")
            gen_code_list.append("ret")    
        case "nd_ind" :
            gennode(A.enfants[0])
            gen_code_list.append("read")
        
        case "nd_adress" :
            gen_code_list.append("prep start")
            gen_code_list.append("swap")
            gen_code_list.append("drop 1")
            gen_code_list.append("push 1")
            gen_code_list.append("sub")
            gen_code_list.append("push "+str(A.enfants[0].index))
            gen_code_list.append("sub")
