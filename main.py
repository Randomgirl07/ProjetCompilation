import analyse_lexicale as al
import analyse_syntaxique as asyn
import optimisateur as op
import generateur as gen

print(".start")
al.init(r"C:\Users\user\Desktop\test.txt")
while (al.T.type_token!=al.tokens.index("tok_eof")):
  
    gen.gencode()
print("halt")
