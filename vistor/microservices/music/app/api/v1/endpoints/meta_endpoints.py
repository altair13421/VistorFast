from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
router = APIRouter()

@router.get("/routes", tags=["meta"])
def list_routes(request: Request):
    app = request.app  # FastAPI instance
    return [
        {
            "path": r.path,
            "methods": list(r.methods),
            "name": r.name,
            "endpoint": r.endpoint.__qualname__,
        }
        for r in app.routes
    ]

@router.get("/health", tags=["meta"])
def health_check():
    """
    Simple health check endpoint to verify that the service is running.
    """
    return {"status": "ok"}
