from pymongo import MongoClient
from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



import os
import sys
import json 
import glob
from conexionmongo import Connection
from .forms import form_usuario

from collections import Counter
import re
import smtplib
from array import *

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
#HACIENDO UN SUBPROCESO
archivo_cluster=os.system ("scp cluster_bigdata:lasalida/* /home/estudiante/GrafoconTaller2/DJANGOTaller2-master")
print archivo_cluster
##TERMINANDO EL SUBPROCESO

@csrf_exempt
#def archive (request)
def inicio(request):
    return render(request, 'inicio.html')
@csrf_exempt
def findNodeId(nodeLabel,graph):
    #graph = {"nodes": [], "edges": []}
    nodes = graph["nodes"]
    for n in nodes:
        if n["label"]==nodeLabel:
            return n["id"]
    return -1

def index(request):
    return render(request, "index.html", {})

def grafo(request):
    return render(request, "grafo.html")
array=[]
#--------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------
#------------------------------PARTE DEL TALLER 2-------------------------------------------------------------------------------------------
pais=""
def mygraph(request):
    graph = {"nodes": [], "edges": []}
    read_files=['nombre_fecha_lugar_ultimo.txt','nombre_padre_padre_ultimo.txt','titulo_pareja_pareja_ultimo.txt']
    with open("archivo_completo.txt","w") as outfile:
	for f in read_files:
	    with open(f) as infile:
		outfile.write(infile.read())
    #LEYENDO EL ARCHIVO FINAL	
    file = open("archivo_completo.txt")
    pais=request.GET['country']
    b=request.GET['name']
    f_inicio=request.GET['fecha_inicio']
    f_fin=request.GET['fecha_fin']
    node_id=1
    edge_id=1
    for line in file:
        if  line.strip():
            line= line.replace("\r\n", "")
            line1=line.replace(", ",",")
            values= line1.split(",")

            try :
                toLabel= values[2]
                fromLabel= values[0]
                fecha=values[1]
                
            except :
                 toLabel= "a"
                 fromLabel= "a"
                 fecha="a"              
                 
            from_id=findNodeId(fromLabel, graph)
            if (fromLabel==b or (toLabel==pais and (f_inicio <= fecha <= f_fin))): #ESTE HACE EL FILTRO POR PAIS
                if from_id==-1:
                    nodes= graph["nodes"]
                    nodes.append({"id": node_id, "label": fromLabel})
                    from_id=node_id
                    node_id=node_id + 1

                to_id=findNodeId(toLabel, graph)
                if to_id==-1:
                    nodes= graph["nodes"]
                    nodes.append({"id": node_id, "label": toLabel})
                    to_id=node_id
                    node_id=node_id + 1


                e= {"from": from_id, "to":to_id, "label": values[1]}
                graph["edges"].append(e)
                edge_id=edge_id+1
    #print "aqui debe generar el json linea antes de json"
    #return JsonResponse(graph)
    return HttpResponse(json.dumps(graph,ensure_ascii=False).encode("utf8"),content_type="application/json")
#--------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------
#------------------------------PARTE DEL TALLER 3----------------

