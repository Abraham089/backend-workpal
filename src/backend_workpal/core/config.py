from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  # Cors
  FRONTEND_URL: str = "http://localhost:5173"
  FRONTEND_IP_URL: str = "http://127.0.0.1:5173"
  FRONTEND_DOCKER_URL: str = "http://172.18.0.2:5173"

  # Authentication
  SECRET_KEY: str
  ALGORITHM: str
  ACCESS_TOKEN_EXPIRE_MINUTES: int

  model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()