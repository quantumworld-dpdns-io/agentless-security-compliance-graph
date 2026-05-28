from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "compliance-graph"
    debug: bool = False
    environment: Literal["dev", "staging", "production"] = "dev"
    database_url: str = "compliance_graph.db"
    redis_url: str = "redis://localhost:6379"
    otel_endpoint: str = "http://localhost:4317"
    log_level: str = "INFO"

    class Config:
        env_prefix = "CG_"

settings = Settings()