@csrf_exempt
def taller3(request):
    print "aQUI ENTRA A VIEWS.PY "
    conn = Connection()
    

    if request.method=="POST":
        form = form_usuario(request.POST)
        if form.is_valid():
            algo= form.cleaned_data['usuario']
	    nombre_usuario=algo
            e= conn.db.pertemas.find_one({"user.screen_name":algo})
	    numero_seguidores= e["user"]["followers_count"]
            consulta_amigos= conn.db.pertemas.find_one({"user.screen_name":algo})
	    amigos= consulta_amigos["user"]["friends_count"]
	    alfa ="and"
	    #CONSULTAS PARA SENTIMIENTO POSITIVO
            sentimiento_p =conn.db.polaridad.find({"$and":[{"tweet":{"$regex":algo}},{"sentimiento":"P"}]})
	    num_sent_p=0
	    num_sent_n=0
	    num_sent_neu=0
	    num_sent_muyp=0
	    num_sent_muyn=0
	    historico19=0
	    historico22=0

	    for h in sentimiento_p:
	    	num_sent_p=num_sent_p+1
	    #CONSULTAS PARA SENTIMIENTO NEGATIVO
            sentimiento_n =conn.db.polaridad.find({"$and":[{"tweet":{"$regex":algo}},{"sentimiento":"N"}]})
	    num_sent_n
	    for n in sentimiento_n:
	    	num_sent_n=num_sent_n+1
            sentimiento_neu =conn.db.polaridad.find({"$and":[{"tweet":{"$regex":algo}},{"sentimiento":"NEU"}]})
	    for neu in sentimiento_neu:
	    	num_sent_neu=num_sent_neu+1
            sentimiento_muyp =conn.db.polaridad.find({"$and":[{"tweet":{"$regex":algo}},{"sentimiento":"P+"}]})
	    for muyp in sentimiento_muyp:
	    	num_sent_muyp=num_sent_muyp+1
            sentimiento_muyn =conn.db.polaridad.find({"$and":[{"tweet":{"$regex":algo}},{"sentimiento":"N-"}]})
	    for muyn in sentimiento_muyn:
	    	num_sent_muyn=num_sent_muyn+1
	    total_polarida=num_sent_muyn+num_sent_muyp+num_sent_n+num_sent_p+num_sent_neu
	    #CONSULTAS PARA contar palabras dentro de los tuits
	    cons_palabras =conn.db.pertemas.find({},{"text":1,"_id":0})
	    a=0
	    arrayList = []
 	    for h in cons_palabras:
	        a=a+1
        	arrayList.append(h)
	    #reg = re.compile('\S{3,}')
	    reg = re.compile('([a-zA-Z]{3,}[^0-9])')
	    lista = Counter(ma.group() for ma in reg.finditer(str(arrayList).strip('[]')))	
	    #palabras_tuits=cp["text"]

	    #CONSULTAS PARA CONOCER EL HISTORICO 
            usuario="@" + algo	
	    print usuario
            consulta_19= conn.db.historico.find({"$and":[{"cuenta":usuario},{"fecha":"2016-10-19"}]}) 
	    for user in consulta_19:
		historico19= user.get("followers") 
	    #historico 22
            consulta_22= conn.db.historico.find({"$and":[{"cuenta":usuario},{"fecha":"2016-10-22"}]}) 
	    for user in consulta_22:
		historico22= user.get("followers") 
	    #historico 24
            consulta_24= conn.db.historico.find({"$and":[{"cuenta":usuario},{"fecha":"2016-10-24"}]}) 
	    for user in consulta_24:
		historico24= user.get("followers") 
	    #historico 25
            consulta_25= conn.db.historico.find({"$and":[{"cuenta":usuario},{"fecha":"2016-10-25"}]}) 
	    for user in consulta_25:
		historico25= user.get("followers") 
	    #historico 26
            consulta_26= conn.db.historico.find({"$and":[{"cuenta":usuario},{"fecha":"2016-10-26"}]}) 
	    for user in consulta_26:
		historico26= user.get("followers") 
	    #historico 27
            consulta_27= conn.db.historico.find({"$and":[{"cuenta":usuario},{"fecha":"2016-10-27"}]}) 
	    for user in consulta_27:
		historico27= user.get("followers") 
	    #historico 28
            consulta_28= conn.db.historico.find({"$and":[{"cuenta":usuario},{"fecha":"2016-10-28"}]}) 
	    for user in consulta_28:
		historico28= user.get("followers") 
	    #historico 29
            consulta_29= conn.db.historico.find({"$and":[{"cuenta":usuario},{"fecha":"2016-10-29"}]}) 
	    for user in consulta_29:
		historico29= user.get("followers") 

    else:
        form = form_usuario()
	numero_seguidores=""
	nombre_usuario=""
	amigos=""
	num_sent_p=""
	num_sent_n=""
	num_sent_neu=""
	num_sent_muyp=""
	num_sent_muyn=0
	total_polarida=0
	#palabras_tuits=""
	#historico19=0
	usuario=""
	lista=[]
	historico19=0
	historico22=0
	historico24=0
	historico25=0
	historico26=0
	historico27=0
	historico28=0
	historico29=0

    return render(request, "taller3.html",{"form":form, "numero_seguidores":numero_seguidores,"nombre_usuario":nombre_usuario,"amigos":amigos,"num_sent_p":num_sent_p,"num_sent_n":num_sent_n,"num_sent_neu":num_sent_neu,"num_sent_muyp":num_sent_muyp,"num_sent_muyn":num_sent_muyn,"total_polarida":total_polarida,"usuario":usuario,"lista":lista,"historico19":historico19,"historico22":historico22,"historico24":historico24,"historico25":historico25,"historico26":historico26,"historico27":historico27,"historico28":historico28,"historico29":historico29})

