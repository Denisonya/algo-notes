from fastapi import APIRouter

from app.web.routers import (
    auth,
    categories,
    notes,
    pages,
)

# Главный Web router собирает отдельные web-роутеры в один
router = APIRouter(tags=["Web"])

router.include_router(pages.router)
router.include_router(auth.router)
router.include_router(categories.router)
router.include_router(notes.router)
