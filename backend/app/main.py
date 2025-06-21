from fastapi import FastAPI
from app.routes import user
from app.database import engine
from app.models import user as user_model
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Nexlify Backend", description="User Management API", version="0.1.0")

# Create database tables
user_model.Base.metadata.create_all(bind=engine)

# CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # Streamlit default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include user routes
app.include_router(user.router, prefix="/users", tags=["Users"])

@app.get("/")
async def root():
    return {"message": "Welcome to Nexlify Backend"}