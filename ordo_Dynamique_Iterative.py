import csv
from itertools import chain, combinations
import generation
import time
pi = []
wi = []
di = []
n = input("Saisir combien de taches souhaitez-vous ordonnancer ? \n")

k=tuple(range(1,n+1))
#la fonction qui supprime un element dans l'ensemble des taches, elle facilite comment retrouver les sous taches de J
def supp(c,chaine):
    res=[]
    if chaine[0]==c:
        res=chaine[1:]
    for j in range(len(chaine)):
        if c==chaine[j]:
            res=chaine[0:j]+chaine[j+1:]
    return res

# Cette boucle pour generer les donnees des taches en respectant les contraintes du poids
# chose qui existe deja dans la fonction generer
for i in range(n):
    pi.append(generation.generer(n)[0][i])
    wi.append(generation.generer(n)[1][i])
    di.append(generation.generer(n)[2][i])
#enregistrer les donnees generes dans un fichier csv sous le nom LesDonnesDyna
with open("LesDonnesDyna.csv", "w") as new_file:
    csv_writer = csv.writer(new_file, delimiter='\t')
    csv_writer.writerow(['i', 'Pi', 'Wi', 'Di'])
    for i in range(1, n + 1):
        csv_writer.writerow([i, pi[i - 1], wi[i - 1], di[i - 1]])

#pour generer les sequenses possibles
# i c'est le nombre de chaque sequence
debut = time.time()
def all_subsets(ss,i):
    return chain(*map(lambda x: combinations(ss, x), range(i,i+1)))
#Combinaison est une liste qui stoque les differentes sous listes (sous taches)
combinaison=[]
for subset in all_subsets(k,2):
    combinaison.append(subset)

#pour calculer la condition initiale qui est l'execution d'une seule tache
def f1(i):
    return wi[i[0]-1]*max(0,(pi[i[0]-1]-di[i[0]-1]))

#pour calculer les valeurs optimales de 2 combinaisons
def f2(i):
    ci=0
    for j in range(len(i)):
        ci+=pi[int(i[j])-1]
    resultP={}
    resultP[str(i[0])+" => "+str(i[1])]=f1(supp(i[1],i))+wi[int(i[1])-1]*max(0,(ci-di[int(i[1])-1]))
    resultP[str(i[1])+" => "+str(i[0])]=f1(supp(i[0],i))+wi[int(i[0])-1]*max(0,(ci-di[int(i[0])-1]))
    #min=min_dic(resultP)
    mino=min(resultP.values())
    n=resultP.values().index(mino)
    v=resultP.keys()[n]
    #chemin.append(v)
    return mino,v


etapeII={}

for i in range(len(combinaison)):
    etapeII[combinaison[i]]=f2(combinaison[i])

for i in range(3,len(k)+1):
    combinaison1=[]
    for subset in all_subsets(k,i):
        combinaison1.append(subset)
    for t in range(len(combinaison1)):
        resultP={}
        for h in range(len(combinaison1[t])):
            ci=0
            for j in range(len(combinaison1[t])):
                ci+=pi[combinaison1[t][j] - 1]
            r=supp(combinaison1[t][h], combinaison1[t])
            resultP[etapeII[r][1] +' => ' + str(combinaison1[t][h])]= etapeII[r][0] + wi[combinaison1[t][h] - 1] * max(0, (ci - (di[combinaison1[t][h] - 1])))
        mino=min(resultP.values())
        n=resultP.values().index(mino)
        v=resultP.keys()[n]
        etapeII[combinaison1[t]]=(mino, v)
fin = time.time()


with open('resultat.txt','w') as resultat:
    resultat.write("-la valeur optimal est :"+str(etapeII[k][0])+"\n")

    resultat.write("-La sequence optimal est : \n")
    resultat.write("-"*len(str(etapeII[k][1])) +"\n")
    resultat.write('|'+str(etapeII[k][1])+'|\n')
    resultat.write("-"*len(str(etapeII[k][1])) +"\n")
    resultat.write("Le temps d'execution est : "+str(fin - debut)+" secondes.")