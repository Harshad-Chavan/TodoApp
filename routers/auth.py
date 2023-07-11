import sys

from starlette.responses import RedirectResponse, Response

sys.path.append("..")

from datetime import datetime, timedelta
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine

SECRET_KEY = "KlgH6AzYDeZeGwD288to79I3vTHT8wp7"
ALGORITHM = "HS256"

templates = Jinja2Templates(directory="templates")
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(bind=engine)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")


router = APIRouter(
    prefix="/auth", tags=["auth"], responses={401: {"user": "Not authorized"}}
)


class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def create_oauth_form(self):
        form = await self.request.form()
        self.username = form.get("email")
        self.password = form.get("password")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str, db):
    user = db.query(models.Users).filter(models.Users.username == username).first()

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(
    username: str, user_id: int, expires_delta: Optional[timedelta] = None
):
    encode = {"sub": username, "id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(request: Request):
    try:
        token = request.cookies.get("access_token")
        if token is None:
            return None
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            logout(request)
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=404, detail="Not Found")


@router.post("/token")
async def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return False
    token_expires = timedelta(minutes=60)
    token = create_access_token(user.username, user.id, expires_delta=token_expires)

    response.set_cookie(key="access_token", value=token, httponly=True)
    return True


@router.get("/", response_class=HTMLResponse)
async def authentication_page(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("login.html", context)


@router.post("/", response_class=HTMLResponse)
async def login(request: Request, db: db_dependency):
    try:
        # This basically converts the email id into username which is required format for oauth
        form = LoginForm(request)
        await form.create_oauth_form()
        response = RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)
        validate_user_cookie = await login_for_access_token(
            response=response, form_data=form, db=db
        )

        if not validate_user_cookie:
            msg = "Incorrect username/ Password"
            context = {"request": request, "msg": msg}
            return templates.TemplateResponse("login.html", context)
        return response
    except HTTPException:
        msg = "Unknown error"
        context = {"request": request, "msg": msg}
        return templates.TemplateResponse("login.html", context)


@router.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    msg = "Logout successful !"
    context = {"request": request, "msg": msg}
    response = templates.TemplateResponse("login.html", context)
    response.delete_cookie("access_token")
    return response


@router.get("/register", response_class=HTMLResponse)
async def registration_page(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("register.html", context)


@router.post("/register", response_class=HTMLResponse)
async def registration_user(
    request: Request,
    db: db_dependency,
    email: str = Form(...),
    username: str = Form(...),
    firstname: str = Form(...),
    lastname: str = Form(...),
    password: str = Form(...),
    password2: str = Form(...),
):
    username_exists_check = (
        db.query(models.Users).filter(models.Users.username == username).first()
    )
    email_exists_check = (
        db.query(models.Users).filter(models.Users.email == email).first()
    )

    if password != password2 or username_exists_check or email_exists_check:
        msg = "Invalid registration request"
        return templates.TemplateResponse(
            "register.html", context={"request": request, "msg": msg}
        )

    create_user_model = models.Users()
    create_user_model.email = email
    create_user_model.username = username
    create_user_model.first_name = firstname
    create_user_model.last_name = lastname

    hash_password = get_password_hash(password)

    create_user_model.hashed_password = hash_password

    create_user_model.is_active = True

    db.add(create_user_model)
    db.commit()

    msg = "User successfully Created"

    return templates.TemplateResponse(
        "register.html", context={"request": request, "msg": msg}
    )
