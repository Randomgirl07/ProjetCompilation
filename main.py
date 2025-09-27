import analyse_lexicale as al
import analyse_syntaxique as asyn
import optimisateur as op
import generateur as gen


gen.gen_code_list.append(".start")
al.init(r"C:\Users\user\Desktop\test.txt")
while (al.T.type_token!="tok_eof"):
    gen.gencode()

gen.gen_code_list.append("halt")
for el in gen.gen_code_list:
    print(el)
