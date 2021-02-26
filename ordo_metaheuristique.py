import time
import random
import generation
import csv
#Pour le choix d'une solution x aléatoire
def seqAleatoire(n):
    seq=[]
    for i in range(n):
        seq.append(random.randint(1,n));
        while seq[i] in seq[0:i]:
            seq[i]=random.randint(1,n);
    return seq

n=int(input("Saisir combien de tâches souhaitez-vous ordonnancer ? \n"))
tachedetail=[] #cette liste contient les p,w,d des30 taches
taches = [] #cette liste est utilisée pour indexer les taches
#Cette boucle est pour générer les P,W,D et les stocker dans la liste tachedetail
for i in range(n):
    taches.append(i+1)
    tachedetail.append([generation.generer(n)[0][i], generation.generer(n)[1][i], generation.generer(n)[2][i]])
taches=seqAleatoire(n)
#l'écriture des P,W,D dans le fichier
with open("LesDonnesMeta.csv", "w") as new_file:
    csv_writer = csv.writer(new_file, delimiter='\t')
    csv_writer.writerow(['i', 'Pi', 'Wi', 'Di'])
    for i in range(1, n + 1):
        csv_writer.writerow([i, tachedetail[i-1][0],tachedetail[i-1][1], tachedetail[i-1][2]])
#Fonction qui permet de calculer le cout d'execution d'une séquence
def cout(seq):
    ct,ci = 0, 0
    for i in range(len(seq)):
        ci += tachedetail[seq[i]-1][0]
        ct += tachedetail[seq[i]-1][1] * max(0, ci - tachedetail[seq[i]-1][2])
    return ct

#Mes structures de voisinage :
def permutation(s, i, j):
    seq=list(s)
    seq[i], seq[j] = seq[j], seq[i]
    return seq
def insertion(s, i, j):
    temp=s[j]
    del s[j]
    s.insert(i,temp)
    seq = s
    return seq
def left_pivot(l,i):
    l1 = l[0:i]
    l1.reverse()
    l2 = l[i:len(l)]
    l = l1+l2
    return l
#La fonction qui applique la méthode de VNS, le parametre seq_agr n'est autre que les taches indexées dans une liste
def optimisation(seq_arg):
    i = 0
    delais_desire = int(input("Combien de secondes souhaitez-vous laisser au programme pour afficher le résultat ?\n"))
    timeout = time.time() + delais_desire
    xp = [] #xp est le x prime
    #cout_fin contiendra le cout minimal; seq_fin contiendra la sequence qui a permet de l'avoir
    cout_fin = 99999999999999999999999 #un cout maximale pour chercher des couts plus petit afin d'initialiser le cout minimal
    seq_fin = []#
    while True:
#while true pour ne pas sortir de la boucle
#ne sortir de la boucle que lorsque le temps est écoulé !
        if time.time() > timeout:
            break
    #premiere structure de voisinage quand i = 0
        if i == 0:
            min_i = random.randint(0, len(seq_arg) - 1)
            min_j = random.randint(0, len(seq_arg) - 1)
            #premiere permutation aléatoire !
            while min_i == min_j:
                min_i = random.randint(0,len(seq_arg)-1)
                #pour éviter d'avoir une permutation entre un element et lui meme
            xp = permutation(seq_arg, min_i,min_j)
            cout_xp = cout(xp)
            #Je stocke le coup de x' dans la variable xp
            cout_min_xseconde = cout(permutation(xp, 0, 1))
            #normalement le cout minimale de x" sera initialisé par la premiere permutation de x'
            for k in range(len(xp)):
                for j in range(k+1, len(xp)):
                    xseconde = permutation(xp, k, j)
                    #je trouve x" à travers la permutation de x'
                    cout_xsec = cout(xseconde)
                    #je calcule son cout et le stocke dans la variable cout_xsec
                    #à la ligne 87 je vérifie si cette x" a un cout plus petit que tous les autres x"! Pour avoir le minimum
                    #des x"
                    if cout(xseconde) < cout_min_xseconde:
                        xseconde_min = xseconde
                        cout_min_xseconde = cout_xsec
            if cout_min_xseconde < cout_xp:
                xp = xseconde_min
                i = 0
                seq_arg = xseconde_min
                #Si j'ai trouvé un x" qui a un cout inferieur à celui de x', il est mon nouveau x' et je le stocke pour
                #recommencer le voisinage à partir de ce point x"
            else:
                seq_arg = xp
                i = 1
        #Deuxieme structure de voisinage
        if i == 1:
            min_i = random.randint(0, len(seq_arg) - 1)
            min_j = random.randint(1, len(seq_arg) - 1)
            while min_i == min_j:
                min_i = random.randint(0, len(seq_arg) - 1)
            xp = insertion(seq_arg, min_i,min_j)
            cout_xp = cout(xp)
            cout_min_xseconde = cout(insertion(xp,0,2))
            for k in range(len(xp)):
                for j in range(k+1,len(xp)):
                    xseconde = insertion(xp, k, j)
                    cout_xsec = cout(xseconde)
                    #je calcule son cout et le stocke dans la variable cout_xsec
                    #je vérifie si cette x" a un cout plus petit que tous les autres x"! Pour avoir le minimum des x"
                    if cout(xseconde) < cout_min_xseconde:
                        xseconde_min = xseconde
                        cout_min_xseconde = cout_xsec
            if cout_min_xseconde < cout_xp:
                # Si j'ai trouvé un x" qui a un cout inferieur à celui de x', il est mon nouveau x' et je le stocke pour
                # recommencer le voisinage à partir de ce point x"
                xp = xseconde_min
                i=0
                seq_arg = xseconde_min
            else:
                seq_arg = xp
                i=2
        #Troisieme structure de voisinage
        #Le meme raisonnement
        if i == 2:
            xp = left_pivot(seq_arg, random.randint(0,len(seq_arg)-1))
            cout_xp = cout(xp)
            cout_min_xseconde = cout(left_pivot(xp,2))
            for k in range(2,len(seq_arg)):
                xseconde = left_pivot(xp, k)
                cout_xsec = cout(xseconde)
                if cout(xseconde) < cout_min_xseconde:
                    xseconde_min = xseconde
                    cout_min_xseconde = cout_xsec
            if cout_min_xseconde < cout_xp:
                xp = xseconde_min
                seq_arg = xseconde_min
            else:
                # si je suis arrivé à la 3eme struct de voisinnage sans avoir un optimum, je génère une nouvelle séquence
                # aléatoire pour recommencer dès la premiere structure de voisinnage LIGNE 145
                seq_arg = seqAleatoire(n)
            i = 0
    # A chaque itération je vérifie si j'ai obtenu un cout minimale pour avoir x" comme convergeant vers la solution optimale
    # globale
        if cout_min_xseconde < cout_fin:
            cout_fin = cout_min_xseconde
            seq_fin = xseconde_min
    return seq_fin, cout_fin

min_seq, min_cout = optimisation(taches)
injection_resultat=f"La séquence optimale est : {min_seq} \n Le cout minimal est {min_cout}"
with open("resultat_meta.csv", "w") as new_file:
    new_file.write(injection_resultat)