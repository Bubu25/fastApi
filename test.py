dico={}
dico2={}
dico['nom']=2
dico['prenom']=3
dico3=dico2.update(dico)
print ("d",dico3)
print(len(dico))
list=[]
for u in dico:
    a=dico.get(u)
    list.append(a)
    print(a)
print(list)
if 2 not in list:
    print("ah ah")

i=0
i+=2
i-=2
print(i)
a='b'
c='o'
i=1
print(a+str(i))
