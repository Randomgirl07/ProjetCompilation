import analyse_lexicale as al
import analyse_syntaxique as asyn
import optimisateur as op
import generateur as gen
import analyse_semantique as asem


al.init(r".\lib.txt")
asem.begin()
while (al.T.type_token!="tok_eof"):
    gen.gencode()
al.init(r".\test.txt")
while (al.T.type_token!="tok_eof"):
    gen.gencode()
asem.end()
gen.gen_code_list.append(".start")
gen.gen_code_list.append("prep main")
gen.gen_code_list.append("call 0")
gen.gen_code_list.append("halt")
for i in range (1, len(gen.gen_code_list)-3) :
    if gen.gen_code_list[i] == "set 0" and gen.gen_code_list[i-1] == "dup" and gen.gen_code_list[i+1] == "drop" :
        gen.gen_code_list.pop(i-1)
        gen.gen_code_list.pop(i)
    elif "jump" in gen.gen_code_list[i] :
        label = gen.gen_code_list[i].split()[1]
        if gen.gen_code_list[i+1] == label :
            gen.gen_code_list.pop(i)
            gen.gen_code_list.pop(i)
        elif gen.gen_code_list[i+2] == label and ".l" in gen.gen_code_list[i+1] :
            gen.gen_code_list.pop(i)
            gen.gen_code_list.pop(i+1)

for el in gen.gen_code_list:
    print(el)
