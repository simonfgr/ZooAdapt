import streamlit as st
from os import listdir, mkdir, makedirs,path
from glob import glob
from pandas import read_csv, read_excel
from shutil import copy
from threading import Thread


bord="Bord"
prediction="Prediction"
sonde="Sonde ref. (m)" 
sepPid='\t'
sepCsv=';'
formatImg = ".jpg"

deleted_files_number_total=0
ls_deleted_objects_wp=[]


##################FONCTIONS######################

def ls(Path, part_of_name):
    """
    Cette fonction prend en argument un Path et une chaine de charactère.
    Cette fonction recherche dans Path les dossiers et/ou fichiers contenant la chaine de charactère indiquée.
    Cette fonction retourne la liste des noms trouvés
    """
    fold=listdir(Path)
    WP2list=[]
    for i in fold:
        if part_of_name in i:
            WP2list.append(i)
            #readOnlyText.insert('end',i+" found\n")
    print(WP2list,'found')
    return WP2list


def create_dos(ExportPath,dosname,suffixe):
    """
    Cette fonciton prend en argument un chemin, un nom de dossier et un suffixe pour le nom de dossier
    Cette fonction créé au chemin d'export indiqué, un dossier ayant pour nom le nom indiqué (dosname)+suffixe 
    Cette fonction revnoie la liste des chemins des dossiers créés
    """
    chemin = ExportPath+'/'+dosname+suffixe
    if not path.exists(chemin):
        mkdir(chemin)
        print ('Created directory :',chemin)
        #readOnlyText.insert('end','Created directory : '+chemin+"\n")

    else:
        print(chemin, " already exist")
        #readOnlyText.insert('end',chemin+ " already exist\n")
    return chemin

def pid_with_pandas(file_path,Data,separateur):
    """
    Cette fonction prends en argument le chemin d'un fichier.pid, la séparateur entre l'entête et le corps (Data) en tant que chaine de charactère et le séparateur dur fichier pid.
    Cette fonction permet douvrir le tableau de données contenu dans le fichier pid comme étant un CSV sans prendre compte de son entête.
    Cette fonction renvoie le tableau de données du fichier pid sans l'entête.
    """
    data_idx= 0
    with open(file_path) as f:
        for idx, line in enumerate(f.readlines()):
            if line.strip() == Data:
                data_idx = idx +1
                break
    return read_csv(file_path,skiprows=data_idx,sep=separateur)

def index_in_col(file_oppened, col_name,word):
    """
    Cette fonction prends en argument un tableau ouvert avec pandas, le nom d'une colonne du tableau et le mot recherché
    Cette fonction renvoie l'index de la ligne du mot recherchée dans la colonne indiqué
    """
    station=[]
    k=0
    for j in file_oppened[col_name]:
        if word == j:
            station.append((k))
        k+=1
    return station


def export(i):
    k=0
    for col in pid_df[i]:
        if col == "Bord":
            colBord=k
        k+=1
    with open(adressPidList[i], 'r', encoding="utf8", errors='ignore') as fd:
        with open(NewPath[i] + "//export.txt", "w") as fd1:
            body= False
            for line in fd:  # parcourons les lignes de fd
                if "Ship" in line:
                    if station == 1:
                        fd1.write('Station = '+stationList[i]+'\n')
                    if Z == 1:
                        fd1.write('zmin = '+str(Xlsx['zmin'][i])+'\n')
                        fd1.write('zmax = '+str(Xlsx['zmax'][i])+'\n')    #fd1.write(' = ' +)
                if "Max Depth = 0.000" in line:
                    fd1.write("Max Depth (m???) = " + str(MaxDepthList[i]).replace(".", ",") + "\n")
                    fd1.write('Volume = '+str(Xlsx['volume'][i])+'\n')
                if "Longitude start = 0.000" in line:
                    if latlon == 1:
                        fd1.write("Longitude start = "+startendlon[i][0]+"\n")
                if "Longitude end = 0.000" in line:
                    if latlon == 1:
                        fd1.write("Longitude end = "+startendlon[i][-1]+"\n")
                if "Latitude start = 0.000" in line:
                    if latlon == 1:
                        fd1.write("Latitude start = "+startendlat[i][0]+"\n")
                if "Latitude end = 0.000" in line:
                    if latlon == 1:
                        fd1.write("Latitude end = "+startendlat[i][-1]+"\n")
                if line.startswith('[Data]') and not body:
                    body = True 
                if body == True and line.count('\t') > 10:
                    l = line.split("\t")
                    if l[colBord] == "0": 
                        fd1.write(line)
                else:
                    if "Latitude" not in line and "Longitude"not in line and "Max Depth = 0.000"not in line:
                        fd1.write(line)



