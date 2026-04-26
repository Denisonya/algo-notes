from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.web.dependencies import get_current_username_from_cookie

router = APIRouter(tags=["Web Pages"])
templates = Jinja2Templates(directory="templates")


@router.get("/")
def home(request: Request):
    username = get_current_username_from_cookie(request)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "username": username
        }
    )