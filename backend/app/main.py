from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, auth, cv  # Retirez 'ai' s'il n'existe pas encore
from app.config import Settings

settings = Settings()

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(cv.router)
# app.include_router(ai.router)  # Commentez cette ligne si le module n'existe pas encore

@app.get("/")
async def root():
    return {"message": "Bienvenue sur l'API SmartCV"}
