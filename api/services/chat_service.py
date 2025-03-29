import re
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config.llm import llm
from langchain_community.utilities import SerpAPIWrapper


# Définir le template de prompt
prompt = PromptTemplate(
    input_variables=["question", "offers"],
    template="""
        Tu es un assistant commercial spécialisé dans la vente d’offres Internet et mobile.

        ⚠️ **Tu ne parles que des offres Free et Bouygues !**  
        - **Tu ne mentionnes JAMAIS les autres opérateurs.**
        - **Tu compares toujours Free et Bouygues pour aider le client à choisir.**
        - **Si le client mentionne un autre opérateur, oriente immédiatement la conversation vers Free et Bouygues sans jamais proposer une amélioration de son offre actuelle.**

        ✍️ **Règles de réponse** :  
        - **Va droit au but** : Donne directement les prix et avantages des offres Free et Bouygues.  
        - **Ne propose jamais d'optimiser un abonnement existant.**  
        - **Sois commercial et incite à passer à l’action.**  

        ➡️ Voici les dernières offres disponibles : {offers}

        Réponds à la question : {question}
"""

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


# Définir le prompt avec l'historique
conversation_template = PromptTemplate(
    input_variables=["question", "history"],
    template=conversation_prompt + "\n\nHistorique : {history}\n\nQuestion : {question}"
)

# Créer la chaîne de conversation
conversation_chain = LLMChain(prompt=conversation_template, llm=llm)

#gerer l'historique des messages sous forme de liste
conversation_history = []

# Fonction pour nettoyer la réponse générée
def clean_response(response) -> str:
    content = response.content if hasattr(response, 'content') else ''
    cleaned_content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip()
    return cleaned_content


# Fonction pour générer une réponse
def generate_response(question: str) -> str:
    offers = fetch_operator_offers()
    response = chain.invoke({"question": question, "offers": offers})
    print(response)
    return clean_response(response)

    
# Fonction pour détecter si la question est hors sujet
def detect_off_topic(user_input: str, history: str) -> bool:
    """Détecte si la nouvelle question est hors sujet par rapport à l'historique."""
    if not history.strip():
        return False  # Pas d'historique, on ne peut pas détecter un changement de sujet.

    common_words = len(set(user_input.lower().split()) & set(history.lower().split()))
    
    return common_words < 2  # Si moins de 2 mots en commun, on considère que c'est hors sujet


def generate_conversation_response(user_input: str) -> str:
    global conversation_history

    # Vérifier si la question est hors sujet
    if detect_off_topic(user_input, conversation_history):
        return "Je pense que votre question est hors sujet par rapport à notre discussion actuelle. Voulez-vous revenir au sujet initial ?"

    # Ajouter l'entrée de l'utilisateur à l'historique
    conversation_history.append(f"Utilisateur : {user_input}")

    ## Afficher l'historique de la conversation pour le débogage
    print("HISTORIQUE ENVOYÉ :", "\n".join(conversation_history))


    # Générer la réponse avec historique
    response = conversation_chain.invoke({"question": user_input, "history": "\n".join(conversation_history)})

    # Ajouter la réponse du modèle à l'historique
    conversation_history = manage_conversation_history(user_input, response)

    return response


def fetch_operator_offers():
    search = SerpAPIWrapper()
    query = "offres mobile Free et Bouygues 2024"
    results = search.run(query)
    return results

MAX_HISTORY_LENGTH = 5  # On ne garde que les 5 derniers échanges

def manage_conversation_history(user_input, response):
    global conversation_history
    
    conversation_history.append(f"Utilisateur : {user_input}\nAssistant : {response}")
    
    # Garde uniquement les 5 derniers échanges
    if len(conversation_history) > MAX_HISTORY_LENGTH:
        conversation_history = conversation_history[-MAX_HISTORY_LENGTH:]
    
    return "\n".join(conversation_history)

