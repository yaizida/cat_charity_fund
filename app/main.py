from fastapi import FastAPI

from app.core.config import settings
from app.api.endpoints.charity_project import router


app = FastAPI(title=settings.app_tittle,
              description=settings.app_description)

app.include_router(router)
