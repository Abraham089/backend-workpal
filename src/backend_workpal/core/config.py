from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  # Cors
  FRONTEND_URL: str
  FRONTEND_IP_URL: str
  FRONTEND_DOCKER_URL: str

  # Authentication
  SECRET_KEY: str
  ALGORITHM: str
  ACCESS_TOKEN_EXPIRE_MINUTES: int

  model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()