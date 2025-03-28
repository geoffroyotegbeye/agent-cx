from fastapi import FastAPI
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from fastapi.middleware.cors import CORSMiddleware
import re

# Initialiser l'application FastAPI
app = FastAPI()

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autorise toutes les origines (à restreindre en prod)
    allow_credentials=True,
    allow_methods=["*"],  # Autorise toutes les méthodes HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Autorise tous les headers
)

# Initialiser le modèle
llm = ChatOllama(model="deepseek-r1", temperature=0.5)

# Définir le template de prompt
prompt = PromptTemplate(
    input_variables=["question"],
    template="Tu es un assistant virtuel conçu pour fournir des réponses complètes et détaillées. Réponds à la question suivante en fournissant autant d'informations pertinentes que possible. Réponds toujours en Français: {question}"
)

# Créer la séquence exécutable
chain = prompt | llm

# Définir la structure de la requête
class QuestionRequest(BaseModel):
    question: str

# Fonction pour nettoyer la réponse générée et extraire la bonne réponse
def clean_response(response) -> str:
    # Accéder directement à la propriété `content` de l'objet `response` (qui est un AIMessage)
    content = response.content if hasattr(response, 'content') else ''
    
    # Suppression de tout texte entre les balises <think>...</think>
    cleaned_content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip()
    
    # Optionnel : on peut nettoyer d'autres parties si nécessaire (par exemple, les balises HTML)
    cleaned_content = cleaned_content.replace("\n", " ").strip()
    
    return cleaned_content

@app.post("/chat")
async def chat(request: QuestionRequest):
    question = request.question
    response = chain.invoke({"question": question})
    
    # Appliquer le nettoyage de la réponse
    cleaned_response = clean_response(response)
    
    return {"response": cleaned_response}
