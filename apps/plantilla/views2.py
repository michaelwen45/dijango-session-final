from pymongo import MongoClient
from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.http import JsonResponse

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

#def archive (request)
def inicio(request):
    return render(request, 'inicio.html')

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

    return render(request, "taller3.html",{"form":form, "numero_seguidores":numero_seguidores,"nombre_usuario":nombre_usuario,"amigos":amigos,"num_sent_p":num_sent_p,"num_sent_n":num_sent_n,"num_sent_neu":num_sent_neu,"num_sent_muyp":num_sent_muyp,"num_sent_muyn":num_sent_muyn,"total_polarida":total_polarida,"usuario":usuario,"lista":lista,"historico19":historico19,"historico22":historico22})


def tagcloud(request):

    print "cambios en la vista de taller 3"
    conn = Connection()

    cons_palabras =conn.db.pertemas.find({},{"text":1,"_id":0})
    a=0
    arrayList = []
    for h in cons_palabras:
        a=a+1
       	arrayList.append(h)
    #reg = re.compile('\S{3,}')
    reg = re.compile('([a-zA-Z]{3,}[^0-9])')
    lista = Counter(ma.group() for ma in reg.finditer(str(arrayList).strip('[]')))
	
    


#for armado in lista:
	
	   
    return render(request, "tagcloud.html",{"lista":lista})

