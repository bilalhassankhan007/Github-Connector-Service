from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.config import settings
from app.github_service import GitHubAPIError
from app.routes import router

settings.validate()

app = FastAPI(title="GitHub Connector")

app.include_router(router)


@app.exception_handler(GitHubAPIError)
async def github_api_error_handler(request: Request, exc: GitHubAPIError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.message,
        },
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
        },
    )
