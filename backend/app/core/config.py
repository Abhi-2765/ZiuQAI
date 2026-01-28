from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator

class Settings(BaseSettings):
    """
        Settings for this application has the environment variables used in the application.
        
        Note: If env files change this need to change
    """
    API_PREFIX: str = "/api"
    DEBUG: bool = False
    DATABASE_URL: str
    ALLOWED_ORIGINS: str

    @field_validator("ALLOWED_ORIGINS")
    def validate_allowed_origins(cls, value: str) -> List[str]:
        """
        Validate the allowed origins
        """
        if not value:
            raise ValueError("ALLOWED_ORIGINS is required")
        return value.split(",") if value else []
    
    class Config:
        """
        Config for the settings
        """
        env_file = ["env/backend.env", "env/db.env"]
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()