frac_wp=""

def image_creator(i):
    """
    Cette fonction est juste moche pour le moment (:
    """
    global deleted_files_number_total,ls_deleted_objects_wp
    k=0
    #readOnlyText.insert('end','WP2_'+str(i+1)+'/'+str(len(pid_df))+" Please wait ..\n")
    for col in pid_df[i]:
        if col == "Bord":
            colBord=k
        if col == "Prediction":
            colPred=k
        k+=1
    print('Creating files. Please wait...')
    #frac_wp = (i+1),"/",len(pid_df)
    #nbrWP_progress=Label(root, text=frac_wp,background="LightBlue3")
    #nbrWP_progress.grid(row=12, column=1)
    with open(adressPidList[i], 'r', encoding="utf8", errors='ignore') as fd:  # ouvertur du fichier indiqué à l'adresse en mode lecture en tant que fd
        k=0
        for line in fd:
            body = False
            for line in fd:  # parcourons les lignes de fd
                msg='WP2_'+str(i+1)+'/'+str(len(pid_df))+' line :'+str(k)+'/'+str(len(pid_df[i]))
                print(msg)
                #my_bar.progress(int((k/len(pid_df[i]))*100))
                k+=1
                if line.startswith("[Data]") and not body:
                    body = True
                if body == True and line.count('\t') > 10:
                    l = line.split("\t")
                    if l[colBord] == "0":
                        fname = l[1]+'_'+l[0]
                        fdos = l[colPred]
                        ad = Path+'//' + WP2list[i] + '/'+'Vignettes'+'//' + fdos + '//' + fname+formatImg              #DUBLE
                        if path.exists(ad):
                            #print(ad)  #Permet d'afficher tout les chemins de fichier examinés lorsqu'ils existent
                            if path.exists(NewPath[i]+'//'+fdos):
                                if not path.exists(NewPath[i]+'//'+fdos+'//'+fname+formatImg):
                                    # En période de testtttt -=-=-=-=-=-=-=-==-=-==-===-=-=-
                                    filePath = copy(ad, NewPath[i]+'//'+fdos+'//'+fname+formatImg)
                                    #os.remove(ad)  #ce code permettait de supprimer directement les images
                                    #print("Fichier supprimé :"+ad)
                            else:
                                makedirs(NewPath[i]+'//'+fdos+'//')
                                filePath = copy(ad, NewPath[i]+'//'+fdos+'//'+fname+formatImg)
                            # else:
                            #     print('Path does not exist : ',ad)   #Cette partie permet d'avoir en log les fichiers qui ont déjà été supprimer aupréalable
                    else:
                        deleted_files_number_total+=1
                        ls_deleted_objects_wp[i]+=1
                        fname = l[1]+'_'+l[0]
                        fdos = l[colPred]
                        ad = Path+'//' + WP2list[i] + '/'+'Vignettes'+'//' + fdos + '//' + fname+formatImg              #DUBLE
                        #readOnlyText.insert('end',"Deleted thumbnail : "+ad+"\n")
                        #readOnlyText.see(END)

