import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.routes import api_router
from settings import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)
app.include_router(api_router, prefix=settings.API_V1_STR)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=settings.APP_PORT,
        host=settings.APP_HOST,
        reload=settings.APP_RELOAD,
    )
