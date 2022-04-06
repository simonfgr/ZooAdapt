"""Maj: export du fichier export.txt au bon endroit (dans le lien donné) + inversion des fichiers à supprimer !!!!!
ajout du maximum mou max Depth.
ajout de latitude/longitude start et End.
Attention, le nom des différents fichiers ne doit pas changer !!
Création de WP2List + createDir +maj créate dir
Création liste des adress des pid
save avant changement de la fonction export pour exporter plusieurs fichiers texte àn partir de chaque pid"""

import csv
import os
import locale   #Pour transformation de ',' en '.' (pour avoir des réels et non des entiers)
import time
#import numpy as np
locale.setlocale(locale.LC_ALL, 'fr_FR') # windows :locale.setlocale(locale.LC_ALL, 'french')


mot1 = "Bord"  #La colonne bord du fichier pid est utilisée pour déterminer les images coupées
mot2 = "Prediction" #La colonne prédiction du fichier pid est utilisée pour connaitre le nom du dossier ou chercher les images
mot3 = "Sonde ref. (m)"  # La colonne sonde du fichier csv est utilisée pour récuperer la profondeur max 
lien = '/Users/simonfeger/Desktop/Work/pour_ecotaxa_propre' #input('lien :')   #Tout doit se trouver au même en droit dans le dissier importé
adressPid = lien + '/WP2_0001/valid_PELGAS2021_WP2_1.pid'
adressCsv = lien + '/20210426_132330_20210527_093800_pelgas2021.csv'
adressVignettes = lien + '/WP2_0001/Vignettes'
separateurPid = '\t'
separateurCsv = ';'
formatImg = ".jpg"  # Format toujours en .JPG !!


def WP2listing(path):
    """Cette fonction prend en argument le lien contenant les dossier WP2 souhaité et renvoie une liste des différents dossier WP2 qui s'y trouvent"""
    fold = os.listdir(path)
    WP2list = []
    for i in fold:
        if "WP2" in i:
            WP2list.append(i)
    return WP2list

WP2list=WP2listing(lien)

def createDir(Path):
    """Cette fonction créé les dossiers export correspondant à chaque dossier de WP2 dans le lien donné en entrée
    Elle renvoie aussi les chemin des fichiers créés."""
    NewPath = []
    for dos in WP2list:
        print(dos)
        chemin = Path+'/'+dos+'_exp'
        os.mkdir(Path+'/'+dos+'_exp') #Les dossiers WP2_exp sont créés au même endroit que les originaux
        print('created dir '+ Path+'/'+dos+'_exp')
        NewPath.append(chemin)
    print (NewPath)

createDir(lien)

def FindPathFile(link, Fname):
    """
    Cette fonction prend en argument le lien d'un dossier ainsi qu'une partie du nom du dossier/Fichier recherché.
    Elle retourne le chemin du fichier recherché.
    Cette fonction ne fouille pas dans les sous dossiers !!
    """
    inLink = os.listdir(link)
    Path=''
    for i in inLink:
        if Fname in i:
            print("found "+ i)
            Path = link+'/'+i
            return(Path)
        else:
            print('not here '+i)
    """for i in inLink:       #Cette partie est créé dans le cas ou l'on souhaiterai fouiller dans les sous-dossiers
        for j in WP2list:
            secondPath = path + '/' + j
            for s in secondPath:
                if Fname in s:
                    print('found '+s+' in WP2')
                    Path = secondPath+'/'+s"""
    return Path




#making a list of .pid adress
adressPidList = []
for i in WP2list:
    adress= FindPathFile(lien, i)
    adressPidList.append(adress)




adressCsv = FindPathFile(lien, '.csv')
adressPid = FindPathFile(lien, '.pid')
print(adressCsv)
print(adressPid)


def Find(mot, fileAdress, separateur):
    """cette fonction retourne les coordonnées d'un mot dans un tableau"""
    fh = open(fileAdress, encoding="utf8", errors='ignore')
    reader = csv.reader(fh, delimiter=separateur)
    i = -1
    loc1 = []
    for ligne in reader:
        i += 1
        if mot in ligne:
            loc1.append(i)
            loc1.append(ligne.index(mot1))
    return loc1



