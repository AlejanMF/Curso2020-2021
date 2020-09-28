# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tV5j-DRcpPtoJGoMj8v2DSqR_9wyXeiE

**Task 07: Querying RDF(s)**
"""

# !pip install rdflib 
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2020-2021/master/Assignment4"

"""Leemos el fichero RDF de la forma que lo hemos venido haciendo"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/resources/example6.rdf", format="xml")

"""
**TASK 7.1: List all subclasses of "Person" with RDFLib and SPARQL**

**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

**TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib and SPARQL**
"""

from rdflib.plugins.sparql import prepareQuery
VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
ns = Namespace("http://somewhere#")

# TASK 7.1
print("TASK 7.1")

for subj, pred, obj in g.triples((None, RDFS.subClassOf, ns.Person)):
    print(subj, pred, obj)

print("")
query = prepareQuery('''
  SELECT 
    ?Subject
  WHERE { 
    ?Subject rdfs:subClassOf ns:Person
  }
  LIMIT 100
  ''',
  initNs = { "rdfs": RDFS, "ns": ns}
)

for res in g.query(query):
  print(res)

# TASK 7.2
print("\nTASK 7.2")
for subj, pred, obj in g.triples((None, RDF.type, ns.Person)):
    print(subj) # This only gets persons, we need the subclass of person "researcher"

for subj, pred, obj in g.triples((None, RDFS.subClassOf, ns.Person)):
    for s, p, o in g.triples((None, RDF.type, subj)):
        print(s)

print("")
query = prepareQuery('''
  SELECT 
    ?Subject
  WHERE { 
    {
    ?Subject rdf:type ns:Person .
    }UNION{
        ?subj rdfs:subClassOf ns:Person .
        ?Subject rdf:type ?subj
    }
  }
  LIMIT 100
  ''',
  initNs = { "rdfs": RDFS, "rdf": RDF, "ns": ns}
)

for res in g.query(query):
  print(res)

# TASK 7.3
print("\nTASK 7.3")
for subj, pred, obj in g.triples((None, RDF.type, ns.Person)):
    for s, p, o in g.triples((subj, None, None)):
        print(s, p, o)

for subj, pred, obj in g.triples((None, RDFS.subClassOf, ns.Person)):
    for s, p, o in g.triples((None, RDF.type, subj)):
        for ss, pp, oo in g.triples((s, None, None)):
            print(ss, pp, oo)

print("")
query = prepareQuery('''
  SELECT 
    ?Data ?WhatEver ?Object
  WHERE { 
    {
    ?Data rdf:type ns:Person .
    ?Data ?WhatEver ?Object .
    }UNION{
        ?tmp rdfs:subClassOf ns:Person .
        ?Data rdf:type ?tmp .
        ?Data ?WhatEver ?Object
    }
  }
  LIMIT 100
  ''',
  initNs = { "rdfs": RDFS, "rdf": RDF, "ns": ns}
)

for res in g.query(query):
  print(res)
