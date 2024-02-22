from pydantic import BaseSettings


class Settings(BaseSettings):
    app_tittle: str = 'Фонд помощи животным'
    app_description: str = 'Этот серивис помогает животным'
    database_url: str

    class Config:
        env_file = '.env'


settings = Settings()
