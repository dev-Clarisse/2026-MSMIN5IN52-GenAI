from agent.documents import rechercher, lire_document

resultats = rechercher("combien de jours de congés ?")
print("IDs trouvés :", resultats)  # Doit afficher ['doc_conges']

if resultats:
    texte_doc = lire_document(resultats[0])
    print("Contenu du document :", texte_doc)