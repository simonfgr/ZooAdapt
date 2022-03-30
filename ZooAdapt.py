"""Maj: export du fichier export.txt au bon endroit (dans le lien donné) + inversion des fichiers à supprimer !!!!!
ajout du maximum mou max Depth.
ajout de latitude/longitude start et End.
Attention, le nom des différents fichiers ne doit pas changer !!"""

import csv
import os
import locale   #Pour transformation de ',' en '.' (pour avoir des réels et non des entiers)
#import numpy as np

mot1 = "Bord"
mot2 = "Prediction"
mot3 = "Sonde ref. (m)"
valeur = 'Bord'
colonne = "Bord"
lien = '/Users/simonfeger/Desktop/Work/pour ecotaxa' #input('lien :')
adressPid = lien + '/WP2_0001/valid_PELGAS2021_WP2_1.pid'
adressCsv = lien + '/20210426_132330_20210527_093800_pelgas2021.csv'
adressVignettes = lien + '/WP2_0001/Vignettes'
separateur = '\t'
separateurCsv = ';'

locale.setlocale(locale.LC_ALL, 'fr_FR') # windows :locale.setlocale(locale.LC_ALL, 'french')


def Find(mot1,mot2, adressPid, separateur):
    """cette fonction retourne les coordonnées d'un mot dans un tableau"""
    fh = open(adressPid, encoding="utf8", errors='ignore')
    reader = csv.reader(fh, delimiter=separateur)
    i = -1
    loc1 = []
    loc2 = []
    for ligne in reader:
        i += 1
        if mot1 in ligne:
            loc1.append(i)
            loc1.append(ligne.index(mot1))
        if mot2 in ligne:
            loc2.append(i)
            loc2.append(ligne.index(mot2))
    return loc1, loc2



def Export():
    """Cette fonction créer un fichier txt en copie du pid mais suprime les lignes du fichier indiqué pour 'adress' qui ont dans la colonne 'Bord' un charactère différent de 0.
    Elle ajoute aussi la valeur maximum de la colonne Sonde ref. (m) à la ligne max Depth"""
    col1=Find(mot1,mot2, adressPid, separateur)[0][1]
    col2=Find(mot1,mot2, adressPid, separateur)[1][1]
    with open(adressPid, 'r', encoding="utf8", errors='ignore') as fd:   #ouvertur du fichier indiqué à l'adresse en mode lecture en tant que fd
        with open( lien + "/export.txt", "w") as fd1:                         #Création d'un fichier texte en tant que fd1
            body = False    #Nous considérons au début que nous ne sommes pas dans le 'body' (=tableau et non entête) 
            count = 0 #testttttt                                
            for line in fd:                     #parcourons les lignes de fd
                count +=1
                if "Longitude start = 0.000"in line:
                    fd1.write("Longitude start = "+latlonStart[1]+"\n")
                if "Longitude end = 0.000" in line:
                    fd1.write("Longitude end = "+latlonEnd[1]+"\n")
                if "Latitude start = 0.000" in line:
                    fd1.write("Latitude start = "+latlonStart[0]+"\n")
                if "Latitude end = 0.000" in line:
                    fd1.write("Latitude end = "+latlonEnd[0]+"\n")
                if "Max Depth = 0.000" in line:
                    fd1.write("Max Depth (m???) = " + str(max) +"\n")  
                    #fd[11]= "Max Depth = " + str(max)
                if line.startswith("1") and not body:           #Commencons à parcourir les colonnes à partir de la ligne de l'objet '1'    (Sécurité 1 ?)
                    body = True
                if body == True and line.count('\t')>10:   #Pour parcourir les colonnes d'une ligne, utilisons \t pour différencier les données entre chaque tabulation. Et pour être sur de commencer au bon endroit, il faut avoir parcouru au moins 10 lignes (sécurtié 2?)
                    l = line.split("\t")
                    if l[col1] == "0":       #Lorsque la colonne en l(col) - soit la colonne Bord - possède un caractère = à 0 alors:
                        fd1.write(line)     #la ligne est copiée dans le fichier créé (fd1) 
                else:
                    if "Latitude" not in line and "Longitude"not in line and "Max Depth = 0.000"not in line :
                        fd1.write(line)         #Cette ligne permet de copier dans le nouveau fichier les lignes précédents le tableau.


def supfile():
    col1=Find(mot1,mot2, adressPid, separateur)[0][1]
    col2=Find(mot1,mot2, adressPid, separateur)[1][1]
    """Cette fonction supprime les vignettes dont la colonne 'Bord' est différente de 0 dans le .pid en retrouvants les images par leur nom donné dans le .pid"""
    with open(adressPid, 'r', encoding="utf8", errors='ignore') as fd:   #ouvertur du fichier indiqué à l'adresse en mode lecture en tant que fd
        for line in fd:
            body = False                                    #Nous considérons au début que nous ne sommes pas dans le 'body' (=tableau et non entête) 
            for line in fd:                                     #parcourons les lignes de fd
                if line.startswith("1") and not body:           #Commencons à parcourir les colonnes à partir de la ligne de l'objet '1'    (Sécurité 1 ?)
                    body = True
                if body == True and line.count('\t')>10:   #Pour parcourir les colonnes d'une ligne, utilisons \t pour différencier les données entre chaque tabulation. Et pour être sur de commencer au bon endroit, il faut avoir parcouru au moins 10 lignes (sécurtié 2?)
                    l = line.split("\t")
                    if l[col1] != "0":       #Lorsque la colonne en l(col) - soit la colonne Bord - possède un caractère = à 0 alors:
                        fname=l[1]+'_'+l[0]
                        fdos=l[col2]
                        ad = adressVignettes +'/'+ fdos +'/'+ fname+'.jpg'  #!!!!!!!!!!!Il faut que les images soient en .jpg
                        try:
                            os.remove(ad)
                            #print("Fichier supprimer :"+ad)
                        except:
                            print("pas de fichier: " + ad)
    


