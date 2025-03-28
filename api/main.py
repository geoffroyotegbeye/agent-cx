from fastapi import FastAPI
from config.cors import setup_cors
from controllers.chat_controller import router as chat_router

app = FastAPI()

# Appliquer la configuration CORS
setup_cors(app)

# Inclure les routes
app.include_router(chat_router)