@csrf_exempt
def tagcloud(request):
	#Secuencia para hacer el tag cloud de palabras 
    array_para_tagcloud=[]
    b=[]
    h=[]
    array_para_hash=[]
    conn = Connection()

    cons_palabras =conn.db.pertemas.find({},{"text":1,"_id":0})
    a=0
    arrayList = []
    for h in cons_palabras:
       	arrayList.append(h)
    reg = re.compile('([a-zA-Z]{3,}[^0-9])')
    exprehash= re.compile("(\x23[a-zA-z]{3,})")
    lista = Counter(ma.group() for ma in reg.finditer(str(arrayList).strip('[]')))
    
    listahash = Counter(ma.group() for ma in exprehash.finditer(str(arrayList).strip('[]')))
    campo1="text"
    campo2="weight"
    quitar=["https"]
    for p in  lista.most_common(300):
        #print p[0]      
	if p[0]not in ('que ', 'xeda ','https:','text\'','por ','las ','los ',"del ",'para ','una ','sobr e','como ','xed ','con ','para ','por ','dos ','http: ','xeds ','Los ','son ','fue','nhttps:','pero ','Bogot\ ',' ser\ ','sus ','han ','fue ','dice ','todo ','sigue ','puede ','les ','sobre ',"est\ ","contra ","xedn ","ser ","deber\ ","Ord\ ","ana ","http: " ):
	   # print p[0]+":"
	    b.extend([{campo1:p[0],campo2:p[1]}])	

    for h in  listahash.most_common(300):#trae los has
	array_para_hash.extend([{campo1:h[0],campo2:h[1]}])	

	
	# en la letra b llega el array para poder graficar el tag en el formato 	
    # haciendo el tagcloud de hastag
	   
    return render(request, "tagcloud.html",{"obj":json.dumps(b),"array_para_hash":array_para_hash})

@csrf_exempt
def punto3(request):
	
    conn = Connection()
    cons_palabras =conn.db.pertemas.find({},{"text":1,"_id":0})
    numero=85
    numero_negative=0
    numero_positive=0
    numero_other=0
    numero_mixed=0

    numero_n=0
    numero_p=0
    debate_negative = conn.db.debate_sent_consulta.find({"sentiment_score_annoted":"Negative"})
    debate_positive = conn.db.debate_sent_consulta.find({"sentiment_score_annoted":"Positive"})
    debate_other = conn.db.debate_sent_consulta.find({"sentiment_score_annoted":"Other"})
    debate_mixed = conn.db.debate_sent_consulta.find({"sentiment_score_annoted":"Mixed"})

    deb_p= conn.db.debate_sent_consulta.find({"sentimiento":"P"})
    deb_n=conn.db.debate_sent_consulta.find({"sentimiento":"N"})
    for n in debate_negative:
        numero_negative = numero_negative+1
    for p in debate_positive:
        numero_positive = numero_positive+1

    for p in debate_other:
        numero_other = numero_other+1
    for p in debate_mixed:
        numero_mixed = numero_mixed+1

    for nn in deb_n:
        numero_n= numero_n+1
    for pp in deb_p:
        numero_p = numero_p+1


    total=numero_positive +numero_negative +numero_other+numero_mixed
    total1=numero_p +numero_n

    #para el otro dataset
    num_n=0
    num_p=0
    num_neutral=0
    sent_p= conn.db.sentiment.find({"sentiment":"Positive"})
    sent_n=conn.db.sentiment.find({"sentiment":"Negative"})
    sent_neutral=conn.db.sentiment.find({"sentiment":"Neutral"})

    for sn in sent_n:
        num_n = num_n+1
    for sp in sent_p:
        num_p = num_p+1
    for neutral in sent_neutral:
        num_neutral = num_neutral+1	
    total3=num_n+num_p +num_neutral

    return render(request, "punto3.html",{"numero":numero,"numero_negative":numero_negative,"numero_positive":numero_positive, "total":total, "total1":total1, "numero_n":numero_n, "numero_p":numero_p,"numero_other":numero_other,"numero_mixed":numero_mixed,"num_neutral":num_neutral,"num_n":num_n, "num_p":num_p,"total3":total3})


