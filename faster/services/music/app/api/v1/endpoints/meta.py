from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/health")
async def health_check(request: Request):
    return JSONResponse(content={"status": "ok"}, status_code=200)

@router.get("/version")
async def version_check(request: Request):
    return JSONResponse(content={"version": "1.0.0"}, status_code=200)

@router.get("/routes")
async def list_routes(request: Request):
    route_list = []
    for route in request.app.routes:
        route_list.append({
            "path": route.path,
            "name": route.name,
            "methods": list(route.methods),
        })
    return JSONResponse(content={"routes": route_list}, status_code=200)