def findMaxDepth(mot3):
    """Cette fonction recherche  et renvoie la profondeur max de la colonne Sonde ref. (m) du fichier CSV"""
    with open(adressCsv, 'r', encoding="utf8", errors='ignore') as fd:   #ouvertur du fichier indiqué à l'adresse en mode lecture en tant que fd
        reader = csv.reader(fd, delimiter=separateurCsv)
        i = -1
        loc3 = []
        max = 0
        for ligne in reader:
            i += 1
            if mot3 in ligne:
                loc3.append(i)
                loc3.append(ligne.index(mot3))
            try :
                data = locale.atof(ligne[loc3[1]])
                if max<data:
                    max =  data
            except :
                print("NAN in CSV file to Sonde ref. (m)")
    return max

def findStart():
    """Cette fonction recherche et renvoie la latitude/logitude de départ et la latidue/longitude d'arrivée
    Pour ne pas utiliser de fonction max, qui pourrait inverser le sens du trajet parcouru par le bateau, la fonction récupère
    uniquement le premier et le dernier élement des colonnes longitude et latitude """
    with open(adressCsv, 'r', encoding="utf8", errors='ignore') as fd:   #ouvertur du fichier indiqué à l'adresse en mode lecture en tant que fd
        reader = csv.reader(fd, delimiter=separateurCsv)
        i = -1
        latlonStart = []
        colLat=0
        colLon=0
        max = 0
        for ligne in reader:
            i += 1
            if "Latitude" in ligne:
                nextline = next(reader)
                colLat = ligne.index("Latitude")
                colLon = ligne.index("Longitude")
                LatStart=nextline[ligne.index("Latitude")]
                LonStart=nextline[ligne.index("Longitude")]
                latlonStart.append(LatStart)
                latlonStart.append(LonStart) 
                return latlonStart, colLat, colLon


def findEnd(colLat, colLon):
    with open(adressCsv, 'r', encoding="utf8", errors='ignore') as fd:   #ouvertur du fichier indiqué à l'adresse en mode lecture en tant que fd
        reader = csv.reader(fd, delimiter=separateurCsv)
        latlonEnd = []
        lastLine = fd.readlines()[-1]
        l = lastLine.split(";")
        latlonEnd.append(l[colLat])
        latlonEnd.append(l[colLon])
        return latlonEnd





latlonStart = findStart()[0]
colLat = findStart()[1]
colLon = findStart()[2]
latlonEnd = findEnd(colLat, colLon)



#?? loc3 = findMaxDepth(mot3)

supfile()
max = findMaxDepth(mot3)
Export()

print(latlonStart)
print(latlonEnd)



#























"""
def Find2(valeur,colonne,adressPid,separateur):
    fh = open(adressPid, encoding="utf8", errors='ignore')
    reader = csv.reader(fh, delimiter =separateur)
    i=-1
    for ligne in reader:
        i+=1
        if ("\t" +colonne+ "\t") in ligne:
            loc = []
            loc.append(i)
            loc.append(ligne.index(colonne))
            print (loc)

###Find2(valeur, colonne,  adressPid, separateur)


def test(valeur,colonne,adressPid,separateur):
    """"""Cette fonction trouve les valeur 0 dans la colonne choisie""""""
    fh = open(adressPid, encoding="utf8", errors='ignore')
    reader = csv.reader(fh, delimiter =separateur)
    i=-1
    colCible=0
    for ligne in reader:
        i+=1
        for col in ligne:
            if col ==valeur:
                print (valeur,"localisé en ligne :",i,"colonne : ", ligne.index(col))
                colCible = ligne.index(col)
        print (ligne[colCible])
        if ligne[colCible] != "0":
            writer = csv.writer(fh, delimiter =separateur)
            print("found", writer.index(ligne))



#test(valeur, colonne,  adressPid, separateur)





def tabl(adress):
    """"""
    col = loc[1]
    myFile = open("essai.txt", "w+")
    fh = open(adressPid, encoding="utf8", errors='ignore')
    reader = csv.reader(fh, delimiter=separateur)
    table = []
    for ligne in reader:
        if "!Item" in ligne:
            print("yes")
            print(col)
            if ligne[col] == 0:
                ligne = str(ligne)
                myFile.write("testttt")
                myFile.write(ligne)
                myFile.write("\n")

# tabl(adress)
"""

"""def replaceMax():
    with open( lien + "/export.txt", "w") as fd1:  
        writer = csv.writer(fd1, delimiter=separateurCsv)
        reader = csv.reader(fd1, delimiter=separateurCsv)
        count = 0
        for i in fd1:
            count +=1
            if "Max Depth = 0.000" in i:
                print(count)
                fd1[11]= "Max Depth = " + str(max)
"""
