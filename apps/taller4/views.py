from django.shortcuts import render
#import ner
#from nltk.tag import StanfordNERTagger
#from nltk.tokenize import word_tokenize
import sys
import SPARQLWrapper
from SPARQLWrapper import SPARQLWrapper, JSON
from django.core.paginator import Paginator
from pymongo import MongoClient
import json
import re
from collections import Counter

from conexionmongo import Connection

from bson.json_util import dumps
# Create your views here.
def taller4_parte1(request): #ESTA VISTA ME MUETRA LAS PREGUNTAS CON SU INFORMACION 
    conn = Connection()
    if request.GET.get('page') != None:
        PAGE = int(request.GET.get('page'))
    else:
        PAGE = 1
    #Conexion a MongoDB
    #cliente = MongoClient()#Inicializar objeto
    #cliente = MongoClient('127.0.0.1', 27017)#Indicar parametros del servidor
    #bd = cliente.taller4 #Seleccionar Schema
    coleccion =conn.bd.body_pregunta  #Seleccionar Coleccion  
    coleccion2=conn.bd.body_respuestas
    coleccion_con_movies=conn.bd.peliculas_en_preguntas
    coleccion_con_movies_respuestas=conn.bd.peliculas_en_respuestas
    coleccion_con_tuitrespuesta=conn.bd.tuit_respuestas2
    coleccion_con_tuitpregunta=conn.bd.tuit_preguntas2

    count=coleccion.count()
    numero_preguntas_pagina=1
    consulta1= coleccion.find().skip(numero_preguntas_pagina * (PAGE-1)).limit(numero_preguntas_pagina)
    pregunta_for_front=coleccion.find().skip(numero_preguntas_pagina * (PAGE-1)).limit(numero_preguntas_pagina)
    consulta2= coleccion2.find().skip(numero_preguntas_pagina * (PAGE-1)).limit(numero_preguntas_pagina)
    consulta_movies=coleccion_con_movies.find().skip(numero_preguntas_pagina * (PAGE-1)).limit(numero_preguntas_pagina)

    consulta_tuitpregunta=coleccion_con_tuitpregunta.find().skip(numero_preguntas_pagina * (PAGE-1)).limit(numero_preguntas_pagina)
    #jsondata = {}
    n=1
    salida={}
    datos=[]
    for los_id_pregunta in pregunta_for_front:
        id_pregunta=int(los_id_pregunta.get("items")[0]["question_id"])  
        datos.append(id_pregunta)
    print datos


    datta=  coleccion2.find({"items.0.question_id": { '$in': datos} })
    movies= coleccion_con_movies.find({"items.0.question_id": { '$in': datos} })
    movies_r= coleccion_con_movies_respuestas.find({"items.0.question_id": { '$in': datos} })
    tuits= coleccion_con_tuitpregunta.find({"items.0.question_id": { '$in': datos} })
    tuits2= coleccion_con_tuitpregunta.find({"items.0.question_id": { '$in': datos} })
    sema= coleccion_con_tuitpregunta.find({"items.0.question_id": { '$in': datos} })

    print movies
    infoPage={'countPage': count, 'num_pages': count/numero_preguntas_pagina + 1, 'page':PAGE,'previous_page_number':PAGE-1, 'next_page_number':PAGE+1}
    return render(request, "taller4_parte1.html",{"consulta1":consulta1, "datta":datta,"movies":movies,"movies_r":movies_r,"tuits":tuits ,"tuits2":tuits2 ,"sema":sema ,"infoPage":infoPage})



def relationship (request):
    conn = Connection()
    if request.GET.get('page') != None:
        PAGE = int(request.GET.get('page'))
    else:
        PAGE = 1
    coleccion = conn.bd.body_pregunta  #Seleccionar Coleccion  
    count=coleccion.count()
    numero_preguntas_pagina=1
    consulta1= coleccion.find().skip(numero_preguntas_pagina * (PAGE-1)).limit(numero_preguntas_pagina)
    consulta2= coleccion.find().skip(numero_preguntas_pagina * (PAGE-1)).limit(numero_preguntas_pagina)
         
    infoPage={'countPage': count, 'num_pages': count/numero_preguntas_pagina + 1, 'page':PAGE,'previous_page_number':PAGE-1, 'next_page_number':PAGE+1}
    return render(request, "relation.html",{"consulta1":consulta1,"consulta2":consulta2,"infoPage":infoPage})

def taller4_parte2(request):
    conn = Connection()
    if request.GET.get('page') != None:
        PAGE = int(request.GET.get('page'))
    else:
        PAGE = 1
    array_para_tagcloud=[]
    b=[]
    h=[]
    array_para_hash=[]
    conn = Connection()

    cons_palabras =conn.bd.peliculas.find({},{"Plot":1,"_id":0})
    consulta_peliculas =conn.bd.peliculas.find()
    a=0
    arrayList = []
    coleccion =conn.bd.body_pregunta
    count=coleccion.count()
    numero_preguntas_pagina=1
    pregunta_for_front=coleccion.find().skip(numero_preguntas_pagina * (PAGE-1)).limit(numero_preguntas_pagina)
    datos=[]
    for los_id_pregunta in pregunta_for_front:
        id_pregunta=int(los_id_pregunta.get("items")[0]["question_id"])
        datos.append(id_pregunta)
    print datos

    for h in cons_palabras:
        print conn.bd.peliculas.find({"items.0.question_id":{ '$in': datos}})
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
        if p[0]not in ("him","him ","two","two ","other ","other","set","set ","them ","them","short ","can ","But ","But","first","first ","get","get ","was","was ","all","all ","while","while ","its","its ","After","After ","wants","wants ","how","how ","When ","takes ","takes","two","two ","This","This ","","have","have ","out","one","out ","one ","into ","into","not","will","When","this ","this","not ","will ","through","through ","which","which ","about ","about","they","they ","when","when ","who ","what ","what ","that ","that","she ","she","but","but ","they",'Plot',"the","Plot'","the ","and ","his ","with ","who","from","the","that","for","her","about","hism","was","out","The","her ","from ","are", "has ","for ","The ","The","are ","their "):
           # print p[0]+":"
            b.extend([{campo1:p[0],campo2:p[1]}])

        for h in  listahash.most_common(300):#trae los has
            array_para_hash.extend([{campo1:h[0],campo2:h[1]}])

    # en la letra b llega el array para poder graficar el tag en el formato     
    # haciendo el tagcloud de hastag



    infoPage={'countPage': count, 'num_pages': count/numero_preguntas_pagina + 1, 'page':PAGE,'previous_page_number':PAGE-1, 'next_page_number':PAGE+1}
    return render(request, "taller4_parte2.html",{"obj":json.dumps(b),"array_para_hash":array_para_hash,"consulta_peliculas":consulta_peliculas,"infoPage":infoPage})

def taller4_parte3(request):
    numero3=79
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?lat
    WHERE { <http://dbpedia.org/resource/Colombia> geo:lat ?lat }
""")
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for result in results["results"]["bindings"]:
        a=2
        #print (result["lat"]["value"]).decode(string)
    lat=(result["lat"]["value"]) 
    print lat   
    #Trae los valores de longitud 
    sparql.setQuery("""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?long
        WHERE { <http://dbpedia.org/resource/Colombia> geo:long ?long }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for result in results["results"]["bindings"]:
        a=2
        #print (result["long"]["value"])
    longit=(result["long"]["value"]) 
    print longit

    return render(request, "taller4_parte3.html",{"longit":longit,"lat":lat})


def taller4_parte4(request):
    b="funciona"

    return render(request, "taller4_parte4.html",{"b":b})