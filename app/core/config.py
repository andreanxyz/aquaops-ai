from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "AquaOps AI"
    DEBUG: bool = False
    DATABASE_URL: str = "postgresql+asyncpg://aquaops:aquaops@localhost:5432/aquaops_db"
    WHATSAPP_TOKEN: str = ""
    WHATSAPP_PHONE_ID: str = ""
    WHATSAPP_VERIFY_TOKEN: str = "aquaops_verify_2024"
    ANTHROPIC_API_KEY: str = ""
    CHROMA_PERSIST_DIR: str = "./knowledge_base/embeddings"

    class Config:
        env_file = ".env"

settings = Settings()
