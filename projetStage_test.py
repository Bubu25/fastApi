import random
import datetime
from datetime import date, time, datetime


dicNoms={"Paul":0, "Pierre":0,"Musa":0,"Aline":0, "charlotte":0}
print(len(dicNoms))
noms=['Paul','Pierre','Musa','Aline', 'charlotte']
nombreSemaines=10

#y=random.choice(dicNoms)
#print(y)


for i in range(1,nombreSemaines+1):
    z = random.choice(noms)
    print(f"semaine {i}, {z} paye son café")
    pos=noms.index(z)
    del noms[pos]
    dicNoms[z]=dicNoms[z]+1
    #print(noms2)
    long=len(noms)
    #print(long)
    if long == 0:
        noms=['Paul','Pierre','Musa','Aline', 'charlotte']
        #print(noms2)
print(dicNoms)

d=date.today()
p=date.isocalendar(d)[1]

