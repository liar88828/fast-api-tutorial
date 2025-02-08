from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    JWT_SECRET_ACCESS_KEY: str = 'rahasia_session'
    JWT_SECRET_REFRESH_KEY: str = 'rahasia_refresh'
    JWT_ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_Day: int = 30
    DATABASE_URL: str = "mysql+aiomysql://root:@localhost:3306/mydatabase"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')
    ENCRYPTION_PASSWORD: str = "securepassword"  # Use a secure and secret password
    SALT: str = "static_salt_value"  # Salt for KDF, ideally unique per file


# SECRET_KEY='secret'
# JWT_SECRET_ACCESS_KEY = 'LhVjhTZNl9V4LhSYmlQkeB1m3As3+TUkmoMa1G5Eq+U='
# JWT_SECRET_REFRESH_KEY = 'eOW45FYqZgPFSLDQzJ9X6GPJ+cp5s9yj8zTAqFix7UA='
# JWT_ALGORITHM = 'HS256'
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
# REFRESH_TOKEN_EXPIRE_Day = 30
# DATABASE_URL = "mysql+aiomysql://root:@localhost:3306/mydatabase"

# DATABASE_URL = "sqlite:///./test.db"

settings = Settings()
