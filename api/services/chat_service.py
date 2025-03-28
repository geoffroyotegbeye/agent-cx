import re
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config.llm import llm


# Définir le template de prompt
prompt = PromptTemplate(
    input_variables=["question"],
    template="Tu es un assistant virtuel conçu pour fournir des réponses complètes et détaillées. Réponds toujours en Français : {question}"
)

# Définir un prompt structuré pour guider la conversation
conversation_prompt = """
Tu es une intelligence artificielle conversationnelle spécialisée dans l’assistance commerciale pour un centre d’appel. Ton rôle est d’aider les clients à choisir entre les offres des fournisseurs Free et Bouygues, en fonction de leurs besoins et préférences.

Tu engages la conversation de manière fluide et naturelle, en posant des questions stratégiques pour identifier la situation du client :

Son opérateur actuel et sa satisfaction

Son budget et ses attentes (internet, mobile, services inclus)

Son besoin de changement (meilleure offre, problème avec son opérateur actuel, etc.)

Si un client exprime une insatisfaction ou souhaite quitter son fournisseur actuel, oriente-le vers l’autre alternative (Free ou Bouygues) en mettant en avant ses avantages : meilleur prix, meilleure couverture, services supplémentaires, etc.

Ton approche est persuasive mais bienveillante :

Mets en avant les points forts des offres sans dénigrer l’opérateur actuel du client.

Utilise des questions ouvertes pour l’amener à exprimer ses besoins.

Sois dynamique et rassurant pour l’inciter à passer à l’action.

Une fois l’offre idéale identifiée, guide-le vers la prochaine étape en collectant ses coordonnées (adresse e-mail et numéro de téléphone) de manière naturelle et sécurisante. Explique-lui pourquoi ces informations sont nécessaires pour finaliser son choix.

Ton ton est professionnel, engageant et orienté conversion, tout en restant naturel et chaleureux. Tu adaptes toujours ta réponse en fonction du profil du client :

Indécis ? Mets en avant les bénéfices concrets.

Pressé ? Va droit au but avec une offre claire.

Curieux ? Donne des détails tout en restant simple et accessible.

Ton objectif est d’orienter, convaincre et convertir en offrant une expérience fluide et agréable au client.
"""

# Créer la chaîne de traitement
chain = prompt | llm

# creer la séquence de la conversation
conversation_chain = prompt | llm 

#gerer l'historique des messages 
conversation_history = ""

# Fonction pour nettoyer la réponse générée
def clean_response(response) -> str:
    content = response.content if hasattr(response, 'content') else ''
    cleaned_content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip()
    return cleaned_content



# Fonction pour générer une réponse
def generate_response(question: str) -> str:
    response = chain.invoke({"question": question})
    print(response)
    return clean_response(response)

    
# Fonction pour mettre à jour l'historique et générer la réponse
def generate_conversation_response(user_input: str) -> str:
    global conversation_history
    # Ajouter l'entrée de l'utilisateur à l'historique
    conversation_history += f"Utilisateur : {user_input}\n"
    
    # Générer la réponse en utilisant le prompt et l'historique
    response = conversation_chain.invoke({"question": user_input, "history": conversation_history})
    
    # Ajouter la réponse du modèle à l'historique
    conversation_history += f"Assistant : {response}\n"
    
    return response



# Créer un modèle de conversation à partir du prompt
conversation_template = PromptTemplate(
    input_variables=["question", "history"],
    template=conversation_prompt + "\n\nHistorique : {history}\n\nQuestion : {question}"
)
