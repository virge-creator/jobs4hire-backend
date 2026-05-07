from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    app_name: str = "Jobs4Hire API"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/jobs4hire"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Auth — WorkOS
    workos_api_key: str = ""
    workos_client_id: str = ""
    workos_redirect_uri: str = "http://localhost:3000/api/auth/callback"

    # JWT
    jwt_algorithm: str = "RS256"
    jwt_audience: str = ""
    jwt_issuer: str = ""

    # AWS S3
    aws_s3_bucket: str = "jobs4hire-uploads"
    aws_region: str = "eu-west-1"

    # Polar.sh
    polar_api_key: str = ""
    polar_webhook_secret: str = ""

    # Resend
    resend_api_key: str = ""

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
