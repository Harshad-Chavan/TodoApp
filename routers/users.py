import sys

from starlette import status
from starlette.responses import RedirectResponse

sys.path.append("..")

from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine

from .auth import get_current_user, get_password_hash, verify_password

router = APIRouter(prefix="/users", tags=["users"], responses={404: {"description": "Not found"}})

models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/change_password", response_class=HTMLResponse)
async def change_passowrd_page(request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    context = {"request": request}
    return templates.TemplateResponse("change_password.html", context)


@router.post("/change_password", response_class=HTMLResponse)
async def change_password(
    request: Request, db: db_dependency, old_password: str = Form(...), new_password: str = Form(...)
):
    context = {"request": request}
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    user_data = db.query(models.Users).filter(models.Users.id == user.get('id')).first()

    # Check if old password matched
    if verify_password(old_password, user_data.hashed_password):
        # allow to change
        new_password_hash = get_password_hash(new_password)
        user_data.hashed_password = new_password_hash
        db.add(user_data)
        db.commit()
        context['msg'] = "Password Changed successfully.Please login again"
        return templates.TemplateResponse("login.html", context)
        pass
    else:
        context['msg'] = "Old password is incorrect"
        return templates.TemplateResponse("change_password.html", context)