#==============ETAPES DE L'APPLICATION ZOOADAPT===========================

#Création des export.txt de chaque PID   +  Copies des images non coupées

def starthere():

    global Path, ExportPath, NewPath,adressPidList,WP2list,WP2PathList,adressCsv,adressXlsx,adressPidList,Csv,Xlsx,pid_df,stationList,stationLineCsv,MaxDepthList,startendlat,startendlon


    #Looking for all the WP2 directory in Path (Name & Path):
    WP2list=ls(Path,"WP2") 
    WP2PathList=glob(Path+'//'+'WP2*')
    
    
    #Création d'un dossier d'export en fonction des dossiers WP2 :
    NewPath = []
    for dos in WP2list:
        NewPath.append(create_dos(ExportPath,dos,"_exp"))
    
    #Attributing file's path to var:
    adressCsv = glob(Path+'//'+'*csv')[0]
    
    adressXlsx = glob(Path+'//'+'*xlsx')[0]
        
    adressPidList = []
    for i in WP2PathList:
        print(glob(i+'//'+'*pid'))
        adressPidList.append(glob(i+'//'+'*pid')[0])
    
    #Oppening big files with pandas
    Csv = read_csv(adressCsv,dtype=str, sep=sepCsv,encoding='latin-1')
    
    Xlsx = read_excel(adressXlsx)
    
    pid_df =[]
    for filename in adressPidList:
        pid_df.append(pid_with_pandas(filename, "[Data]",'\t'))
    
    
    #Creation liste station in xlsx
    stationList=[]
    for i in range(Xlsx.shape[0]):
        stationList.append(Xlsx['station'][i])
    
    
    #Récupération index des stations dans le CSV:
    stationLineCsv=[]
    for i in stationList:
        stationLineCsv.append(index_in_col(Csv, 'Num Station', i))
    #pour la meme station , Si il y a deux lignes et donc deux profondeurs max, je dois prendre la plus grande ? ____________________
    #Recherchons dans le pelgas.CSV la profonseur max de chaque station(s)  +  #Récupértion latitude longitude start end in csv:
    MaxDepthList=[]
    startendlat=[]
    startendlon=[]
    for i in stationLineCsv:
        max=0
        tempstartendlat=[]
        tempstartendlon=[]
        for j in i:
            tempstartendlat.append(Csv['Latitude'][j])
            tempstartendlon.append(Csv['Longitude'][j])
            if max<float(Csv['Sonde ref. (m)'][j].replace(",", ".")):
                max=float(Csv['Sonde ref. (m)'][j].replace(",", "."))
            
        MaxDepthList.append(max)
        startendlat.append(tempstartendlat)
        startendlon.append(tempstartendlon)
    for i in range(len(pid_df)):
        ls_deleted_objects_wp.append(0)
        export(i)
        image_creator(i)
        
    print("Ended")
    print(ls_deleted_objects_wp)
    #readOnlyText.insert('end','\n\n\nProcess ended.\n')
    #readOnlyText.insert('end',"Total of cutted files : "+ str(deleted_files_number_total))
    #for i in range(len(WP2list)):
        #readOnlyText.insert('end',"\nCutted files in "+WP2list[i]+" : "+ str(ls_deleted_objects_wp[i]))
    #readOnlyText.see(END)
    end = Label (text ="completed successfully")
    end.grid(row=14,column=3)



##################INSTANT PROCESS######################

st.title("ZooAdapt")
Path = st.text_input('Please enter import path')
ExportPath = st.text_input('Please enter Export path')
if Path!="" and ExportPath!="":
  st.write("import path : "+Path)
  st.write("export path : "+ExportPath)

station=st.checkbox("Station")
latlon=st.checkbox("Latitude & Longitude")
Z=st.checkbox("Zmin & Zmax")

st.button(label="start", on_click=lambda :Thread(target=starthere, daemon=True).start())
 
my_bar=st.progress(0)
