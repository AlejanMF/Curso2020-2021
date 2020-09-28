# -*- coding: utf-8 -*-
"""Task08.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18P0xTS31q1P7nR4efg0Yy3QrClOxqMAe

**Task 08: Completing missing data**
"""

# !pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2020-2021/master/Assignment4/"

from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF
g1 = Graph()
g2 = Graph()
g1.parse(github_storage+"resources/data01.rdf", format="xml")
g2.parse(github_storage+"resources/data02.rdf", format="xml")

"""Tarea: lista todos los elementos de la clase Person en el primer grafo (data01.rdf) y completa los campos (given name, family name y email) que puedan faltar con los datos del segundo grafo (data02.rdf). Puedes usar consultas SPARQL o iterar el grafo, o ambas cosas."""
# Para ver el grafo inicialmente
print("\nGrafo 1 incompleto")
for s, p, o in g1:
  print(s,p,o)
  
from rdflib.plugins.sparql import prepareQuery

data = Namespace("http://data.org#")
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")

print("\nElementos de la clase Person en el primer grafo: ")

q1 = prepareQuery('''
  SELECT 
    ?Subject
  WHERE { 
    ?Subject rdf:type ns:Person
  }
  ''',
  initNs = { "ns": data, "rdf": RDF}
  )
for r in g1.query(q1):
  print(r.Subject)


# Para ver el grafo2 inicialmente
print("\nGrafo2 completo: ")
for s, p, o in g2:
  print(s,p,o)
  
print("\nDatos faltantes en el primer grafo: ")

q2 = prepareQuery('''
  SELECT 
    ?Subject ?Predicate ?Object
  WHERE {
    ?Subject ?Predicate ?Object
    FILTER(?Predicate=vcard:FN || ?Predicate=vcard:Given || ?Predicate=vcard:EMAIL)
  }
  ''',
  initNs = { "vcard": vcard}
  )

for r in g2.query(q2):
  print(r)
  g1.add(r)
  
print("\nGrafo 1 completo: ")

for s, p, o in g1:
  print(s,p,o)