def Export():
    """Cette fonction créer un fichier txt en copie du pid mais suprime les lignes du fichier indiqué pour 'adress' qui ont dans la colonne 'Bord' un charactère différent de 0.
    Elle ajoute aussi la valeur maximum de la colonne Sonde ref. (m) à la ligne max Depth"""
    colBord=Find(mot1, adressPid, separateurPid)[1]
    colPred=Find(mot2, adressPid, separateurPid)[1]
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
                    if l[colBord] == "0":       #Lorsque la colonne en l(col) - soit la colonne Bord - possède un caractère = à 0 alors:
                        fd1.write(line)     #la ligne est copiée dans le fichier créé (fd1) 
                else:
                    if "Latitude" not in line and "Longitude"not in line and "Max Depth = 0.000"not in line :
                        fd1.write(line)         #Cette ligne permet de copier dans le nouveau fichier les lignes précédents le tableau.


def supfile():
    colBord=Find(mot1, adressPid, separateurPid)[1]
    colPred=Find(mot2, adressPid, separateurPid)[1]
    """Cette fonction supprime les vignettes dont la colonne 'Bord' est différente de 0 dans le .pid en retrouvants les images par leur nom donné dans le .pid"""
    with open(adressPid, 'r', encoding="utf8", errors='ignore') as fd:   #ouvertur du fichier indiqué à l'adresse en mode lecture en tant que fd
        for line in fd:
            body = False                                    #Nous considérons au début que nous ne sommes pas dans le 'body' (=tableau et non entête) 
            for line in fd:                                     #parcourons les lignes de fd
                if line.startswith("1") and not body:           #Commencons à parcourir les colonnes à partir de la ligne de l'objet '1'    (Sécurité 1 ?)
                    body = True
                if body == True and line.count('\t')>10:   #Pour parcourir les colonnes d'une ligne, utilisons \t pour différencier les données entre chaque tabulation. Et pour être sur de commencer au bon endroit, il faut avoir parcouru au moins 10 lignes (sécurtié 2?)
                    l = line.split("\t")
                    if l[colBord] != "0":       #Lorsque la colonne en l(col) - soit la colonne Bord - possède un caractère = à 0 alors:
                        fname=l[1]+'_'+l[0]
                        fdos=l[colPred]
                        ad = adressVignettes +'/'+ fdos +'/'+ fname+formatImg  
                        try:
                            os.remove(ad)
                            #print("Fichier supprimer :"+ad)
                        except:
                            print("pas de fichier: " + ad)
    


def findMaxDepth(colonne,adresse,separateur):
    """Cette fonction recherche  et renvoie la profondeur max de la colonne choisie du fichier CSV"""
    with open(adresse, 'r', encoding="utf8", errors='ignore') as fd:   #ouvertur du fichier indiqué à l'adresse en mode lecture en tant que fd
        reader = csv.reader(fd, delimiter=separateur)
        i = -1
        loc3 = []
        max = 0
        for ligne in reader:
            i += 1
            if colonne in ligne:
                loc3.append(i)
                loc3.append(ligne.index(colonne))
            try :
                data = locale.atof(ligne[loc3[1]])
                if max<data:
                    max =  data
            except :
                print("NAN in CSV file to Sonde ref. (m)",loc3)
    return max

def findStart():
    """Cette fonction recherche et renvoie la latitude/logitude de départ et la latidue/longitude d'arrivée
    Pour ne pas utiliser de fonction max, qui pourrait inverser le sens du trajet parcouru par le bateau, la fonction récupère
    uniquement le premier et le dernier élement des colonnes longitude et latitude.
    Cette fonction renvoie aussi l'adresse des colonnes 'latitude' et 'longitude'"""
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
                LatStart=nextline[colLat]   #récupère la première valeur de la colonne Latitude
                LonStart=nextline[colLon]       #récupère la première valeur de la colonne Longitude
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




latlonStart = findStart()[0]   #le O fait permet de récuperer uniquement latlonStart et non pas colLat et colLon
colLat = findStart()[1]
colLon = findStart()[2]
latlonEnd = findEnd(colLat, colLon)



#?? loc3 = findMaxDepth(mot3)

supfile()
max = findMaxDepth(mot3,adressCsv,separateurCsv)
Export()

print("lat/lon start :",latlonStart)
print("lat/lon end : ",latlonEnd)



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
