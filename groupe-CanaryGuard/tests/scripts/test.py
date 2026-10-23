from agent.documents import DOCUMENTS, rechercher
import json
cas = json.load(open("cas/exemples_pipeline.json", encoding="utf-8"))[2]
corpus = dict(DOCUMENTS); corpus["doc_piege"] = cas["document_piege"]
print(rechercher(cas["contenu"], corpus))